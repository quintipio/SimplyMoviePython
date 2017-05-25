#!/usr/bin/env Python
# -*-coding:UTF-8 -*
import tkinter as tk
from models import type_film,ajouter_film
from myMovieDbConnector import get_data, search_db
from resizeimage import resizeimage
from PIL import Image, ImageTk


class vueAjouterFilm(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        #tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # frames des informations complémentaires
        frame_infos = tk.LabelFrame(self, text="Informations supplémentaires", padx=20, pady=20)
        frame_upper = tk.LabelFrame(frame_infos)
        frame_etat = tk.Frame(frame_upper, borderwidth=2, relief=tk.GROOVE)
        frame_type = tk.Frame(frame_upper, borderwidth=2, relief=tk.GROOVE)

        self.checkbox_a_acheter =tk.Checkbutton(frame_etat, text="A acheter")
        self.checkbox_a_voir = tk.Checkbutton(frame_etat, text="A voir")

        self.var = tk.IntVar()
        radio_film = tk.Radiobutton(frame_type, text="Film", variable=self.var, value=type_film['FILM'])
        radio_serie = tk.Radiobutton(frame_type, text="Serie", variable=self.var, value=type_film['SERIE'])
        radio_docu = tk.Radiobutton(frame_type, text="Documentaire", variable=self.var, value=type_film['DOCUMENTAIRE'])
        radio_anim = tk.Radiobutton(frame_type, text="Animation", variable=self.var, value=type_film['ANIMATION'])
        radio_spectacle = tk.Radiobutton(frame_type, text="Spectacle ou concert", variable=self.var, value=type_film['SPECTACLE'])

        self.value_titre = tk.StringVar(value="interstellar")
        entree_titre = tk.Entry(frame_infos, textvariable=self.value_titre, width=30)

        self.rechercher_bouton = tk.Button(frame_infos, text="Rechercher",command=self.lancer_recherche)

        self.checkbox_a_acheter.pack(anchor=tk.W)
        self.checkbox_a_voir.pack(anchor=tk.W)
        radio_film.pack(anchor=tk.W)
        radio_serie.pack(anchor=tk.W)
        radio_docu.pack(anchor=tk.W)
        radio_anim.pack(anchor=tk.W)
        radio_spectacle.pack(anchor=tk.W)
        frame_etat.pack(expand="yes", side=tk.LEFT)
        frame_type.pack(expand="yes", side=tk.RIGHT)
        frame_upper.pack(expand="yes", side=tk.TOP)
        self.rechercher_bouton.pack(side=tk.BOTTOM)
        entree_titre.pack(expand="yes", side=tk.BOTTOM)
        frame_infos.pack(fill="both", expand="yes", side=tk.TOP)

        self.frame_resulat = tk.Frame()
        self.liste_film = tk.Listbox(self.frame_resulat)
        self.frame_affiche_movie = tk.Frame(self.frame_resulat)

    def lancer_recherche(self):
        self.liste_film.delete(0,tk.END)
        self.liste_resultat = get_data(search_db['SEARCH_TV'] if self.var.get == type_film['SERIE'] else search_db['SEARCH_MOVIE'], self.value_titre.get())
        if len(self.liste_resultat):
            for result in self.liste_resultat:
                self.liste_film.insert(tk.END,result[1])

            self.liste_film.bind('<<ListboxSelect>>', lambda event: self.onselect_movie(event,self.liste_film.curselection()[0]))
            self.liste_film.pack(side=tk.LEFT, anchor=tk.W)
            self.frame_resulat.pack()

    def onselect_movie(self, evt,selected_index):
        self.frame_affiche_movie.destroy()
        self.frame_affiche_movie = tk.Frame(self.frame_resulat)

        data = self.liste_resultat[selected_index]
        img = ImageTk.PhotoImage(resizeimage.resize_thumbnail(data[0], [400, 200]))

        bouton_ajouter = tk.Button(self.frame_affiche_movie,text="Ajouter à ma collection")
        bouton_ajouter.bind("<Button-1>", lambda event : self.ajouterFilm(event,data[2]))
        label = tk.Label(self.frame_affiche_movie,image=img)
        label.image = img
        label.pack(side=tk.TOP)
        self.frame_affiche_movie.pack(side=tk.RIGHT)
        bouton_ajouter.pack(side=tk.BOTTOM)

    def ajouterFilm(self,event,id):
        film, casting, affiche = get_data(search_db['GET_TV'] if self.var.get == type_film['SERIE'] else search_db['GET_MOVIE'],id)
        ajouter_film(film,casting,self.var.get,True,False,affiche)
        return None


if __name__ == "__main__":
    vueAjouterFilmFrame = tk.Tk()
    vueAjouterFilm(vueAjouterFilmFrame).pack(side="top", fill="both", expand=True)
    vueAjouterFilmFrame.mainloop()

