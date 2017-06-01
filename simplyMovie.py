#!/usr/bin/env Python
# -*-coding:UTF-8 -*
import tkinter as tk
from vuePrincipale import vuePrincipale
from vueAjouterFilm import vueAjouterFilm
from models import init_database


class SimplyMovie:
    """
        Classe principale de l'application
    """
    def __init__(self, master):
        self.master = master

        # menuBar
        self.menubar = tk.Menu(self.master)
        self.menu_fichier = tk.Menu(self.menubar, tearoff=0)
        self.menu_fichier.add_command(label="Quitter", command=self.fermer_appli)
        self.menu_film = tk.Menu(self.menubar, tearoff=0)
        self.menu_film.add_command(label="Ajouter un film", command=self.ajouter_film)
        self.menubar.add_cascade(label="Fichier", menu=self.menu_fichier)
        self.menubar.add_cascade(label="Film", menu=self.menu_film)

        # fenetre
        self.master.config(menu=self.menubar)
        self.frame_principale = vuePrincipale(self.master,width=600,height=320)
        self.frame_principale.pack()

    def ajouter_film(self):
        """
            Démarre la vue pour ajouter un film à partir d'une recherche internet
        """
        self.ajouter_film_fenetre = tk.Toplevel(self.master)
        self.ajouter_film_frame = vueAjouterFilm(self.ajouter_film_fenetre)
        self.ajouter_film_frame.pack()

    def fermer_appli(self):
        """
            Ferme l'application
        """
        self.master.quit()


def main():
    """
        Méthode de démarrage de l'application
    """
    init_database()
    root = tk.Tk()
    root.wm_title("Simply Movie")
    root.minsize(300, 300)
    app = SimplyMovie(root)
    root.mainloop()


if __name__ == '__main__':
    main()
