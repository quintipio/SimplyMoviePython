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


class Collection(database.Entity):
    titre = Required(str)
    idInternet = Optional(int)
    films = Set("Film")


class Genre(database.Entity):
    titre = Required(str)
    idInternet = Required(int)
    films = Set("Film")


class Personne(database.Entity):
    nom = Required(str)
    idInternet = Required(int)
    films_producteur = Set("Film")
    films_realisateur = Set("Film")
    roles = Set("Role")


class Film(database.Entity):
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
    film = Required(Film)
    personne = Required(Personne)
    nom_role = Required(str)
    PrimaryKey(film, personne)


def init_database():
    database.bind("sqlite", "simplyMovie.sqlite", create_db=True)
    database.generate_mapping(create_tables=True)
    sql_debug(True)


def __convert_image_to_byte_array(image):
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr


@db_session
def __get_genre(genre):
    result = Genre.get(idInternet=genre['id'])
    if result is None:
        result = Genre(titre=genre['name'], idInternet=genre['id'])
    return result


@db_session
def __get_personne(personne):
    result = Personne.get(idInternet=personne['id'])
    if result is None:
        result = Personne(nom=personne['name'], idInternet=personne['id'])
    return result


@db_session
def __get_collection(collection):
    result = Collection.get(idInternet=collection['id'])
    if result is None:
        result = Collection(titre=collection['name'], idInternet=collection['id'])
    return result


@db_session
def ajouter_film(data_film, data_casting, type, a_voir, a_acheter, affiche):
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
