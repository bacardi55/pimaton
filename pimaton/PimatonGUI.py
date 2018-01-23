import Tkinter as tk
import ttk as ttk

import datetime
import time

from PimatonUI import PimatonUI
from PimatonGUITK import PimatonGUITK


class PimatonGUI(PimatonUI, object):
    """
    GUI central class
    """
    def __init__(self, pimaton):
        super(PimatonGUI, self).__init__(pimaton)
        self.root = self.init_tk_root()
        self.app = self.init_tk_app(self.root)


    def init_tk_root(self):
        root = tk.Tk()
        root.attributes('-fullscreen', True)
        root.attributes('-topmost', True)
        root.config(cursor="none")

        return root

    def init_tk_app(self, root):
        app = PimatonGUITK(master=root, pimaton=self.pimaton)
        app.master.title("Pimaton PhotoBooth")
        # app.master.geometry('640x480')

        return app

    def mainloop(self):
        self.app.mainloop()




