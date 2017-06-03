#!/usr/bin/env Python
# -*-coding:UTF-8 -*
import tkinter as tk
from models import type_recherche, get_liste_film, count_liste_film, type_film
from myMovieDbConnector import get_search_general, search_db
from vueConsulterFilm import vueConsulterFilm, mode_consultation

resultat_par_page = 20


class vuePrincipale(tk.Frame):
    """
        Module pour la fenêtre principale d'affichage des films
     """

    def __init__(self, parent, *args, **kwargs):
        """
        Initialisation de frame de la vue principale
        :param parent: object parent
        :param args: arguments de la frame
        :param kwargs: arguments de la frame
        """
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.page_en_cours = 1
        # recherche principale
        self.frame_champ_recherche = tk.Frame(self)
        self.var_recherche = tk.StringVar()
        self.recherche_entry = tk.Entry(self.frame_champ_recherche, textvariable=self.var_recherche, width=30)
        self.button_recherche = tk.Button(self.frame_champ_recherche, text="Rechercher",
                                          command=lambda: self.lancer_recherche_general())
        self.recherche_entry.pack(side=tk.LEFT)
        self.button_recherche.pack(side=tk.RIGHT)

        # liste des recherches disponibles
        self.liste_film_principale = tk.Listbox(self, selectmode=tk.SINGLE, height=5, exportselection=0)
        self.liste_film_principale.insert(0, "Film")
        self.liste_film_principale.insert(1, "Série")
        self.liste_film_principale.insert(2, "Documentaire")
        self.liste_film_principale.insert(3, "Spectacle")
        self.liste_film_principale.insert(4, "Animation")
        self.liste_film_principale.select_set(0)
        self.liste_vue_principale = tk.Listbox(self, selectmode=tk.SINGLE, height=5, exportselection=0)
        self.liste_vue_principale.insert(0, "A acheter")
        self.liste_vue_principale.insert(1, "A voir")
        self.liste_vue_principale.insert(2, "Ma collection")
        self.liste_vue_principale.insert(3, "En ce moment")
        self.liste_vue_principale.insert(4, "Populaire")
        self.liste_vue_principale.select_set(0)

        # frame des résultats initialisation
        self.frame_result = tk.Frame(self)
        self.frame_pagination = tk.Frame(self.frame_result)
        self.button_precedent = tk.Button(self.frame_pagination)
        self.button_suivant = tk.Button(self.frame_pagination)
        self.label_page_en_cours = tk.Label(self.frame_pagination)

        # mise en place
        self.frame_champ_recherche.grid(row=0,column=0,columnspan=2)
        self.liste_film_principale.grid(row=1, column=0)
        self.liste_vue_principale.grid(row=1, column=1)
        self.frame_result.grid(row=2, column=0, columnspan=2)

        self.liste_vue_principale.bind('<<ListboxSelect>>', lambda ev: self.event_for_recherche())
        self.liste_film_principale.bind('<<ListboxSelect>>', lambda ev: self.event_for_recherche())
        self.recherche_liste_film()

    def lancer_recherche_general(self):
        """
        Lance une recherche générale sur les séries et films
        """
        results = get_search_general(search_db['GENERAL_SEARCH'], self.page_en_cours, query=self.var_recherche.get())
        self.charger_resultats(results, results['total_results'], results['total_pages'], mode_consultation['INTERNET'], type=None)

    def event_for_recherche(self):
        """
        Réinitialise une nouvelle recherche
        """
        self.page_en_cours = 1
        self.recherche_liste_film()

    def recherche_liste_film(self):
        """
            recherche une liste de films selected_index indiquant le type de recherche à voir, acheter...)
        """
        selected_index = self.liste_vue_principale.curselection()[0]
        selected_film = self.liste_film_principale.curselection()[0] + 1

        # en base de donnée
        if selected_index in [0, 1, 2]:
            if 1 is selected_index:
                categorie = type_recherche['A_VOIR']
                result = get_liste_film(type_recherche['A_VOIR'], selected_film, self.page_en_cours,
                                        resultat_par_page)
            elif 0 is selected_index:
                categorie = type_recherche['A_ACHETER']
                result = get_liste_film(type_recherche['A_ACHETER'], selected_film, self.page_en_cours,
                                        resultat_par_page)
            elif 2 is selected_index:
                categorie = 0
                result = get_liste_film(0,selected_film, self.page_en_cours, resultat_par_page)

            nombre_resultats = count_liste_film(categorie, selected_film)
            nombre_page = nombre_resultats // resultat_par_page
            if nombre_resultats % resultat_par_page > 0:
                nombre_page += 1
            mode = mode_consultation['LOCAL']

        # sur my movie DB
        if selected_index in [3, 4]:
            if selected_index is 3:
                if selected_film is type_film['SERIE']:
                    result = get_search_general(search_db['MOMENT_TV'], self.page_en_cours)
                else:
                    result = get_search_general(search_db['MOMENT_MOVIE'], self.page_en_cours)

            if selected_index is 4:
                if selected_film is type_film['SERIE']:
                    result = get_search_general(search_db['POPULAR_TV'], self.page_en_cours)
                else:
                    result = get_search_general(search_db['POPULAR_MOVIE'], self.page_en_cours)
            nombre_resultats = result['total_results']
            nombre_page = result['total_pages']
            mode = mode_consultation['INTERNET']

        self.charger_resultats(result, nombre_resultats, nombre_page, mode, selected_film)

    def charger_resultats(self, result, nombre_resultat, nombre_page, mode, type):
        """
            Charge les boutons de navigation de la pagination des résultats et les résultats
            :param result: les résultats à afficher
            :param nombre_resultat: le nombre de résultats total
            :param mode: le mode de consultation de la fenêtre (internet ou local)
            :param type: le type de films (série,films...)
        """
        # on efface la frame des résultats
        self.frame_result.destroy()
        self.frame_result = tk.Frame(self)
        self.frame_result.grid(row=2, column=0, columnspan=2)

        # mise en place des nouveaux résultats
        i = 0
        for film in (result if mode is mode_consultation['LOCAL'] else result['results']):
            if type is None:
                if 'media_type' in film and film['media_type'] == 'tv':
                    type_consult = type_film['SERIE']
                elif 'media_type' in film and film['media_type'] == 'movie':
                    type_consult = type_film['FILM']
            else:
                type_consult = type
            if mode is mode_consultation['LOCAL']:
                label_titre = tk.Label(self.frame_result, text=film.titre)
                label_annee = tk.Label(self.frame_result, text=film.annee)
                consulter_bouton = tk.Button(self.frame_result, text="Consulter",
                                             command=lambda arg=(film.id, type_consult, mode_consultation['LOCAL']):
                                             self.consulter_film(arg))
            elif mode is mode_consultation['INTERNET']:
                label_titre = tk.Label(self.frame_result, text=film['title'] if 'title' in film else film['name'])
                consulter_bouton = tk.Button(self.frame_result, text="Consulter",
                                             command=lambda arg=(film['id'], type_consult, mode_consultation['INTERNET']):
                                             self.consulter_film(arg))
            label_titre.grid(row=i, column=0)
            if mode is mode_consultation['LOCAL']:
                label_annee.grid(row=i, column=1)
            if mode is mode_consultation['LOCAL'] or (mode is mode_consultation['INTERNET']
                                                     and 'media_type' not in film or
                                                         ('media_type' in film and film['media_type'] != 'person')):
                consulter_bouton.grid(row=i, column=2)
            i += 1

        # mise en place de la pagination
        self.frame_pagination = tk.Frame(self.frame_result)
        self.button_precedent = tk.Button(self.frame_pagination, text="Précédent",
                                          command=lambda: self.pagination_precedent())
        self.button_suivant = tk.Button(self.frame_pagination, text="Suivant",
                                        command=lambda: self.pagination_suivant())
        self.label_page_en_cours = tk.Label(self.frame_pagination,
                                            text='Page ' + str(self.page_en_cours) + '/' + str(nombre_page) + '(' + str(
                                                nombre_resultat) + ' films)')

        if self.page_en_cours > 1:
            self.button_precedent.pack(side=tk.LEFT, anchor=tk.W)
        if self.page_en_cours < nombre_page:
            self.button_suivant.pack(side=tk.RIGHT, anchor=tk.E)
        self.label_page_en_cours.pack()
        self.frame_pagination.grid(row=21, column=0, columnspan=3)

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

    def consulter_film(self, args):
        """
            Démarre la vue de consultation d'un film
            :param args: tuple pour l'affichage d'un film (l'id du film, son type, le mode d'ouverture de la fenetre)
        """
        self.consulter_film_fenetre = tk.Toplevel(self.parent)
        self.consulter_film_fenetre = vueConsulterFilm(self.consulter_film_fenetre,
                                                       id_film=args[0], type=args[1], mode=args[2],
                                                       fenetre_appelante=self)
        self.consulter_film_fenetre.pack()
