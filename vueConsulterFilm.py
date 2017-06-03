#!/usr/bin/env Python
# -*-coding:UTF-8 -*
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from models import get_film, get_type, supprimer_film, type_film, verifier_film_en_base,\
    passer_film_to_achete, passer_film_to_vue_or_voir
from myMovieDbConnector import get_data, search_db
from PIL import Image, ImageTk
from resizeimage import resizeimage
from vueAjouterFilm import vueAjouterFilm
import io

# mode d'utilisation de la vue de consultation (film en base ou provenant d'internet)
mode_consultation = {
    'LOCAL': 1,
    'INTERNET': 2
}


class vueConsulterFilm(ttk.Frame):
    """
        Classe de la frame pour consulter un film
    """

    def __init__(self, parent, id_film, type, mode, fenetre_appelante, *args, **kwargs):
        """
        Initialisation de la frame
        :param parent: l'objet parent
        :param id_film: l'id du film à afficher
        :param type: le type de film à afficher
        :param mode: le mode d'utilisation de la vue (internet ou local)
        :param fenetre_appelante: la fenetre appelante (pour le rafraichissement en cas d'effacement)
        :param args: arguments de la frame
        :param kwargs: arguments de la frame
        """
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.fenetre_appelante = fenetre_appelante
        self.mode = mode
        self.type = type

        # récupération du film et affichage
        if mode is mode_consultation['LOCAL']:
            film = get_film(id_film)
            self.afficher_film_local(film)
        if mode is mode_consultation['INTERNET']:
            if type is type_film['SERIE'] :
                film, casting, affiche = get_data(search_db['GET_TV'],id_film)
            else:
                film, casting, affiche = get_data(search_db['GET_MOVIE'], id_film)
            self.afficher_film_internet(film, casting, affiche)

    def afficher_film_internet(self, film, casting, affiche):
        """
        Méthode pour afficher un film provenant d'internet
        :param film: le film à afficher
        :param casting: son casting et équipe technique
        :param affiche: l'affiche du film
        """
        # affichage de l'affiche
        if affiche is not None:
            image = ImageTk.PhotoImage(
                resizeimage.resize_thumbnail(affiche, [400, 200]))
        else:
            image = ImageTk.PhotoImage(resizeimage.resize_thumbnail(Image.open("afficheDefaut.jpg"), [400, 200]))
        self.label_affiche = ttk.Label(self, image=image)
        self.label_affiche.img = image
        # titre
        self.label_titre = ttk.Label(self, text=film['title'] if 'title' in film else film['name'], font='bold 16')
        # année
        if ('release_date' in film and film['release_date'] is not None) or \
                ('first_air_date' in film and film['first_air_date'] is not None) :
            self.label_annee = ttk.Label(self, text='Année : '+str(film['release_date'][:4] if 'release_date' in film else
                                                       film['first_air_date'][:4]))
        # durée
        if ('runtime' in film and film['runtime'] is not None) or \
                ('episode_run_time' in film and film['episode_run_time'] is not None):
            self.label_duree = ttk.Label(self, text='Durée : '+str(film['runtime'] if 'runtime' in film else
                                                       film['episode_run_time'][:4]))
        # nombre de saisons
        if 'number_of_seasons' in film and film['number_of_seasons'] is not None and film['number_of_seasons'] > 0:
            self.label_saison = ttk.Label(self, text=('Saisons : ' + str(film['number_of_seasons'])))
        # note
        if 'vote_average' in film and film['vote_average'] is not None:
            self.label_note = ttk.Label(self, text=str(film['vote_average']) + '/10')
        # collection
        if 'belongs_to_collection' in film and film['belongs_to_collection'] is not None:
            self.label_collection = ttk.Label(self, text='Collection : '+str(film['belongs_to_collection']['name']))
        # genres
        self.frame_genres = ttk.Frame(self)
        titre_lab_genre = ttk.Label(self.frame_genres, text='Genres : ', padx=2, font='bold')
        titre_lab_genre.pack(side=tk.LEFT)
        if len(film['genres']) > 0:
            for genre in film['genres']:
                lab_genre = ttk.Label(self.frame_genres, text=genre['name'], padx=2)
                lab_genre.pack(side=tk.LEFT)
        # producteurs
        liste_producteurs = [item for item in casting['crew'] if 'producer' in str(item['job']).lower()]
        if len(liste_producteurs) > 0:
            r = 0
            c = 1
            self.frame_producteurs = ttk.Frame(self)
            titre_lab_producteurs = ttk.Label(self.frame_producteurs, text='Producteurs : ', padx=2, font='bold')
            titre_lab_producteurs.grid(row=0, column=0)
            for producteur in liste_producteurs:
                lab_producteur = ttk.Label(self.frame_producteurs, text=producteur['name'], padx=2)
                lab_producteur.grid(row=r, column=c)
                c += 1
                if c is 4:
                    c = 0
                    r += 1
        # réalisateurs
        liste_realisateurs = [item for item in casting['crew'] if 'director' in str(item['job']).lower()]
        if len(liste_realisateurs) > 0:
            r = 0
            c = 1
            self.frame_realisateurs = ttk.Frame(self)
            titre_lab_realisateurs = ttk.Label(self.frame_realisateurs, text='Réalisateurs : ', padx=2, font='bold')
            titre_lab_realisateurs.grid(row=0, column=0)
            for realisateur in liste_realisateurs:
                lab_realisateur = ttk.Label(self.frame_realisateurs, text=realisateur['name'], padx=2)
                lab_realisateur.grid(row=r, column=c)
                c += 1
                if c is 4:
                    c = 0
                    r += 1
        # casting principal
        if len(casting['cast']) > 0:
            r = 0
            c = 1
            self.frame_acteurs = ttk.Frame(self)
            titre_lab_acteurs = ttk.Label(self.frame_acteurs, text='Acteurs : ', padx=2, font='bold')
            titre_lab_acteurs.grid(row=0, column=0)
            for acteur in casting['cast'][:10]:
                lab_acteur = ttk.Label(self.frame_acteurs, text=(acteur['name'] + '(' + acteur['character'] + ')'), padx=2)
                lab_acteur.grid(row=r, column=c)
                c += 1
                if c is 4:
                    c = 0
                    r += 1
        # bouton d'ajout en base
        self.button_ajout = ttk.Button(self, text="Ajouter à la bibliothèque",
                                      command=lambda: self.ajouter_film(film['id'],
                                                                        film['title'] if 'title' in film
                                                                        else film['name']
                                                                        , affiche))
        # histoire
        self.label_synopsis = ttk.Label(self, text=film['overview'], wraplength=500, pady=10)

        # affichage des élements
        self.label_affiche.grid(row=0, column=0, rowspan=9)
        self.label_titre.grid(row=0, column=1)
        if ('release_date' in film and film['release_date'] is not None) or \
                ('first_air_date' in film and film['first_air_date'] is not None):
            self.label_annee.grid(row=1, column=1)
        if ('runtime' in film and film['runtime'] is not None) or \
                ('episode_run_time' in film and film['episode_run_time'] is not None):
            self.label_duree.grid(row=2, column=1)
        if 'number_of_seasons' in film and film['number_of_seasons'] is not None and film['number_of_seasons'] > 0:
            self.label_saison.grid(row=3, column=1)
        if 'vote_average' in film and film['vote_average'] is not None:
            self.label_note.grid(row=4, column=1)
        if 'belongs_to_collection' in film and film['belongs_to_collection'] is not None:
            self.label_collection.grid(row=5, column=1)
        if len(film['genres']) > 0:
            self.frame_genres.grid(row=6, column=1)
        if len(liste_producteurs) > 0:
            self.frame_producteurs.grid(row=7, column=1)
        if len(liste_realisateurs) > 0:
            self.frame_realisateurs.grid(row=8, column=1)
        if not verifier_film_en_base(film['id'], self.type):
            self.button_ajout.grid(row=9, column=0)
        if len(casting['cast']) > 0:
            self.frame_acteurs.grid(row=10, column=0, columnspan=2)
        self.label_synopsis.grid(row=11, column=0, columnspan=2)

    def afficher_film_local(self, film):
        """
        Affiche les données d'un film en base
        :param film: le film à afficher
        """
        # affiche
        if film['affiche'] is not None:
            image = ImageTk.PhotoImage(
                resizeimage.resize_thumbnail(Image.open(io.BytesIO(film['affiche'])), [400, 200]))
        else:
            image = ImageTk.PhotoImage(resizeimage.resize_thumbnail(Image.open("afficheDefaut.jpg"), [400, 200]))
        self.label_affiche = ttk.Label(self, image=image)
        self.label_affiche.img = image
        # titre
        self.label_titre = ttk.Label(self, text=film['titre'], font='bold 16')
        # annee
        if film['annee'] is not None:
            self.label_annee = ttk.Label(self, text=str(film['annee']))
        # duree
        if film['duree'] is not None:
            self.label_duree = ttk.Label(self, text=('Durée : ' + str(film['duree']) + ' minutes'))
        # saison
        if film['saison'] is not None and film['saison'] > 0:
            self.label_saison = ttk.Label(self, text=('Saisons : ' + str(film['saison'])))
        # note générale
        if film['note_gen'] is not None:
            self.label_note = ttk.Label(self, text=str(film['note_gen']) + '/10')
        # le type de film
        self.label_type = ttk.Label(self, text=get_type(film['type']))
        # est à acheter ou non
        self.label_a_acheter = ttk.Label(self, text=('A acheter : ' + ('Oui' if film['a_acheter'] is True else 'Non')))
        # est à voir
        self.label_a_voir = ttk.Label(self, text=('A voir : ' + ('Oui' if film['a_voir'] is True else 'Non')))
        # collection
        if film['collection'] is not None:
            self.label_collection = ttk.Label(self, text=('De la collection : ' + film['collection']['titre']))
        # boutons
        self.frame_boutons = ttk.Frame(self)
        self.button_supprimer = ttk.Button(self.frame_boutons, text="Supprimer",
                                          command=lambda: self.supprimer_film(film['id']))
        self.button_supprimer.pack(side=tk.LEFT)
        self.button_vu = ttk.Button(self.frame_boutons, text="Vu !" if film['a_voir'] is True else 'A voir !',
                                       command=lambda: self.film_vu(film['id']))
        self.button_vu.pack(side=tk.LEFT)
        if film['a_acheter'] is True :
            self.button_achete = ttk.Button(self.frame_boutons, text="Acheté !",
                                           command=lambda: self.film_achete(film['id']))
            self.button_achete.pack(side=tk.LEFT)
        # histoire
        self.label_synopsis = ttk.Label(self, text=film['synopsis'], wraplength=500)
        # genres
        self.frame_genres = ttk.Frame(self)
        titre_lab_genre = ttk.Label(self.frame_genres, text='Genres : ', font='bold')
        titre_lab_genre.pack(side=tk.LEFT)
        if len(film['genres']) > 0:
            for genre in film['genres']:
                lab_genre = ttk.Label(self.frame_genres, text=genre['titre'])
                lab_genre.pack(side=tk.LEFT)
        # producteurs
        if len(film['producteurs']) > 0:
            r = 0
            c = 1
            self.frame_producteurs = ttk.Frame(self)
            titre_lab_producteurs = ttk.Label(self.frame_producteurs, text='Producteurs : ', font='bold')
            titre_lab_producteurs.grid(row=0, column=0)
            for producteur in film['producteurs']:
                lab_producteur = ttk.Label(self.frame_producteurs, text=producteur['nom'])
                lab_producteur.grid(row=r, column=c)
                c += 1
                if c is 4:
                    c = 0
                    r += 1
        # realisateurs
        if len(film['realisateurs']) > 0:
            r = 0
            c = 1
            self.frame_realisateurs = ttk.Frame(self)
            titre_lab_realisateurs = ttk.Label(self.frame_realisateurs, text='Réalisateurs : ', font='bold')
            titre_lab_realisateurs.grid(row=0, column=0)
            for realisateur in film['realisateurs']:
                lab_realisateur = ttk.Label(self.frame_realisateurs, text=realisateur['nom'])
                lab_realisateur.grid(row=r, column=c)
                c += 1
                if c is 4:
                    c = 0
                    r += 1
        # casting
        if len(film['acteurs']) > 0:
            r = 0
            c = 1
            self.frame_acteurs = ttk.Frame(self)
            titre_lab_acteurs = ttk.Label(self.frame_acteurs, text='Acteurs : ', font='bold')
            titre_lab_acteurs.grid(row=0, column=0)
            for acteur in film['acteurs']:
                lab_acteur = ttk.Label(self.frame_acteurs, text=(acteur['nom'] + '(' + acteur['role'] + ')'))
                lab_acteur.grid(row=r, column=c)
                c += 1
                if c is 4:
                    c = 0
                    r += 1

        # affichage des éléments
        self.label_affiche.grid(row=0, column=0, rowspan=12)
        self.label_titre.grid(row=0, column=1)
        if film['annee'] is not None:
            self.label_annee.grid(row=1, column=1)
        if film['duree'] is not None:
            self.label_duree.grid(row=2, column=1)
        if film['saison'] is not None and film['saison'] > 0:
            self.label_saison.grid(row=3, column=1)
        if film['note_gen'] is not None:
            self.label_note.grid(row=4, column=1)
        self.label_type.grid(row=5, column=1)
        self.label_a_acheter.grid(row=6, column=1)
        self.label_a_voir.grid(row=7, column=1)
        if film['collection'] is not None:
            self.label_collection.grid(row=8, column=1)
        if len(film['genres']) > 0:
            self.frame_genres.grid(row=9, column=1)
        if len(film['producteurs']) > 0:
            self.frame_producteurs.grid(row=10, column=1)
        if len(film['realisateurs']) > 0:
            self.frame_realisateurs.grid(row=11, column=1)
        self.frame_boutons.grid(row=12, column=0)
        if len(film['acteurs']) > 0:
            self.frame_acteurs.grid(row=13, column=0, columnspan=2)
        self.label_synopsis.grid(row=14, column=0, columnspan=2)

    def film_vu(self, id):
        nouvelle_valeur = passer_film_to_vue_or_voir(id)
        self.fenetre_appelante.recherche_liste_film()
        self.label_a_voir['text'] = 'A voir : ' + ('Oui' if nouvelle_valeur is True else 'Non')
        self.button_vu['text'] = 'Vu !' if nouvelle_valeur is True else 'A voir !'

    def film_achete(self, id):
        passer_film_to_achete(id)
        self.fenetre_appelante.recherche_liste_film()
        self.button_achete.forget()

    def supprimer_film(self, id):
        """
            Supprime un film de la base et ferme la fenêtre
            :param id: action de suppression d'un film en base
        """
        result_question = messagebox.askquestion(title="Supression du film",
                                                 message="Etes vous sûr de vouloir supprimer ce film ?", icon="warning")
        if result_question == 'yes':
            supprimer_film(id)
            self.fenetre_appelante.recherche_liste_film()
            self.parent.destroy()

    def ajouter_film(self, film_id, titre, affiche):
        """
            Ouvre la fenetre pour ajouter le film en base
            :param film_id: id du film à ajouter
            :param titre : le titre du filmà ajouter
            :param affiche : l'affiche du film à ajouter
        """
        self.ajouter_film_fenetre = tk.Toplevel(self.parent)
        self.ajouter_film_frame = vueAjouterFilm(self.ajouter_film_fenetre)
        self.ajouter_film_frame.charger_film(film_id, titre, affiche, self.type, self.parent)
        self.ajouter_film_frame.pack()
