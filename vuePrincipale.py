#!/usr/bin/env Python
# -*-coding:UTF-8 -*
import tkinter as tk
from models import type_recherche, get_liste_film
from vueConsulterFilm import vueConsulterFilm


class vuePrincipale(tk.Frame):
     """
        Module pour la fenêtre principale d'affichage des films
     """
     def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        # panneau principale

        # liste des recherches disponibles
        self.liste_vue_principale = tk.Listbox(self,selectmode=tk.SINGLE)
        self.liste_vue_principale.insert(1, "En ce moment")
        self.liste_vue_principale.insert(2, "A acheter")
        self.liste_vue_principale.insert(3, "A voir")
        self.liste_vue_principale.insert(4, "Ma collection")
        self.liste_vue_principale.bind('<<ListboxSelect>>', lambda event: self.recherche_liste_film(event,self.liste_vue_principale.curselection()))

        # frame des résultats initialisation
        self.frame_result = tk.Frame(self)

        # mise en place
        self.liste_vue_principale.pack(side=tk.LEFT,anchor=tk.W)
        self.frame_result.pack(side=tk.LEFT)

     def recherche_liste_film(self, event,selected_index):
        """
            recherche une liste de films selected_index indiquant le type de recherche à voir, acheter...)
        """
        self.frame_result.destroy()
        self.frame_result = tk.Frame(self)
        
        if 2 in selected_index:
            result = get_liste_film(type_recherche['A_VOIR'])
        elif 3 in selected_index:
            result = get_liste_film(type_recherche['A_ACHETER'])
        
        i = 0
        for film in result :
           label_titre = tk.Label(self.frame_result, text=film.titre)
           label_annee = tk.Label(self.frame_result,text=film.annee)
           consulter_bouton = tk.Button(self.frame_result,text="Consulter",command=lambda:self.consulter_film(film.id))

           label_titre.grid(row=i,column=0)
           label_annee.grid(row=i,column=1)
           consulter_bouton.grid(row=i,column=2)
           i+=1

        self.frame_result.pack(side=tk.LEFT)
    

     def consulter_film(self,id_film):
         """
            Démarre la vue de consultation d'un film
         """
         self.consulter_film_fenetre = tk.Toplevel(self.parent)
         self.consulter_film_fenetre = vueConsulterFilm(self.consulter_film_fenetre)
         self.consulter_film_fenetre.pack()



if __name__ == "__main__":
    vuePrincipaleFrame = tk.Tk()
    vuePrincipale(vuePrincipaleFrame).pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    vuePrincipaleFrame.mainloop()
