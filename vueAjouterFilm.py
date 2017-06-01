#!/usr/bin/env Python
# -*-coding:UTF-8 -*
import tkinter as tk
from tkinter import messagebox
from models import type_film, ajouter_film, ajouter_film_basique
from myMovieDbConnector import get_data, search_db, get_affiche
from resizeimage import resizeimage
from PIL import Image, ImageTk


class vueAjouterFilm(tk.Frame):
    """
        Module pour la fenêtre de recherche et d'ajout de films par internet
    """
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        # frames des informations complémentaires
        self.frame_infos = tk.LabelFrame(self, text="Informations supplémentaires", padx=20, pady=20)
        self.frame_upper = tk.LabelFrame(self.frame_infos)
        self.frame_etat = tk.Frame(self.frame_upper, borderwidth=2, relief=tk.GROOVE)
        self.frame_type = tk.Frame(self.frame_upper, borderwidth=2, relief=tk.GROOVE)

        # checkbox à voir / à acheter 
        self.var_a_acheter = tk.BooleanVar()
        self.var_a_voir = tk.BooleanVar()
        self.checkbox_a_acheter =tk.Checkbutton(self.frame_etat, text="A acheter",onvalue=True,offvalue=False,variable=self.var_a_acheter)
        self.checkbox_a_voir = tk.Checkbutton(self.frame_etat, text="A voir",onvalue=True,offvalue=False,variable=self.var_a_voir)

        # type de film
        self.var = tk.IntVar(value=type_film['FILM'])
        self.radio_film = tk.Radiobutton(self.frame_type, text="Film", variable=self.var, value=type_film['FILM'])
        self.radio_serie = tk.Radiobutton(self.frame_type, text="Serie", variable=self.var, value=type_film['SERIE'])
        self.radio_docu = tk.Radiobutton(self.frame_type, text="Documentaire", variable=self.var, value=type_film['DOCUMENTAIRE'])
        self.radio_anim = tk.Radiobutton(self.frame_type, text="Animation", variable=self.var, value=type_film['ANIMATION'])
        self.radio_spectacle = tk.Radiobutton(self.frame_type, text="Spectacle ou concert", variable=self.var, value=type_film['SPECTACLE'])
        
        # textbox de recherche
        self.value_titre = tk.StringVar()
        self.entree_titre = tk.Entry(self.frame_infos, textvariable=self.value_titre, width=30)

        #bouton de recherche
        self.rechercher_bouton = tk.Button(self.frame_infos, text="Rechercher",command=self.lancer_recherche)

        #mise en place des éléments
        self.checkbox_a_acheter.pack(anchor=tk.W)
        self.checkbox_a_voir.pack(anchor=tk.W)
        self.radio_film.pack(anchor=tk.W)
        self.radio_serie.pack(anchor=tk.W)
        self.radio_docu.pack(anchor=tk.W)
        self.radio_anim.pack(anchor=tk.W)
        self.radio_spectacle.pack(anchor=tk.W)
        self.frame_etat.pack(expand="yes", side=tk.LEFT)
        self.frame_type.pack(expand="yes", side=tk.RIGHT)
        self.frame_upper.pack(expand="yes", side=tk.TOP)
        self.rechercher_bouton.pack(side=tk.BOTTOM)
        self.entree_titre.pack(expand="yes", side=tk.BOTTOM)
        self.frame_infos.pack(fill="both", expand="yes", side=tk.TOP)

        # éléments supplémentaires de la vue pas encore affiché
        self.frame_resulat = tk.Frame(self)
        self.liste_film = tk.Listbox(self.frame_resulat,width=30,height=10)
        self.frame_affiche_movie = tk.Frame(self.frame_resulat)

        # scrollbar liste_film
        self.scrollbar_liste = tk.Scrollbar(self.frame_resulat)
        self.scrollbar_liste.pack(side=tk.RIGHT,fill=tk.Y)
        self.liste_film.config(yscrollcommand=self.scrollbar_liste.set)
        self.scrollbar_liste.config(command=self.liste_film.yview)


    def lancer_recherche(self):
        """
            Action de recherche d'un film sur internet et affichage des résultats
        """
        self.liste_film.delete(0,tk.END)
        self.liste_resultat = get_data(search_db['SEARCH_TV'] if self.var.get() is type_film['SERIE'] else search_db['SEARCH_MOVIE'], self.value_titre.get())

        if len(self.liste_resultat) > 0:
            for result in self.liste_resultat:
                self.liste_film.insert(tk.END,result[1])

            self.liste_film.bind('<<ListboxSelect>>', lambda event: self.onselect_movie(event,self.liste_film.curselection()[0]))
            self.liste_film.pack(side=tk.LEFT, anchor=tk.W)
            self.frame_resulat.pack()
        else:
            result_question = messagebox.askquestion(title="Aucun résultat",message="Ce film est introuvable. Voulez vous quand même l'ajouter ?",icon="info")
            if result_question == 'yes' :
                ajouter_film_basique(titre=self.value_titre.get(),type=self.var.get(),a_acheter=self.var_a_acheter.get(),a_voir=self.var_a_voir.get())
                self.parent.destroy()
                
        

    def onselect_movie(self, evt,selected_index):
        """
            Action d'affichage d'un film avant d'ajouter le film en base avec selected_index l'emplacement du résultat dans la liste de résultats
        """
        self.frame_affiche_movie.destroy()
        self.frame_affiche_movie = tk.Frame(self.frame_resulat)
        data = self.liste_resultat[selected_index]
        img = ImageTk.PhotoImage(resizeimage.resize_thumbnail(get_affiche(data[0]), [400, 200]))
        self.bouton_ajouter = tk.Button(self.frame_affiche_movie,text="Ajouter à ma collection",command= lambda: self.ajouterFilm(data[2]))
        self.label = tk.Label(self.frame_affiche_movie,image=img)
        self.label.image = img
        self.label.pack(side=tk.TOP)
        self.frame_affiche_movie.pack(side=tk.RIGHT)
        self.bouton_ajouter.pack(side=tk.BOTTOM)

    def ajouterFilm(self,id):
        """
            Action d'ajout du film en base avec id, l'id du film à ajouter
        """
        film, casting, affiche = get_data(search_db['GET_TV'] if self.var.get() == type_film['SERIE'] else search_db['GET_MOVIE'],id)
        resultat = ajouter_film(film,casting,self.var.get(),self.var_a_voir.get(),self.var_a_acheter.get(),affiche)
        self.parent.destroy()
        if(resultat is not None) :
            messagebox.showerror(title="Erreur lors de l'ajout",message=resultat)


if __name__ == "__main__":
    vueAjouterFilmFrame = tk.Tk()
    vueAjouterFilm(vueAjouterFilmFrame).pack(side="top", fill="both", expand=True)
    vueAjouterFilmFrame.mainloop()

