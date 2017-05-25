#!/usr/bin/env Python
# -*-coding:UTF-8 -*
import tkinter as tk
from vuePrincipale import vuePrincipale
from vueAjouterFilm import vueAjouterFilm
from models import init_database


class SimplyMovie:

    def __init__(self, master):
        self.master = master

        # menuBar
        self.menubar = tk.Menu(self)
        self.menu_fichier = tk.Menu(self.menubar, tearoff=0)
        self.menu_fichier.add_command(label="Quitter", command=self.fermer_appli)
        self.menu_film = tk.Menu(self.menubar, tearoff=0)
        self.menu_film.add_command(label="Ajouter un film", command=self.ajouter_film)
        self.menubar.add_cascade(label="Fichier", menu=self.menu_fichier)
        self.menubar.add_cascade(label="Film", menu=self.menu_film)

        # fenetre
        self.master.config(menu=self.menubar)
        self.frame_principale = vuePrincipale(self.master)
        self.frame_principale.pack(side="top")


    def ajouter_film(self):
        ajouter_film_fenetre = tk.Toplevel(self.master)
        ajouter_film_frame = vueAjouterFilm(ajouter_film_fenetre)
        ajouter_film_frame.pack()

    def fermer_appli(self):
        self.master.quit()


def main():
    init_database()
    fenetre_appli = tk.Tk()
    fenetre_appli.wm_title("Simply Movie")
    fenetre_appli.minsize(450, 300)
    app = SimplyMovie(fenetre_appli)
    fenetre_appli.mainloop()


if __name__ == '__main__':
    main()
