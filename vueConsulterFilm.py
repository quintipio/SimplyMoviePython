#!/usr/bin/env Python
# -*-coding:UTF-8 -*
import tkinter as tk
from tkinter import messagebox
from models import get_film, get_type, supprimer_film, type_film
from myMovieDbConnector import get_data, search_db
from PIL import Image, ImageTk
from resizeimage import resizeimage
import io

acteur_par_page = 5

mode_consultation = {
    'LOCAL': 1,
    'INTERNET': 2
}


class vueConsulterFilm(tk.Frame):
    """
        Class de la frame pour consulter un film
    """

    def __init__(self, parent, id_film, type, mode, fenetre_appelante, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.fenetre_appelante = fenetre_appelante
        self.mode = mode
        self.type = type

        #récupération du film
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
        if affiche is not None:
            image = ImageTk.PhotoImage(
                resizeimage.resize_thumbnail(affiche, [400, 200]))
        else:
            image = ImageTk.PhotoImage(resizeimage.resize_thumbnail(Image.open("afficheDefaut.jpg"), [400, 200]))
        self.label_affiche = tk.Label(self, image=image)
        self.label_affiche.img = image
        self.label_titre = tk.Label(self, text=film['title'] if 'title' in film else film['name'], font='bold 16')
        if ('release_date' in film and film['release_date'] is not None) or \
                ('first_air_date' in film and film['first_air_date'] is not None) :
            self.label_annee = tk.Label(self, text='Année : '+str(film['release_date'][:4] if 'release_date' in film else
                                                       film['first_air_date'][:4]))
        if ('runtime' in film and film['runtime'] is not None) or \
                ('episode_run_time' in film and film['episode_run_time'] is not None):
            self.label_duree = tk.Label(self, text='Durée : '+str(film['runtime'] if 'runtime' in film else
                                                       film['episode_run_time'][:4]))
        if 'number_of_seasons' in film and film['number_of_seasons'] is not None and film['number_of_seasons'] > 0:
            self.label_saison = tk.Label(self, text=('Saisons : ' + str(film['number_of_seasons'])))
        if 'vote_average' in film and film['vote_average'] is not None:
            self.label_note = tk.Label(self, text=str(film['vote_average']) + '/10')
        if 'belongs_to_collection' in film and film['belongs_to_collection'] is not None:
            self.label_collection = tk.Label(self, text='Collection : '+str(film['belongs_to_collection']['name']))
        self.frame_genres = tk.Frame(self)
        titre_lab_genre = tk.Label(self.frame_genres, text='Genres : ', padx=2, font='bold')
        titre_lab_genre.pack(side=tk.LEFT)
        if len(film['genres']) > 0:
            for genre in film['genres']:
                lab_genre = tk.Label(self.frame_genres, text=genre['name'], padx=2)
                lab_genre.pack(side=tk.LEFT)
        liste_producteurs = [item for item in casting['crew'] if 'producer' in str(item['job']).lower()]
        if len(liste_producteurs) > 0:
            r = 0
            c = 1
            self.frame_producteurs = tk.Frame(self)
            titre_lab_producteurs = tk.Label(self.frame_producteurs, text='Producteurs : ', padx=2, font='bold')
            titre_lab_producteurs.grid(row=0, column=0)
            for producteur in liste_producteurs:
                lab_producteur = tk.Label(self.frame_producteurs, text=producteur['name'], padx=2)
                lab_producteur.grid(row=r, column=c)
                c += 1
                if c is 4:
                    c = 0
                    r += 1
        liste_realisateurs = [item for item in casting['crew'] if 'director' in str(item['job']).lower()]
        if len(liste_realisateurs) > 0:
            r = 0
            c = 1
            self.frame_realisateurs = tk.Frame(self)
            titre_lab_realisateurs = tk.Label(self.frame_realisateurs, text='Réalisateurs : ', padx=2, font='bold')
            titre_lab_realisateurs.grid(row=0, column=0)
            for realisateur in liste_realisateurs:
                lab_realisateur = tk.Label(self.frame_realisateurs, text=realisateur['name'], padx=2)
                lab_realisateur.grid(row=r, column=c)
                c += 1
                if c is 4:
                    c = 0
                    r += 1
        if len(casting['cast']) > 0:
            r = 0
            c = 1
            self.frame_acteurs = tk.Frame(self)
            titre_lab_acteurs = tk.Label(self.frame_acteurs, text='Acteurs : ', padx=2, font='bold')
            titre_lab_acteurs.grid(row=0, column=0)
            for acteur in casting['cast'][:10]:
                lab_acteur = tk.Label(self.frame_acteurs, text=(acteur['name'] + '(' + acteur['character'] + ')'), padx=2)
                lab_acteur.grid(row=r, column=c)
                c += 1
                if c is 4:
                    c = 0
                    r += 1
        self.label_synopsis = tk.Label(self, text=film['overview'], wraplength=500, pady=10)

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
        if len(casting['cast']) > 0:
            self.frame_acteurs.grid(row=9, column=0, columnspan=2)
        self.label_synopsis.grid(row=10, column=0, columnspan=2)

    def afficher_film_local(self, film):
        if film['affiche'] is not None:
            image = ImageTk.PhotoImage(
                resizeimage.resize_thumbnail(Image.open(io.BytesIO(film['affiche'])), [400, 200]))
        else:
            image = ImageTk.PhotoImage(resizeimage.resize_thumbnail(Image.open("afficheDefaut.jpg"), [400, 200]))
        self.label_affiche = tk.Label(self, image=image)
        self.label_affiche.img = image
        self.label_titre = tk.Label(self, text=film['titre'], font='bold 16')
        if film['annee'] is not None:
            self.label_annee = tk.Label(self, text=str(film['annee']))
        if film['duree'] is not None:
            self.label_duree = tk.Label(self, text=('Durée : ' + str(film['duree']) + ' minutes'))
        if film['saison'] is not None and film['saison'] > 0:
            self.label_saison = tk.Label(self, text=('Saisons : ' + str(film['saison'])))
        if film['note_gen'] is not None:
            self.label_note = tk.Label(self, text=str(film['note_gen']) + '/10')
        self.label_type = tk.Label(self, text=get_type(film['type']))
        self.label_a_acheter = tk.Label(self, text=('A acheter : ' + ('Oui' if film['a_acheter'] is True else 'Non')))
        self.label_a_voir = tk.Label(self, text=('A voir : ' + ('Oui' if film['a_voir'] is True else 'Non')))
        if film['collection'] is not None:
            self.label_collection = tk.Label(self, text=('De la collection : ' + film['collection']['titre']))
        self.frame_genres = tk.Frame(self)
        self.button_supprimer = tk.Button(self, text="Supprimer", command=lambda: self.supprimer_film(film['id']))
        self.label_synopsis = tk.Label(self, text=film['synopsis'], wraplength=500, pady=10)

        titre_lab_genre = tk.Label(self.frame_genres, text='Genres : ', padx=2, font='bold')
        titre_lab_genre.pack(side=tk.LEFT)
        if len(film['genres']) > 0:
            for genre in film['genres']:
                lab_genre = tk.Label(self.frame_genres, text=genre['titre'], padx=2)
                lab_genre.pack(side=tk.LEFT)

        if len(film['producteurs']) > 0:
            r = 0
            c = 1
            self.frame_producteurs = tk.Frame(self)
            titre_lab_producteurs = tk.Label(self.frame_producteurs, text='Producteurs : ', padx=2, font='bold')
            titre_lab_producteurs.grid(row=0, column=0)
            for producteur in film['producteurs']:
                lab_producteur = tk.Label(self.frame_producteurs, text=producteur['nom'], padx=2)
                lab_producteur.grid(row=r, column=c)
                c += 1
                if c is 4:
                    c = 0
                    r += 1

        if len(film['realisateurs']) > 0:
            r = 0
            c = 1
            self.frame_realisateurs = tk.Frame(self)
            titre_lab_realisateurs = tk.Label(self.frame_realisateurs, text='Réalisateurs : ', padx=2, font='bold')
            titre_lab_realisateurs.grid(row=0, column=0)
            for realisateur in film['realisateurs']:
                lab_realisateur = tk.Label(self.frame_realisateurs, text=realisateur['nom'], padx=2)
                lab_realisateur.grid(row=r, column=c)
                c += 1
                if c is 4:
                    c = 0
                    r += 1

        if len(film['acteurs']) > 0:
            r = 0
            c = 1
            self.frame_acteurs = tk.Frame(self)
            titre_lab_acteurs = tk.Label(self.frame_acteurs, text='Acteurs : ', padx=2, font='bold')
            titre_lab_acteurs.grid(row=0, column=0)
            for acteur in film['acteurs']:
                lab_acteur = tk.Label(self.frame_acteurs, text=(acteur['nom'] + '(' + acteur['role'] + ')'), padx=2)
                lab_acteur.grid(row=r, column=c)
                c += 1
                if c is 4:
                    c = 0
                    r += 1

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
        self.button_supprimer.grid(row=12, column=0)
        if len(film['acteurs']) > 0:
            self.frame_acteurs.grid(row=13, column=0, columnspan=2)
        self.label_synopsis.grid(row=14, column=0, columnspan=2)

    def supprimer_film(self, id):
        """
            Supprime un film de la base et ferme la fenêtre
        """
        result_question = messagebox.askquestion(title="Supression du film",
                                                 message="Etes vous sûr de vouloir supprimer ce film ?", icon="warning")
        if result_question == 'yes':
            supprimer_film(id)
            self.fenetre_appelante.recherche_liste_film()
            self.parent.destroy()


if __name__ == "__main__":
    vueConsulterFilmFrame = tk.Tk()
    vueConsulterFilm(vueConsulterFilmFrame, 8, vueConsulterFilmFrame).pack(side="top", fill="both", expand=True)
    vueConsulterFilmFrame.mainloop()
