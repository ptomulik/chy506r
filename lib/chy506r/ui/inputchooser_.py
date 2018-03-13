# -*- coding: utf8 -*-
"""
"""

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
import glob
import os
import pathlib

__all__ = ('InputChooser',)


class InputChooser(object):
    def __init__(self, parent, **kw):

        self._parent = parent
        self._selection = ''
        self._label = tk.Label(parent, **self._label_options())
        self._combobox = ttk.Combobox(parent, **self._combo_options(parent))
        self._selectcommand = kw.get('selectcommand', lambda: True )

    def _label_options(self):
        return {'text': 'Input'}

    def _combo_options(self, parent):
        validate = parent.register(self._validate)
        invalid = parent.register(self._invalid)
        return {'postcommand': self._generate_values,
                'validate': 'focus',
                'validatecommand': (validate, '%V', '%P'),
                'invalidcommand': (invalid, '%P')}

    def _validate(self, reason, value):
        if value :
            if not pathlib.Path(value).is_char_device():
                messagebox.showerror("Invalid path", ("%s is not a character" +
                                     " device") % repr(value))
                return False
            with open(value, 'r') as fr, open(value, 'w') as fw:
                if not fr.isatty() or not fw.isatty():
                    messagebox.showerror("Invalid path", "%s is not a TTY"
                                         % repr(value))
                    return False

        self._selection = self.combobox.get()
        self._selectcommand()
        return True

    def _invalid(self, value):
        self.combobox.set(self.selection)

    def _generate_values(self):
        serials = glob.glob('/dev/serial/by-id/*')
        values = [os.path.realpath(f) for f in serials]
        self.combobox['values'] = values

    @property
    def label(self):
        return self._label

    @property
    def combobox(self):
        return self._combobox

    @property
    def parent(self):
        return self._parent

    @property
    def selection(self):
        return self._selection

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
