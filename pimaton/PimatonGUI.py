#!/usr/bin/env python2

#from __future__ import division, absolute_import, print_function
#from builtins import super

import Tkinter as tk
import ttk as ttk

import datetime
import time

from PimatonUI import PimatonUI


class PimatonGUIMain(tk.Frame, object):
    def __init__(self, master=None):
        super(PimatonGUIMain, self).__init__(master)
        self.parent = master
        self.pack(fill=tk.BOTH, expand=1)
        self.initialize_ui()

        # Load pimaton

    def initialize_ui(self):
        print('INIT UI')
        # Bootstrap UI layout.
        self.ui = {
            'header': self.create_header(),
            'footer': self.create_footer(),
            'screens': {
                'waiting': WaitingScreen(self),
                'processing': ProcessingScreen(self),
                'thanking': ThankyouScreen(self)
            }
        }

        # Show waiting screen to start with.
        self.ui['screens']['waiting'].show()

    def create_header(self):
        print('CREATE HEADER')
        header_frame = tk.Frame(self, background="green", height=1000)
        header_frame.pack(expand=0, fill=tk.X, side=tk.TOP, padx=10, pady=10)

        self.current_time = datetime.datetime.now().strftime('%H:%M')
        self.clock = tk.Label(header_frame, text=self.current_time)
        self.clock.pack(side=tk.LEFT, anchor="nw")
        tk.Label(header_frame, text="STATISTIQUES").pack(side=tk.RIGHT, anchor="ne")
        tk.Label(header_frame, text="WELCOME MESSAGE!").pack(side=tk.TOP)

        return header_frame

    def create_footer(self):
        print('CREATE FOOTER')
        footer_frame = tk.Frame(self, background="yellow")
        footer_frame.pack(expand=0, fill=tk.X, side=tk.BOTTOM, padx=10, pady=10)
        tk.Label(footer_frame, text="Disclaimer message!").pack(anchor=tk.CENTER)

        return footer_frame

    def set_clock(self):
        self.current_time = datetime.datetime.now().strftime('%H:%M')
        self.clock.config(text = self.current_time)
        self.clock.after(30000, self.set_clock)

    def ui_event(self, event):
        print('UI EVENT %s' % event)
        if event == 'start_triggered':
            # init
            self.ui['screens']['processing'].set_progress_value(0)
            self.ui['screens']['processing'].steptxt.set("Step 1/4: Starting taking pictures...")
            self.update_idletasks()
            time.sleep(1)
            # Show progress screen
            self.ui['screens']['waiting'].hide()
            self.ui['screens']['processing'].show()
            self.update_idletasks()
            time.sleep(5)

            # After run, you got the generated file.
            # Pimaton run.
            generated = 'todo'
            self.ui['screens']['processing'].set_progress_value(25)
            self.ui['screens']['processing'].set_step_value('Step 2/4: Generating picture to print')
            self.update_idletasks()

            time.sleep(10)
            self.ui['screens']['processing'].set_progress_value(50)
            self.ui['screens']['processing'].set_step_value('Step 3/4: Sending picture to printer')
            self.update_idletasks()

            time.sleep(10)
            self.ui['screens']['processing'].set_progress_value(75)
            self.ui['screens']['processing'].set_step_value('Step 4/4: Syncing picture to the internet')
            self.update_idletasks()

            time.sleep(10)
            self.ui['screens']['processing'].set_progress_value(100)
            self.ui['screens']['processing'].set_step_value('Finished! Your photo will be ready soon')
            self.update_idletasks()

            time.sleep(10)
            self.ui['screens']['processing'].hide()
            self.ui['screens']['thanking'].show()
            self.update_idletasks()

            time.sleep(10)
            self.ui['screens']['thanking'].hide()
            self.ui['screens']['waiting'].show()
            self.update_idletasks()


    def mainloop(self):
        self.set_clock()
        super(PimatonGUIMain, self).mainloop()


class WaitingScreen(tk.Frame, object):
    def __init__(self, master=None):
        super(WaitingScreen, self).__init__(master)
        self.parent = master
        self.create_waiting_screen()

    def create_waiting_screen(self):
        print('CREATE WAITING SCREEN')
        content_frame = tk.Frame(self, background="red")
        content_frame.pack(fill=tk.BOTH, expand=1, padx=10, pady=10)
        button_frame = tk.Frame(content_frame, background="orange", borderwidth=2)
        tk.Button(button_frame, text="START MESSAGE", command=self.trigger_start).pack(anchor=tk.CENTER)
        button_frame.place(relx=.5, rely=.5, anchor=tk.CENTER)

    def trigger_start(self):
        print('TRIGGER START')
        self.parent.ui_event('start_triggered')

    def hide(self):
        self.pack_forget()

    def show(self):
        self.pack(fill=tk.BOTH, expand=1)


class ProcessingScreen(tk.Frame, object):
    def __init__(self, master=None):
        super(ProcessingScreen, self).__init__(master)
        self.parent = master
        # self.pack(fill=tk.BOTH, expand=1)
        self.create_processing_screen()

    def create_processing_screen(self):
        print('CREATE PROCESSING SCREEN')
        content_frame = tk.LabelFrame(self, text="Pimaton is working...", background="ivory")
        content_frame.pack(fill=tk.BOTH, expand=1, padx=10, pady=10)

        # Load generated Gif
        file = '/home/bacardi55/Workspace/perso/testtmp' + '/' + 'to_print.gif'
        c = tk.Canvas(content_frame, height=250, width=300)
        c.create_image((0, 0), image=tk.PhotoImage(file))
        c.pack()

        # Progress Bar.
        self.progress_value = tk.IntVar()
        self.progress_value.set(0)
        progress_frame = tk.Frame(content_frame)
        progress_frame.pack(fill=tk.BOTH, expand=0, padx=20, pady=20, anchor=tk.CENTER)
        pb = ttk.Progressbar(progress_frame, variable=self.progress_value).pack(fill=tk.X,anchor=tk.CENTER)

        # Text.
        self.steptxt = tk.StringVar()
        self.steptxt.set("Step 1/4: Starting taking pictures...")
        tk.Label(progress_frame, textvariable=self.steptxt).pack()

    def hide(self):
        self.pack_forget()

    def show(self):
        self.pack(fill=tk.BOTH, expand=1)

    def set_progress_value(self, value=0):
        self.progress_value.set(value)

    def set_step_value(self, value=''):
        self.steptxt.set(value)

class ThankyouScreen(tk.Frame, object):
    def __init__(self, master=None):
        super(ThankyouScreen, self).__init__(master)
        self.parent = master
        self.create_thankyou_screen()

    def create_thankyou_screen(self):
        print('CREATE THANKYOU SCREEN')
        content_frame = tk.Frame(self)
        content_frame.pack(fill=tk.BOTH, expand=1, padx=10, pady=10)

        tk.Label(content_frame, text="Thank you for using Pimaton! Your photo is ready (or should be soon) :)").pack(fill=tk.BOTH)

    def hide(self):
        self.pack_forget()

    def show(self):
        self.pack(fill=tk.BOTH, expand=1)


class PimatonGUI(PimatonUI, object):
    def __init__(self, pimaton):
        super(PimatonGUI, self).__init__(pimaton)
        self.root = self.init_tk_root()
        self.app = self.init_tk_app(self.root)


    def init_tk_root(self):
        root = tk.Tk()
        root.attributes('-fullscreen', True)
        root.attributes('-topmost', True)

        return root

    def init_tk_app(self, root):
        app = PimatonGUIMain(master=root)
        app.master.title("Pimaton PhotoBooth")
        # app.master.geometry('640x480')

        return app

    def mainloop(self):
        self.app.mainloop()
