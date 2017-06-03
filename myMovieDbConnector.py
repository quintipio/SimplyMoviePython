#!/usr/bin/env Python
# -*-coding:UTF-8 -*
from urllib.request import urlopen
from models import type_film
import requests
from PIL import Image
from io import BytesIO
import os
import json

# clé de connexion à myMovieDb
__key_connector = ""
# adresse de base pour obtenir une affiche de film ou dé série
__root_adress_affiche = "http://image.tmdb.org/t/p/original"
# adresse de base pour obtenir la photo d'un acteur
__root_adress_actor = "https://image.tmdb.org/t/p/w640/"
#adresse de base pour obtenir un résultat de film ou de série
__root_adress_db = "https://api.themoviedb.org/3"

# différentes recherches prise en compte par la classe
search_db = {
    'SEARCH_MOVIE': 1,
    'GET_MOVIE': 2,
    'ASK_POSTER_MOVIE': 3,
    'ASK_CASTING_MOVIE': 4,
    'SEARCH_TV': 5,
    'GET_TV': 6,
    'ASK_POSTER_TV': 7,
    'ASK_CASTING_TV': 8,
    'ASK_SIMILAR_FILM': 9,
    'ASK_SIMILAR_TV': 10,
    'GENERAL_SEARCH': 11,
    'GET_PERSON': 12,
    'GET_PERSON_CREDIT': 13,
    'MOMENT_MOVIE': 14,
    'POPULAR_MOVIE': 15,
    'MOMENT_TV': 16,
    'POPULAR_TV': 17,
    'TV_SEASON': 18,
    'GET_COLLECTION': 19,
}


def __get_data_from_mymoviedb(search_type, query, page=0):
    """
        génère une url pour obtenir les résultats de my movie db, interroge le site et retourne le json
        :param search_type: fait référence au type de recherche indiqué par search_db
        :param query: est la donnée à passer en paramètre pour certaines recherche id de film, chaine de caractère à chercher...)
        :param page: est la page de recherche à obtenir pour les recherches avec plusieurs pages
    """
    url_asking = __root_adress_db

    if search_db['GET_MOVIE'] == search_type:
        url_asking += "/movie/{}".format(query)
    elif search_db['GET_TV'] == search_type:
        url_asking += "/tv/{}".format(query)
    elif search_db['SEARCH_MOVIE'] == search_type:
        url_asking += "/search/movie"
    elif search_db['SEARCH_TV'] == search_type:
        url_asking += "/search/tv"
    elif search_db['ASK_POSTER_MOVIE'] == search_type:
        url_asking += "/movie/{}/images".format(query)
    elif search_db['ASK_POSTER_TV'] == search_type:
        url_asking += "/tv/{}/images".format(query)
    elif search_db['ASK_CASTING_MOVIE'] == search_type:
        url_asking += "/movie/{}/credits".format(query)
    elif search_db['ASK_CASTING_TV'] == search_type:
        url_asking += "/tv/{}/credits".format(query)
    elif search_db['ASK_SIMILAR_FILM'] == search_type:
        url_asking += "/movie/{}/similar".format(query)
    elif search_db['ASK_SIMILAR_TV'] == search_type:
        url_asking += "/tv/{}/similar".format(query)
    elif search_db['TV_SEASON'] == search_type:
        url_asking += "/tv/{}".format(query)
    elif search_db['GENERAL_SEARCH'] == search_type:
        url_asking += "/search/multi"
    elif search_db['GET_PERSON'] == search_type:
        url_asking += "/person/{}".format(query)
    elif search_db['GET_PERSON_CREDIT'] == search_type:
        url_asking += "/person/{}/combined_credits".format(query)
    elif search_db['MOMENT_MOVIE'] == search_type:
        url_asking += "/movie/now_playing"
    elif search_db['MOMENT_TV'] == search_type:
        url_asking += "/tv/on_the_air"
    elif search_db['POPULAR_MOVIE'] == search_type:
        url_asking += "/movie/popular"
    elif search_db['POPULAR_TV'] == search_type:
        url_asking += "/tv/popular"
    elif search_db['GET_COLLECTION'] == search_type:
        url_asking += "/collection/{}".format(query)

    url_asking += "?api_key=" + __key_connector

    if search_db['SEARCH_MOVIE'] == search_type \
            or search_db['SEARCH_TV'] == search_type \
            or search_db['GENERAL_SEARCH'] == search_type:
        url_asking += "&query=" + query.replace(' ', '+')

    if page > 0 and search_type in [search_db['GENERAL_SEARCH'],
                                    search_db['MOMENT_MOVIE'], search_db['MOMENT_TV'],
                                    search_db['POPULAR_MOVIE'], search_db['POPULAR_TV']]:
        url_asking += "&page={}".format(page)

    url_asking += "&language={}".format(os.getenv('LANG'))
    url_asking += "&include_image_language={},null".format(os.getenv('LANG'));

    with urlopen(url_asking) as url:
        data = json.loads(url.read().decode())
        return data


def get_affiche(adresse):
    """
        retourne l'image de l'affiche à partir de son adresse
        :param adresse: étant l'adresse web de l'image
        retourne l'affiche ou en cas d'erreur l'affiche par défaut
    """
    try:
        response = requests.get(__root_adress_affiche + adresse)
        return Image.open(BytesIO(response.content))
    except:
        return Image.open('afficheDefaut.jpg')


def get_data(search_type, query, page=0):
    """
        permet d'obtenir les résultats en appelant une recherche sur myMovieDb
        :param search_type: fait référence au type de recherche indiqué par search_db
        :param query: est la donnée à passer en paramètre pour certaines recherche id de film, chaine de caractère à chercher...)
        :param page: est la page de recherche à obtenir pour les recherches avec plusieurs pages
        :return retourne la liste des résultats en cas de recherche, ou un tuple film casting, affiche pour des données précise de film/série
    """
    # récupération des données d'internet
    data = __get_data_from_mymoviedb(search_type, query, page)

    # en cas de recherche
    if search_type in [search_db['SEARCH_MOVIE'], search_db['SEARCH_TV']]:
        liste_resultat = []
        for data_result in data['results']:
            liste_resultat.append((data_result['poster_path'],
                                   data_result['name'] if search_type is search_db['SEARCH_TV'] else data_result[
                                       'title'],
                                   data_result['id']))
        return liste_resultat

    # en cas de recherche de film ou de série
    if search_type in [search_db['GET_TV'], search_db['GET_MOVIE']]:
        casting = __get_data_from_mymoviedb(search_db['ASK_CASTING_TV']
                                 if search_type == search_db['GET_TV'] else
                                 search_db['ASK_CASTING_MOVIE'], data['id'])
        return data, casting, get_affiche(data['poster_path'])


def get_popular_movie(type_recherche,page):
    """
        Retourne une liste de série ou de film/série populaire ou du moment 
        :param type_recherche: le type de recherche à effectuer
        :param page: la page de résultats
        :return une liste de résultats
    """
    results = __get_data_from_mymoviedb(type_recherche, None, page)
    return results
