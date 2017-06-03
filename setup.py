#!/usr/bin/env Python
# -*-coding:UTF-8 -*
from cx_Freeze import setup, Executable

setup(
    name="Simply Movie",
    version="0.6",
    description="Gestionnaire de bibliothèque de film",
    executables = [Executable("simplyMovie.py")],
)