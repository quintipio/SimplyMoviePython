#!/usr/bin/env Python
# -*-coding:UTF-8 -*
import tkinter as tk
from models import type_recherche, type_film, get_liste_film, count_liste_film
from vueConsulterFilm import vueConsulterFilm

resultat_par_page = 10

class vuePrincipale(tk.Frame):
    """
        Module pour la fenêtre principale d'affichage des films
     """

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.page_en_cours = 1
        self.categorie = 0

        # liste des recherches disponibles
        self.liste_film_principale = tk.Listbox(self, selectmode=tk.SINGLE,height=5, exportselection=0)
        self.liste_film_principale.insert(0, "Film")
        self.liste_film_principale.insert(1, "Série")
        self.liste_film_principale.insert(2, "Documentaire")
        self.liste_film_principale.insert(3, "Spectacle")
        self.liste_film_principale.insert(4, "Animation")
        self.liste_film_principale.select_set(0)
        self.liste_vue_principale = tk.Listbox(self, selectmode=tk.SINGLE,height=5, exportselection=0)
        self.liste_vue_principale.insert(0, "A acheter")
        self.liste_vue_principale.insert(1, "A voir")
        self.liste_vue_principale.insert(2, "Ma collection")
        self.liste_vue_principale.insert(3, "En ce moment")
        self.liste_vue_principale.select_set(0)

        # frame des résultats initialisation
        self.frame_result = tk.Frame(self)

        # mise en place
        self.liste_film_principale.grid(row=0,column=0)
        self.liste_vue_principale.grid(row=0,column=1)
        self.frame_result.grid(row=1,column=0,columnspan=2)

        self.liste_vue_principale.bind('<<ListboxSelect>>', lambda ev : self.recherche_liste_film())
        self.liste_film_principale.bind('<<ListboxSelect>>', lambda ev : self.recherche_liste_film())
        self.recherche_liste_film()

    def recherche_liste_film(self):
        """
            recherche une liste de films selected_index indiquant le type de recherche à voir, acheter...)
        """
        selected_index = self.liste_vue_principale.curselection()[0]
        self.selected_film = self.liste_film_principale.curselection()[0]+1

        self.frame_result.destroy()
        self.frame_result = tk.Frame(self)

        if 1 is selected_index:
            self.categorie = type_recherche['A_VOIR']
            result = get_liste_film(type_recherche['A_VOIR'], self.selected_film, self.page_en_cours,resultat_par_page)
        elif 2 is selected_index:
            self.categorie = type_recherche['A_ACHETER']
            result = get_liste_film(type_recherche['A_ACHETER'], self.selected_film, self.page_en_cours,resultat_par_page)
        elif 3 is selected_index:
            self.categorie = 0
            result = get_liste_film(0,self.page_en_cours,resultat_par_page)
        
        if selected_index in [1,2,3] :
            i = 0
            for film in result:
                self.label_titre = tk.Label(self.frame_result, text=film.titre)
                self.label_annee = tk.Label(self.frame_result, text=film.annee)
                self.consulter_bouton = tk.Button(self.frame_result, text="Consulter", command=lambda arg=film.id: self.consulter_film(arg))

                self.label_titre.grid(row=i, column=0)
                self.label_annee.grid(row=i, column=1)
                self.consulter_bouton.grid(row=i, column=2)
                i += 1

            self.charger_pagination()
            self.frame_result.grid(row=1,column=0,columnspan=2)
    
    def charger_pagination(self) :
        """
            Charge les boutons de navigation de la pagination des résultats
        """
        compteur_film = count_liste_film(self.categorie,self.selected_film)
        page_max = compteur_film//resultat_par_page
        if compteur_film%resultat_par_page > 0 :
            page_max += 1
        self.frame_pagination = tk.Frame(self.frame_result)
        self.button_precedent = tk.Button(self.frame_pagination, text="Précédent", command=lambda: self.pagination_precedent())
        self.button_suivant = tk.Button(self.frame_pagination, text="Suivant", command=lambda: self.pagination_suivant())
        self.label_page_en_cours = tk.Label(self.frame_pagination,text='Page '+str(self.page_en_cours)+'/'+str(page_max)+'('+str(compteur_film)+' films)')

        if self.page_en_cours > 1 :
            self.button_precedent.pack(side=tk.LEFT,anchor=tk.W)
        
        if self.page_en_cours < page_max :
            self.button_suivant.pack(side=tk.RIGHT,anchor=tk.E)
        self.label_page_en_cours.pack()
        self.frame_pagination.grid(row=11,column=0,columnspan=3)

    def pagination_suivant(self):
        """
            Accès à la page suivante des résultats de films
        """
        self.page_en_cours += 1
        self.recherche_liste_film()

    def pagination_precedent(self):
        """
            Accès à la page précédente des résultats de films
        """
        self.page_en_cours -= 1 
        self.recherche_liste_film()

    def consulter_film(self, id_film):
        """
            Démarre la vue de consultation d'un film
        """
        self.consulter_film_fenetre = tk.Toplevel(self.parent)
        self.consulter_film_fenetre = vueConsulterFilm(self.consulter_film_fenetre, id_film=id_film,fenetre_appelante=self)
        self.consulter_film_fenetre.pack()
        

if __name__ == "__main__":
    vuePrincipaleFrame = tk.Tk()
    vuePrincipale(vuePrincipaleFrame).pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    vuePrincipaleFrame.mainloop()
