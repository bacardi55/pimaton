import Tkinter as tk
import ttk as ttk

import datetime
import time
import logging

from PimatonUI import PimatonUI
from PimatonGUITK import PimatonGUITK

logging.basicConfig()
logger = logging.getLogger("Pimaton")

try:
    import RPi.GPIO as GPIO
except BaseException:
    logger.debug('Couldn\'t load GPIO library')


class PimatonGUI(PimatonUI, object):
    """
    GUI central class
    """

    def __init__(self, pimaton):
        super(PimatonGUI, self).__init__(pimaton)
        self.inputs = pimaton.config['pimaton']['inputs']
        logger.debug('inputs :%s' % self.inputs)

        self.root = self.init_tk_root()
        self.app = self.init_tk_app(self.root)

        self.gpio_lock = 1
        if 'GPIO' in self.inputs and 'GPIO' in pimaton.config:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(
                pimaton.config['GPIO']['start_button'],
                GPIO.IN,
                pull_up_down=GPIO.PUD_UP)
            self.gpio_listener(pimaton.config['GPIO']['start_button'])

    def init_tk_root(self):
        root = tk.Tk()
        root.attributes('-fullscreen', True)
        root.attributes('-topmost', True)
        root.config(cursor="none")

        # If keyboard enabled.
        if 'keyboard' in self.inputs:
            root.bind('<Return>', self.keyboard_trigger)

        return root

    def init_tk_app(self, root):
        app = PimatonGUITK(master=root, pimaton=self.pimaton)
        app.master.title("Pimaton PhotoBooth")

        return app

    def keyboard_trigger(self, event):
        logger.debug('keyboard triggered: %s' % event)
        self.app.start_triggered()

    def gpio_trigger(self, channel):
        logger.debug('GPIO triggered on channel %s' % channel)
        logger.debug('GPIO LOCK %s' % self.gpio_lock)
        # Horrible hack due to this bug:
        # https://sourceforge.net/p/raspberry-gpio-python/tickets/136/
        # That makes Pimaton segfault if we play with remove_event_detect.
        if self.gpio_lock % 2 == 0 or self.app.trigger_locked is True:
            logger.debug('GPIO is locked, ignoring.')
            self.gpio_lock = 1
            return
        self.gpio_lock = self.gpio_lock + 1

        logger.debug('App is not running, starting it now.')
        self.app.start_triggered()
        logger.debug("start triggered finished")
        # We can't use this, because of segfault error.
        # When it's done, release the kraken... hmm the lock.
        # self.gpio_unlock()

    # The following code should be used as it is a way cleaner way
    # To prevent Pimaton to run twice for some reason.
    # But for some reason, removing the event make Pimaton segfault.
    # def gpio_lock(self, channel):
    #     logger.debug('Removing event detection for now.')
    #     GPIO.remove_event_detect(channel)
    #
    # def gpio_unlock(self, channel):
    #     logger.debug('GPIO unlock: recreating listener on channel %s' % channel)
    #     self.gpio_listener(channel)

    def gpio_listener(self, channel):
        logger.debug('Adding event listener on channel %s' % channel)
        GPIO.add_event_detect(
            channel,
            GPIO.FALLING,
            callback=self.gpio_trigger,
            bouncetime=1000)

    def mainloop(self):
        self.app.mainloop()
