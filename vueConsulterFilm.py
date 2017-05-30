#!/usr/bin/env Python
# -*-coding:UTF-8 -*
import tkinter as tk
from models import type_recherche, init_database


class vueConsulterFilm(tk.Frame):
    """
        Class de la frame pour consulter un film
    """

    def __init__(self, parent, *args, **kwargs):
         tk.Frame.__init__(self, parent, *args, **kwargs)
         self.parent = parent