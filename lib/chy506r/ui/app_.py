# -*- coding: utf8 -*-
"""
"""

import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import tkinter.ttk as ttk
import glob
import os
import threading

from .inputchooser_ import *
from .outputchooser_ import *
from ..api import *

__all__ = ('App',)

class _AppMeta(type):
    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        cls._tk = None
        cls._ui = None

    @property
    def tk(cls):
        if cls._tk is None:
            cls._tk = tk.Tk()
        return cls._tk

    @property
    def ui(cls):
        if cls._ui is None:
            cls._ui = cls(cls.tk)
        return cls._ui


class App(tk.Frame, metaclass=_AppMeta):
    def __init__(self, master):
        super().__init__(master)

        self._device = None
        self._gnuplot = None
        self._configure_master(master)
        self._create_widgets()
        self._set_layout()
        self._update_widgets()

    @property
    def tty(self):
        return self._input_chooser.selection

    @property
    def output(self):
        return self._output_chooser.selection

    def working(self):
        return self._device is not None and self._device.is_alive()

    def _configure_master(self, master):
        self.master.title("CHY 506R")
        self.master.protocol("WM_DELETE_WINDOW", self._closing)

    def _closing(self):
        self._stop_device()
        self._stop_gnuplot()
        self.master.destroy()

    def _create_widgets(self):
        self._input_chooser = InputChooser(self.master, selectcommand=self._select_input)
        self._output_chooser = OutputChooser(self.master, selectcommand=self._select_output)
        self._create_control_buttons()
        self._status_bar = tk.Label(self.master, text="Idle", bd=1, relief=tk.SUNKEN, anchor=tk.W)

    def _set_layout(self):
        self._input_chooser.label.grid(row=0, column=0, pady=4)
        self._input_chooser.combobox.grid(row=0, column=1, columnspan=3, sticky=tk.W+tk.E, pady=4)
        self._output_chooser.button.grid(row=1, column=0, pady=4)
        self._output_chooser.label.grid(row=1, column=1, columnspan=3, sticky=tk.W+tk.E, pady=4)
        self._start_button.grid(row=2, column=1, sticky=tk.W+tk.E, pady=4)
        self._stop_button.grid(row=2, column=2, sticky=tk.W+tk.E, pady=4)
        self._plot_button.grid(row=2, column=3, sticky=tk.W+tk.E, pady=4)
        self._status_bar.grid(row=3, column=0, columnspan=4, sticky=tk.W+tk.E)

    def _create_control_buttons(self):
        self._start_button = tk.Button(self.master, text='Start', state=tk.DISABLED, command=self._start_device)
        self._stop_button = tk.Button(self.master, text='Stop', state=tk.DISABLED, command=self._stop_device)
        self._plot_button = tk.Button(self.master, text='Plot', state=tk.DISABLED, command=self._toggle_gnuplot)

    def _start_device(self):
        if os.path.exists(self.output) and not self._output_chooser.override:
            answer = self._output_chooser.select()  # try to not override existing file
            if not answer:
                return
        self._output_chooser.override = False
        self._device = Chy506R(self.tty, self.output)
        self._device.start()
        self._update_widgets()
        self.master.after(250, self._watch_device)

    def _stop_device(self):
        if self.working():
            self._device.stop()
            self._device.join()
            self._device = None
        self._update_widgets()

    def _start_gnuplot(self):
        self._gnuplot = Gnuplot(self.output)
        self._gnuplot.start()
        self._update_widgets()

    def _stop_gnuplot(self):
        if self._gnuplot is not None:
            self._gnuplot.terminate()
            self._gnuplot = None
            self._update_widgets()

    def _toggle_gnuplot(self):
        if self._gnuplot is None:
            self._start_gnuplot()
        else:
            self._stop_gnuplot()

    def _watch_device(self):
        self._update_widgets()
        if self.working():
            self.master.after(250, self._watch_device)
        else:
            if self._device is not None and not self._device.done:
                messagebox.showwarning("Warning", "Measurements aborted. " +
                                       "It looks like a timeout occurred. " +
                                       "Did you connect the device to PC?")

    def _update_widgets(self):
        working = self.working()
        start = self.tty and self.output and not working
        stop = working
        plot = working and self._device.count >= 2 or self._gnuplot is not None and self._gnuplot.poll() is None
        self._start_button['state'] = tk.NORMAL if start else tk.DISABLED
        self._stop_button['state'] = tk.NORMAL if stop else tk.DISABLED
        self._plot_button['state'] = tk.NORMAL if plot else tk.DISABLED
        self._status_bar['text'] = "Measurements in progress..." if working else "Idle"

    def _select_input(self):
        self._update_widgets()

    def _select_output(self):
        self._update_widgets()


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
