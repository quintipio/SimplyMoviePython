#!/usr/bin/env Python
# -*-coding:UTF-8 -*
from cx_Freeze import setup, Executable
import os
os.environ['TCL_LIBRARY'] = r'D:\Logiciel\Python\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'D:\Logiciel\Python\tcl\tk8.6'

setup(
    name="Simply Movie",
    version="0.6",
    description="Gestionnaire de bibliothèque de film",
    executables=[Executable("simplyMovie.py")],
)
