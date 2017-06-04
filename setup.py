#!/usr/bin/env Python
# -*-coding:UTF-8 -*
from cx_Freeze import setup, Executable
import os
import sys

os.environ['TCL_LIBRARY'] = r'D:\Logiciel\Python\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'D:\Logiciel\Python\tcl\tk8.6'

base = None
if sys.platform == "win32":
    base = "Win32GUI"
    # base = "console"

build_exe_options = {"packages": ["tkinter","resizeimage", "pony.orm", "os", "io", "urllib", "requests", "PIL", "json",
                                    "models", "myMovieDbConnector", "vueAjouterFilm", "vueConsulterFilm", "vuePrincipale"],
                     "excludes": ["PyQt5","pyqt5-tools"],
                     "includes": [],
                     "include_files": ["afficheDefaut.jpg",
                                       r"D:\Logiciel\Python\DLLs\tcl86t.dll",
                                       r"D:\Logiciel\Python\DLLs\tk86t.dll",]
                     }

setup(
    name="Simply Movie",
    version="1.0",
    description="Gestionnaire de bibliothèque de film",
    executables=[Executable("simplyMovie.py",
                            base=base,
                            icon="icone.ico")],
    options={"build_exe": build_exe_options}
)
