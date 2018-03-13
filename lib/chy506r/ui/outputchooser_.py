# -*- coding: utf8 -*-
"""
"""

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox

__all__ = ('OutputChooser',)


class OutputChooser(object):
    def __init__(self, parent, **kw):

        self._parent = parent
        self._selection = ''
        self._button = tk.Button(parent, **self._button_options())
        self._label = tk.Label(parent, **self._label_options())
        self._selectcommand = kw.get('selectcommand', lambda: True )
        self._override = False

    def _button_options(self):
        return {'text': 'Output', 'command': self.select}

    def _label_options(self):
        return {'borderwidth': 1, 'relief': 'ridge', 'text': 'No file selected'}

    @property
    def button(self):
        return self._button

    @property
    def label(self):
        return self._label

    @property
    def parent(self):
        return self._parent

    @property
    def selection(self):
        return self._selection

    @selection.setter
    def selection(self, value):
        self._selection = value
        self._label['text'] = value or 'No file selected'
        self._selectcommand()

    @property
    def override(self):
        return self._override

    @override.setter
    def override(self, value):
        self._override = value

    def select(self):
        types = [('Comma Separated Values', '*.csv'), ('All files', '*')]
        config = {'parent': self.parent, 'defaultextension': '.csv', 'filetypes': types}
        if self._selection:
            config['initialfile'] = self._selection

        answer = filedialog.asksaveasfilename(**config)

        if answer and isinstance(answer, str):
            self.selection = answer
            self.override = True
        return answer


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
