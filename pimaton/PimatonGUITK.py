import Tkinter as tk
import ttk as ttk
import tkFont as tkf

import datetime
import time
import logging
import math

from PIL import Image, ImageTk

logging.basicConfig()
logger = logging.getLogger("Pimaton")


class PimatonGUITK(tk.Frame, object):
    def __init__(self, master=None, pimaton=None):
        super(PimatonGUITK, self).__init__(master)
        self.trigger_locked = True
        self.cptr = 0
        self.start_time = datetime.datetime.now()
        self.pimaton = pimaton
        self.config = self.pimaton.config['gui']
        self.parent = master

        self.pack(fill=tk.BOTH, expand=1)

        self.nb_steps = self.get_step_number()
        logger.debug('** GUI ** Number of steps: %s' % self.nb_steps)
        self.progress_inc = int(100) / self.nb_steps
        logger.debug('** GUI ** Progress_inc = %s' % self.progress_inc)
        self.current_step = 0

        self.set_fonts()
        self.initialize_ui()

    def set_fonts(self):
        self.fonts = {
            'small': tkf.Font(size=6),
            'normal': tkf.Font(size=8),
            'normalbold': tkf.Font(size=8, weight="bold"),
            'large': tkf.Font(size=18, weight="bold")
        }

    def initialize_ui(self):
        logger.debug('** GUI ** INIT UI')
        # Bootstrap UI layout.
        self.ui = {
            'header': self.create_header(),
            'footer': self.create_footer(),
            'screens': {
                'waiting': WaitingScreen(
                    self,
                    self.config,
                    self.pimaton.config['pimaton']['inputs']),
                'processing': ProcessingScreen(self),
                'thanking': ThankyouScreen(
                    self,
                    self.config)}}
        logger.debug('** GUI ** All screens have been initiated')

        # Show waiting screen to start with.
        self.ui['screens']['waiting'].show()
        self.trigger_locked = False

    def create_header(self):
        logger.debug('** GUI ** Create gui header area')
        header_frame = tk.Frame(self, height=1000)
        header_frame.pack(expand=0, fill=tk.X, side=tk.TOP, padx=10, pady=10)

        self.current_time = datetime.datetime.now().strftime('%H:%M')
        self.clock = tk.Label(
            header_frame,
            text=self.current_time,
            font=self.fonts['normal'])
        self.clock.pack(side=tk.LEFT, anchor="nw")
        self.stats = tk.Label(
            header_frame,
            text=self.get_stats_text(),
            font=self.fonts['small'])
        self.stats.pack(side=tk.RIGHT, anchor="ne")
        tk.Label(
            header_frame,
            text=self.config['header_message'],
            font=self.fonts['normalbold']).pack(
            side=tk.TOP)

        return header_frame

    def create_footer(self):
        logger.debug('** GUI ** Create gui footer area')
        footer_frame = tk.Frame(self)
        footer_frame.pack(
            expand=0,
            fill=tk.X,
            side=tk.BOTTOM,
            padx=10,
            pady=10)
        tk.Label(
            footer_frame,
            text=self.config['footer_message'],
            font=self.fonts['normal']).pack(
            anchor=tk.CENTER)

        return footer_frame

    def set_clock(self):
        self.current_time = datetime.datetime.now().strftime('%H:%M')
        self.clock.config(text=self.current_time)
        self.clock.after(30000, self.set_clock)

    def set_stats_area(self):
        self.stats.config(text=self.get_stats_text())
        self.stats.after(30000, self.set_stats_area)

    def start_triggered(self):
        logger.debug('Start has been triggered')
        if self.trigger_locked is True:
            logger.debug('Trigger is locked, please retry later')
            return

        self.trigger_locked = True
        # Start process screen
        self.init_processing_screen()
        self.run_pimaton()
        self.ui['screens']['processing'].clean_process_screen()
        self.switch_to_thanking_screen()

        time.sleep(self.config['time_between_thankyou_and_waiting'])
        self.switch_to_waiting_screen()

    def run_pimaton(self):
        # Reset current step.
        self.current_step = 1
        unique_key = self.pimaton.get_unique_key()
        time.sleep(self.config['time_between_steps'])
        taken_pictures = self.pimaton.take_pictures(unique_key)

        # After run, you got the generated file.
        # Place an image on the screen.
        self.ui['screens']['processing'].set_canvas_image(
            taken_pictures[self.current_step - 1])
        # Update progress on statusbar.
        self.ui['screens']['processing'].set_progress_value(
            self.current_step * self.progress_inc)
        # Update progress on statusbar text.
        self.ui['screens']['processing'].set_step_value(
            'Step ' + str(self.current_step) + '/' + str(self.nb_steps) + ': Generating picture to print')
        self.update_idletasks()

        filename = self.pimaton.get_filename(unique_key)
        to_print = self.pimaton.generate_picture(taken_pictures, filename)
        self.current_step = self.current_step + 1

        time.sleep(self.config['time_between_steps'])

        if self.pimaton.is_print_enabled() is True:
            self.ui['screens']['processing'].set_canvas_image(
                taken_pictures[self.current_step - 1])
            self.ui['screens']['processing'].set_progress_value(
                self.current_step * self.progress_inc)
            self.ui['screens']['processing'].set_step_value(
                'Step ' + str(self.current_step) + '/' + str(self.nb_steps) + ': Sending picture to printer')
            self.update_idletasks()
            self.pimaton.print_picture(to_print)
            self.current_step = self.current_step + 1

        time.sleep(self.config['time_between_steps'])

        # TODO v0.0.5: Sync picture to the internet.
        if self.pimaton.is_sync_enabled():
            self.ui['screens']['processing'].set_canvas_image(
                taken_pictures[self.current_step - 1])
            self.ui['screens']['processing'].set_progress_value(
                self.current_step * self.progress_inc)
            self.ui['screens']['processing'].set_step_value(
                'Step ' + str(self.current_step) + '/' + str(self.nb_steps) + ': Syncing picture to the internet')
            self.update_idletasks()
            self.current_step = self.current_step + 1

        time.sleep(self.config['time_between_steps'])

        # Finished!
        self.ui['screens']['processing'].set_canvas_image(
            taken_pictures[self.current_step - 1])
        self.ui['screens']['processing'].set_progress_value(100)
        self.ui['screens']['processing'].set_step_value(
            'Pimaton process is done!')
        self.update_idletasks()

        time.sleep(self.config['time_between_steps'])

        # unlock process
        self.cptr = self.cptr + 1
        self.trigger_locked = False

    def init_processing_screen(self):
        # Show progress screen.
        self.ui['screens']['waiting'].hide()
        self.ui['screens']['processing'].show()

        # Update step progress and text.
        self.ui['screens']['processing'].set_progress_value(
            self.progress_inc * self.current_step)
        self.ui['screens']['processing'].steptxt.set(
            "Step 1/" + str(self.nb_steps) + ": Starting taking pictures...")

        self.current_step = self.current_step + 1
        self.update_idletasks()

    def get_step_number(self):
        # Minimum number is 2: taking picture and generating finale image.
        step = 2
        if self.pimaton.is_print_enabled():
            step = step + 1
        if self.pimaton.is_sync_enabled():
            step = step + 1

        return step

    def switch_to_thanking_screen(self):
        self.ui['screens']['processing'].hide()
        self.ui['screens']['thanking'].show()
        self.update_idletasks()

    def switch_to_waiting_screen(self):
        self.ui['screens']['thanking'].hide()
        self.ui['screens']['waiting'].show()
        self.update_idletasks()

    def get_stats_text(self):
        text = 'Taken pictues: ' + \
            str(self.cptr * int(self.pimaton.config['picamera']['number_of_pictures_to_take'])) + \
            "\nSince: "

        minutes = int(
            math.floor(
                (datetime.datetime.now() -
                 self.start_time).seconds /
                60))
        if minutes > 59:
            hours = int(math.floor(minutes / 60))
            minutes = minutes % 60
            text = text + str(hours) + ' h' + str(minutes) + ' m'
        else:
            text = text + str(minutes) + 'min'

        return text

    def mainloop(self):
        self.set_clock()
        self.set_stats_area()
        super(PimatonGUITK, self).mainloop()


class WaitingScreen(tk.Frame, object):
    def __init__(self, master=None, config=None, inputs=[]):
        super(WaitingScreen, self).__init__(master)
        self.parent = master
        self.create_waiting_screen(config['start_btn_txt'], inputs)

    def create_waiting_screen(self, start_btn_txt="", inputs=[]):
        logger.debug('** GUI ** Create waiting screen')
        content_frame = tk.Frame(self)
        content_frame.pack(fill=tk.BOTH, expand=1, padx=10, pady=10)
        button_frame = tk.Frame(content_frame, borderwidth=2)

        if 'gui' in inputs:
            tk.Button(
                button_frame,
                text=start_btn_txt,
                font=self.parent.fonts['large'],
                command=self.start_triggered).pack(
                anchor=tk.CENTER)
        else:
            tk.Label(
                button_frame,
                font=self.parent.fonts['large'],
                text=start_btn_txt).pack(
                anchor=tk.CENTER)

        button_frame.place(relx=.5, rely=.5, anchor=tk.CENTER)

    def start_triggered(self):
        logger.debug('** GUI ** Start has been triggered')
        self.parent.start_triggered()

    def hide(self):
        self.pack_forget()

    def show(self):
        self.pack(fill=tk.BOTH, expand=1)


class ProcessingScreen(tk.Frame, object):
    def __init__(self, master=None):
        super(ProcessingScreen, self).__init__(master)
        self.parent = master
        self.size = (512, 384)
        self.create_processing_screen()

    def create_processing_screen(self):
        logger.debug('** GUI ** Create gui processing screen')
        content_frame = tk.LabelFrame(self, text="Pimaton is working...")
        content_frame.pack(fill=tk.BOTH, expand=1, padx=10, pady=10)

        # Progress Bar.
        self.progress_value = tk.IntVar()
        self.progress_value.set(0)
        progress_frame = tk.Frame(content_frame)
        progress_frame.pack(
            fill=tk.BOTH,
            expand=0,
            padx=20,
            pady=20,
            anchor=tk.CENTER,
            side=tk.BOTTOM)
        ttk.Progressbar(
            progress_frame,
            variable=self.progress_value).pack(
            fill=tk.X,
            anchor=tk.CENTER)

        # Text.
        self.steptxt = tk.StringVar()
        self.steptxt.set("Step 0/" +
                         str(self.parent.nb_steps) +
                         ": Waiting to start...")
        tk.Label(progress_frame, textvariable=self.steptxt,
                 font=self.parent.fonts['normal']).pack()

        # Canvas to display taken pictures.
        self.canvas = tk.Canvas(content_frame, height=384, width=512)
        self.init_canvas_image()
        self.canvas.pack(side=tk.TOP)

    def hide(self):
        self.pack_forget()

    def show(self):
        self.pack(fill=tk.BOTH, expand=1)

    def set_progress_value(self, value=0):
        self.progress_value.set(value)

    def set_step_value(self, value=''):
        self.steptxt.set(value)

    def init_canvas_image(self):
        pilimage = Image.new('RGB', self.size, 'white')
        self.image = ImageTk.PhotoImage(pilimage)
        self.imagesprite = self.canvas.create_image(250, 100, image=self.image)

    def set_canvas_image(self, filename):
        filename_path = self.parent.pimaton.config['picamera']['photo_directory'] + '/' + filename
        pilimage = Image.open(filename_path)
        pilimage.thumbnail(self.size)
        new_image = ImageTk.PhotoImage(pilimage)
        self.imagesprite = self.canvas.create_image(250, 100, image=new_image)
        self.canvas.itemconfig(self.image, image=new_image)
        self.image = new_image

    def clean_process_screen(self):
        self.set_progress_value(0)
        self.set_step_value('Step 0 /' +
                            str(self.parent.nb_steps) +
                            ': Waiting to start')


class ThankyouScreen(tk.Frame, object):
    def __init__(self, master=None, config=None):
        super(ThankyouScreen, self).__init__(master)
        self.parent = master
        self.config = config
        self.create_thankyou_screen(config['thankyou_message'])

    def create_thankyou_screen(self, thankyou_message):
        logger.debug('** GUI ** Create thankyou screen')
        content_frame = tk.Frame(self)
        content_frame.pack(fill=tk.BOTH, expand=1, padx=10, pady=10)

        tk.Label(
            content_frame,
            text=thankyou_message,
            font=self.parent.fonts['large']).pack(
            fill=tk.BOTH)

    def hide(self):
        self.pack_forget()

    def show(self):
        self.pack(fill=tk.BOTH, expand=1)
