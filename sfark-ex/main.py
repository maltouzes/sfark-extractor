#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
# copyright 2016-2017 Tony Maillefaud <maltouzes@gmail.com>                   #
#                                                                             #
# This file is part of sfark-extractor                                        #
#                                                                             #
# sfark-extractor is free software: you can redistribute it and/or modify     #
# it under the terms of the GNU General Public License as published by        #
# the Free Software Foundation, either version 3 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# sfark-extractor is distributed in the hope that it will be useful,          #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with sfark-extractor. If not, see <http://www.gnu.org/licenses/>.     #
###############################################################################

"""sfark-extractor is a simple GUI sfArk decompressor to sf2, it convert
soundfonts in the legacy sfArk v2 file format to sf2."""

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import threading
import subprocess
from os.path import expanduser
import os


class SfarkConvertor():

    def fetch_sfark(self):
        filename = filedialog.askopenfilename(
            initialfile='file.sfArk',
            initialdir=expanduser("~"),
            filetypes=[('SFARK', '.sfArk'),
                       ('SFARK SF2', '.sf2'),
                       ('SFARK SF2', '.sfArk'),
                       ('ALL', '.*')])
        self._path_sfark.set(filename)
        if filename:
            self.myDict['sfarkfile'] = filename.split('/')[-1]
            self.myDict['path'] = os.path.dirname(filename)
            self.myDict['sf2file'] = (self.myDict['sfarkfile'].split('.')[-2] +
                                      ".sf2")
            self._status_msg.set(self.myDict['sfarkfile'] + " -> " +
                                 self.myDict['sf2file'])
        else:
            self._status_msg.set('Please choose a sfArk file')
            try:
                self.myDict.pop('sfarkfile')
            except KeyError:
                pass

    def convert_sfark(self):
        if ('sfarkfile' in self.myDict and
                self.myDict['sfarkfile'].endswith('sfArk')):
            self.pgr.grid(row=2)
            self.pgr.start()

            self.shell_cmd()
        else:
            self._status_msg.set('Please select a sfArk file')
            self._alert('Please select a sfArk file (*.sfArk)')

    def shell_cmd(self):

        exe = "cd " + (self.myDict['path']) + " && sfarkxtc " + (self.myDict['sfarkfile']) \
              + " " + (self.myDict['sf2file'])
        self.myDict['exe'] = exe
        self._convert_btn['state'] = 'disabled'
        thd = threading.Thread(target=self.convert_subprocess, args=(exe,))
        thd.start()
        # convert_subprocess(exe)

    def convert_subprocess(self, exe):
        try:
            self.p_exe = subprocess.Popen(["sfarkxtc",
                                          self.myDict['sfarkfile'],
                                          self.myDict['sf2file']],
                                          stdout=subprocess.PIPE,
                                          cwd=self.myDict['path'])
            self.p_exe.communicate()
            code_return = self.p_exe.returncode
            print(code_return)
            if "0" in str(code_return):
                self._convert_btn['state'] = 'normal'
                self._alert('Successful conversion')

            elif "1" in str(code_return):
                self._convert_btn['state'] = 'normal'
                self._alert('Conversion failed')
            else:
                pass

        except FileNotFoundError:
                self._status_msg.set('Please install sfArkxtc')
                self._alert('Please install sfArkxtc', _type="showError")
                self._convert_btn['state'] = 'normal'

        self.pgr.stop()
        self.pgr.grid_forget()

    def _alert(self, msg, _type="showInfo"):
        if _type == "showError":
            messagebox.showerror(message=msg)
        elif _type == "showWarning":
            messagebox.showwarning(message=msg)
        else:
            messagebox.showinfo(message=msg)

    def errorPrint(self, err):
        print("{0}: {1}".format(type(err), err))

    def _quit(self, event=None):
        try:
            self.p_exe.kill()
            self._convert_btn['state'] = 'normal'
            self._status_msg.set('operation canceled')
        except (ProcessLookupError, AttributeError):
            self._root.quit()
        # sys.exit(0)

    def __init__(self):
        self.p_exe = None
        self._root = Tk()
        self.myDict = {}
        help_text = "sfArk-extractor is an apps for converts soudfonts in the "\
            "legacy sfArk v2 file format to sf2\n\n"\
            "Only Linux is supported"
        about_text = "Developer:\n"\
            "Maltouzes <maltouzes@gmail.com>\n\n"\
            "Official Website:\n"\
            "http://github.com/maltouzes/sfark-extractor\n\n"\
            "Copyright \xa9 2016-2017 Tony Maillefaud"

        self._root.bind('<Escape>', self._quit)
        self._root.bind('<Control-q>', self._quit)
        try:
            icon_path = os.getcwd() + "/sfark-extractor.png"
            icon_sfark = PhotoImage(file=icon_path)
            self._root.tk.call("wm", "iconphoto",
                               self._root, "-default", icon_sfark)
        except TclError as tkerror:
            self.errorPrint(tkerror)

        self._root.title("sfArk Convertor")
        menubar = Menu(self._root)
        self._root.config(menu=menubar)
        menubar.add_command(label="Exit", command=self._quit)
        # function objects are required so we must use anonymous functions
        menubar.add_command(label="Help",
                            command=lambda: self._alert(help_text))
        menubar.add_command(label="About",
                            command=lambda: self._alert(about_text))

        _mainframe = ttk.Frame(self._root, padding='5 5 5 5')
        _mainframe.grid(row=0, column=0, sticky=(E, W, N, S))

        _path_frame = ttk.LabelFrame(
            _mainframe, text='Path to the sfArk file', padding='5 5 5 5')
        _path_frame.grid(row=0, column=0, sticky=(E, W))
        _path_frame.columnconfigure(0, weight=1)
        _path_frame.rowconfigure(0, weight=1)

        self._path_sfark = StringVar()
        self._path_sfark.set(expanduser("~"))
        _path_entry = ttk.Label(
            _path_frame, width=40, textvariable=self._path_sfark)
        _path_entry.grid(row=0, column=0, sticky=(E, W, S, N), padx=5)

        _fetch_btn = ttk.Button(
            _path_frame, text='Choose', command=self.fetch_sfark)
        _fetch_btn.grid(row=0, column=1, sticky=W, padx=5)

        _convert_frame = ttk.LabelFrame(
            _mainframe, text='Convert', padding='5 5 5 5')
        _convert_frame.grid(row=1, column=0, sticky=(E, W, S, N), padx=5)

        self._status_msg = StringVar()
        self._status_msg.set('Please choose a sfark file')

        _status = ttk.Label(
            _convert_frame, textvariable=self._status_msg, anchor=W)
        _status.grid(row=0, column=0, sticky=W, pady=5)

        self._convert_btn = ttk.Button(
            _mainframe, text='Convert', command=self.convert_sfark)
        self._convert_btn.grid(row=2, column=0, sticky=E, pady=5)

        self.pgr = ttk.Progressbar(_mainframe, orient=HORIZONTAL,
                                   length=200, mode='indeterminate')

        self._root.mainloop()

sfarkconvertor = SfarkConvertor()
