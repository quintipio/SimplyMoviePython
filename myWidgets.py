#!/usr/bin/env Python
# -*-coding:UTF-8 -*
import tkinter as tk
from PIL import Image, ImageTk
from resizeimage import resizeimage

class AfficheFilm(tk.Frame):

    def __init__(self, parent, affiche=None, titre="", *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        #img = resizeimage.resize_thumbnail(affiche, [400, 200])
        #canvas = tk.Canvas(self, borderwidth=2, relief=tk.GROOVE)
        #canvas.image = ImageTk.PhotoImage(img)
        #canvas.create_image(0, 0, image=canvas.image, anchor=tk.N)
        #canvas.pack()

        titre_label = tk.Label(self, text=titre)
        titre_label.pack(side=tk.TOP, anchor=tk.N)

        bouton_ajouter = tk.Button(self, text="Ajouter")
        bouton_ajouter.pack(side=tk.TOP, anchor=tk.N)
