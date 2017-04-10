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

myDict = {}


def fetch_sfark():
    filename = filedialog.askopenfilename(
        initialfile='file.sfArk',
        initialdir=expanduser("~"),
        filetypes=[('SFARK', '.sfArk'),
                   ('SFARK SF2', '.sf2'),
                   ('SFARK SF2', '.sfArk'),
                   ('ALL', '.*')])
    _path_sfark.set(filename)
    if filename:
        myDict['sfarkfile'] = filename.split('/')[-1]
        myDict['path'] = os.path.dirname(filename)
        myDict['sf2file'] = myDict['sfarkfile'].split('.')[-2] + ".sf2"
        _status_msg.set(myDict['sfarkfile'] + " -> " + myDict['sf2file'])
    else:
        _status_msg.set('Please choose a sfArk file')
        try:
            myDict.pop('sfarkfile')
        except KeyError:
            pass


def convert_sfark():
    if 'sfarkfile' in myDict and myDict['sfarkfile'].endswith('sfArk'):
        p.grid(row=2)
        p.start()

        shell_cmd()
    else:
        _status_msg.set('Please select a sfArk file')
        _alert('Please select a sfArk file')


def shell_cmd():

    exe = "cd " + (myDict['path']) + " && sfarkxtc " + (myDict['sfarkfile']) \
          + " " + (myDict['sf2file'])
    myDict['exe'] = exe
    _convert_btn['state'] = 'disabled'
    thd = threading.Thread(target=convert_subprocess, args=(exe,))
    thd.start()
    # convert_subprocess(exe)


def convert_subprocess(exe):
    p_exe = subprocess.Popen(["sfarkxtc", myDict['sfarkfile'],
                             myDict['sf2file']], stdout=subprocess.PIPE,
                             cwd=myDict['path'])
    p_exe.communicate()
    code_return = p_exe.returncode
    print(code_return)
    p.stop()
    p.grid_forget()
    if "0" in str(code_return):
        _convert_btn['state'] = 'normal'
        _alert('Successful conversion')

    elif "1" in str(code_return):
        _convert_btn['state'] = 'normal'
        _alert('Conversion failed')
    else:
        pass


def _alert(msg):
    messagebox.showinfo(message=msg)


def errorPrint(err):
    print("{0}: {1}".format(type(err), err))


def _quit(event=None):
    sys.exit(0)


if __name__ == "__main__":
    _root = Tk()
    help_text = "sfArk-extractor is an apps for converts soudfonts in the "\
        "legacy sfArk v2 file format to sf2\n\n"\
        "Only Linux is supported"
    about_text = "Developer:\n"\
        "Maltouzes <maltouzes@gmail.com>\n\n"\
        "Official Website:\n"\
        "http://github.com/maltouzes/sfark-extractor\n\n"\
        "Copyright \xa9 2016-2017 Tony Maillefaud"

    _root.bind('<Escape>', _quit)
    _root.bind('<Control-q>', _quit)
    try:
        icon_path = os.getcwd() + "/icon.png"
        icon_sfark = PhotoImage(file=icon_path)
        _root.tk.call("wm", "iconphoto", _root, "-default", icon_sfark)
    except TclError as tkerror:
        errorPrint(tkerror)

    _root.title("myApp")
    menubar = Menu(_root)
    _root.config(menu=menubar)
    menubar.add_command(label="Exit", command=_root.quit)
    # function objects are required so we must use anonymous functions
    menubar.add_command(label="Help", command=lambda: _alert(help_text))
    menubar.add_command(label="About", command=lambda: _alert(about_text))

    _mainframe = ttk.Frame(_root, padding='5 5 5 5')
    _mainframe.grid(row=0, column=0, sticky=(E, W, N, S))

    _path_frame = ttk.LabelFrame(
        _mainframe, text='Path to the sfArk file', padding='5 5 5 5')
    _path_frame.grid(row=0, column=0, sticky=(E, W))
    _path_frame.columnconfigure(0, weight=1)
    _path_frame.rowconfigure(0, weight=1)

    _path_sfark = StringVar()
    _path_sfark.set(expanduser("~"))
    _path_entry = ttk.Entry(
        _path_frame, width=40, textvariable=_path_sfark)
    _path_entry.grid(row=0, column=0, sticky=(E, W, S, N), padx=5)

    _fetch_btn = ttk.Button(
        _path_frame, text='Choose', command=fetch_sfark)
    _fetch_btn.grid(row=0, column=1, sticky=W, padx=5)

    _convert_frame = ttk.LabelFrame(
        _mainframe, text='Convert', padding='5 5 5 5')
    _convert_frame.grid(row=1, column=0, sticky=(E, W, S, N), padx=5)

    _status_msg = StringVar()
    _status_msg.set('Please choose a sfark file')

    _status = ttk.Label(
        _convert_frame, textvariable=_status_msg, anchor=W)
    _status.grid(row=0, column=0, sticky=W, pady=5)

    _convert_btn = ttk.Button(
        _mainframe, text='Convert', command=convert_sfark)
    _convert_btn.grid(row=2, column=0, sticky=E, pady=5)

    p = ttk.Progressbar(_mainframe, orient=HORIZONTAL,
                        length=200, mode='indeterminate')

    _root.mainloop()
