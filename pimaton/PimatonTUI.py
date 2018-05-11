import logging

from PimatonUI import PimatonUI
from PimatonExceptions import PimatonExceptions

logging.basicConfig()
logger = logging.getLogger("Pimaton")

try:
    import RPi.GPIO as GPIO
except BaseException:
    logger.debug('Couldn\'t load RPi.GPIO library')


class PimatonTUI(PimatonUI, object):
    def __init__(self, pimaton):
        super(PimatonTUI, self).__init__(pimaton)

        if 'GPIO' in self.pimaton.config['pimaton']['inputs']:
            logger.debug(
                'GPIO input is enabled - Start button configured on channel %s' %
                self.pimaton.config['GPIO']['start_button'])
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(
                self.pimaton.config['GPIO']['start_button'],
                GPIO.IN,
                pull_up_down=GPIO.PUD_UP)
            self.reset_gpio(self.pimaton.config['GPIO']['start_button'])

    def mainloop(self):
        while True:
            # Don't wait for a trigger is the single_loop is enabled.
            if self.pimaton.is_single_loop() is False and self.is_triggered() is False:
                continue

            if self.pimaton.is_single_loop():
                logger.info(
                    '*** Pimaton TUI *** Single Loop is True, not waiting for trigger!')

            logger.info(
                '*** Pimaton trigger has been pressed, starting taking pictures!')

            unique_key = self.pimaton.get_unique_key()
            taken_pictures = self.pimaton.take_pictures(unique_key)
            filename = self.pimaton.get_filename(unique_key)
            qrcode = self.pimaton.get_qrcode(unique_key)
            to_print = self.pimaton.generate_picture(
                taken_pictures,
                filename,
                qrcode,
                unique_key)

            if self.pimaton.is_print_enabled() is True:
                self.pimaton.print_picture(to_print)

            if self.pimaton.is_sync_enabled():
                self.pimaton.sync_pictures()

            if self.pimaton.is_single_loop():
                logger.info(
                    '*** Pimaton TUI *** Single Loop is True, exiting Pimaton')
                break

            self.pimaton.wait_before_next_iteration()
            if 'GPIO' in self.pimaton.config['pimaton']['inputs']:
                self.reset_gpio(self.pimaton.config['GPIO']['start_button'])

    def is_triggered(self):
        if 'GPIO' in self.pimaton.config['pimaton']['inputs']:
            if self.gpio_triggered is True:
                logger.debug('GPIO is ON and has been triggered.')
                return True
        # ELIF because keyboard and GPIO are not compatible yet.
        elif 'keyboard' in self.pimaton.config['pimaton']['inputs']:
            logger.debug('Waiting for start key to be pressed')
            # TODO: This will need to change for being able to manage both
            # keyboard and GPIO.
            input = raw_input("Press enter to start")
            return True
        else:
            # No other input compatible with TUI yet, raise an alert.
            raise PimatonTUIExceptions(
                'TUI mode has no compatible inputs configured.')

        return False

    def gpio_button_pressed(self, channel):
        logger.debug('GPIO button pressed callback.')
        self.gpio_triggered = True
        # To avoid multiple trigger, let's disable the event for now.
        self.remove_start_detection(channel)

    def remove_start_detection(self, channel):
        logger.debug('Removing event detection on channel %s' % channel)
        GPIO.remove_event_detect(channel)

    def reset_gpio(self, channel):
        logger.debug('GPIO reset callback.')
        self.gpio_triggered = False
        logger.debug('Start listening to event on channel %s' % channel)
        GPIO.add_event_detect(
            channel,
            GPIO.BOTH,
            callback=self.gpio_button_pressed,
            bouncetime=200)


class PimatonTUIExceptions(PimatonExceptions):
    pass
