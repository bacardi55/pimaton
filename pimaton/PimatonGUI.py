import Tkinter as tk
import ttk as ttk

import datetime
import time
import logging

from PimatonUI import PimatonUI
from PimatonGUITK import PimatonGUITK

logging.basicConfig()
logger = logging.getLogger("Pimaton")


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

    def mainloop(self):
        self.app.mainloop()
