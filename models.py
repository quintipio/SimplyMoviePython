#!/usr/bin/env Python
# -*-coding:UTF-8 -*
from pony.orm import *
import io

database = Database()

role = {
    'ACTEUR': 1,
    'PRODUCTEUR': 2,
    'REALISATEUR': 3
}

type_film = {
    'FILM': 1,
    'SERIE': 2,
    'DOCUMENTAIRE': 3,
    'SPECTACLE': 4,
    'ANIMATION': 5
}

type_recherche = {
    'A_VOIR':1,
    'A_ACHETER':2,
    'CONNU':3,
}


class Collection(database.Entity):
    """
        Modèle pour une collection de films
    """
    titre = Required(str)
    idInternet = Optional(int)
    films = Set("Film")


class Genre(database.Entity):
    """
        Modèle pour un genre de film
    """
    titre = Required(str)
    idInternet = Required(int)
    films = Set("Film")


class Personne(database.Entity):
    """
        Modèle pour une personne au sein d'un film
    """
    nom = Required(str)
    idInternet = Required(int)
    films_producteur = Set("Film")
    films_realisateur = Set("Film")
    roles = Set("Role")


class Film(database.Entity):
    """
        Modèle pour un film
    """
    titre = Required(str)
    annee = Required(int)
    producteurs = Set("Personne", reverse="films_producteur")
    realisateurs = Set("Personne", reverse="films_realisateur")
    roles = Set("Role")
    genres = Set("Genre")
    synopsis = Optional(unicode)
    affiche = Optional(bytes)
    type = Required(int)
    noteGen = Optional(float)
    saison = Optional(int)
    duree = Optional(int)
    a_voir = Optional(bool)
    a_acheter = Optional(bool)
    id_internet = Optional(int)
    collection = Optional(Collection)
        


class Role(database.Entity):
    """
        Table de liaison entre une personne et un film en indiquant son role d'acteur au sein du film (uniquement pour les acteurs)
    """
    film = Required(Film)
    personne = Required(Personne)
    nom_role = Required(str)
    PrimaryKey(film, personne)


def init_database():
    """
        Initialisation de la base de donnée et création au besoin
    """
    database.bind("sqlite", "simplyMovie.sqlite", create_db=True)
    database.generate_mapping(create_tables=True)
    sql_debug(True)


def __convert_image_to_byte_array(image):
    """
        converti une image de la bibliothèque PIL en byteArray pour être blober
    """
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr

@db_session
def get_liste_film(type_recherche_param) :
    """
        retourne une liste de film recherché en fonction du paramètre "type_recherche_param" indiqué par "type_recherche"
    """
    if type_recherche_param is type_recherche['A_VOIR'] :
        result = select(f for f in Film if f.a_voir is True and f.a_acheter is not True)
    elif type_recherche_param is type_recherche['A_ACHETER']:
        result = select(f for f in Film if f.a_acheter is True).get()
    
    retour = []
    for tuple in result :
        retour.append(tuple)
    return retour
        

@db_session
def __verifier_film_en_base(id_internet):
    """
        vérifie si un film est en base en le recherchant par son id internet
    """
    return count(f for f in Film if f.id_internet == id_internet)


@db_session
def __get_genre(genre):
    """
        retourne un genre s'il existe déjà sinon le crée et retourne le résultat
    """
    result = Genre.get(idInternet=genre['id'])
    if result is None:
        result = Genre(titre=genre['name'], idInternet=genre['id'])
    return result


@db_session
def __get_personne(personne):
    """
        retourne une personne si elle existe déjà sinon la créee et retourne le résultat
    """
    result = Personne.get(idInternet=personne['id'])
    if result is None:
        result = Personne(nom=personne['name'], idInternet=personne['id'])
    return result


@db_session
def __get_collection(collection):
    """
        retourne une collection si elle existe déjà sinon la créee et retourne le résultat
    """
    result = Collection.get(idInternet=collection['id'])
    if result is None:
        result = Collection(titre=collection['name'], idInternet=collection['id'])
    return result


@db_session
def ajouter_film(data_film, data_casting, type, a_voir, a_acheter, affiche):
    """
        créer un film en base de donnée ou retourne une erreur s'il existe déja
        data_film contient les données du film
        data_casting contient les acteurs producteurs et réalisateurs
        type fait référence à type_film
        a_voir est un boolean pour indiquer si le film est à voir
        a_acheter est un boolean pour indiquer si le film est à acheter
        affiche est l'image d el'affiche du film
    """
    if __verifier_film_en_base(data_film['id']) is False:
        producteurs = []
        realisateurs = []
        for data_result in data_casting['crew']:
            if 'producer' in data_result['job'].lower():
                producteurs.append(__get_personne(data_result))
            if 'director' in data_result['job'].lower():
                realisateurs.append(__get_personne(data_result))

        liste_genre = []
        for data_result in data_film['genres']:
            liste_genre.append(__get_genre(data_result))

        film = Film(
            titre=data_film['title'],
            duree=data_film['runtime'] if type == type_film['FILM'] else data_film['episode_run_time'],
            annee=data_film['release_date'][:4] if type == type_film['FILM'] else data_film['first_air_date'],
            affiche=__convert_image_to_byte_array(affiche),
            id_internet=data_film['id'],
            synopsis=data_film['overview'],
            noteGen=data_film['vote_average'],
            saison=0 if type == type_film['FILM'] else data_film['number_of_seasons'],
            genres=liste_genre,
            type=type,
            a_acheter=a_acheter,
            a_voir=a_voir,
            producteurs=producteurs,
            realisateurs=realisateurs,
            collection=None if data_film['belongs_to_collection'] is None
            else __get_collection(data_film['belongs_to_collection'])
        )

        roles = []
        for data_result in data_casting['cast']:
            roles.append(Role(film=film
                            , personne=(__get_personne(data_result))
                            , nom_role=data_result['character']))
        return None
    else:
        return "Ce film est déjà présent"
        
