#!/usr/bin/env Python
# -*-coding:UTF-8 -*
import models
import myMovieDbConnector

"""
    Script pour ajouter automatiquement les films en base à partir d'un fichier CSV de deux colonnes
    (idinternet, type) ou type correspond à l'enum de SimplyMovie sur le windows Store
"""
# lecture du fichier
with open("listeFilm.csv") as f:
    content = f.readlines()
content = [x.strip() for x in content]

# séparation des résultats en liste
resultat = []
for c in content:
    resultat.append([c.split(';')[0], c.split(';')[1]])

# ouverture de la base
models.init_database()
# ajout de chaque ligne du fichier en base
for r in resultat:
    # mise en place des variables pour la recherche
    idInternet = int(r[0])
    type = int(r[1])
    recherche = myMovieDbConnector.search_db['GET_TV'] if type == 2 else myMovieDbConnector.search_db['GET_MOVIE']
    # conversion pour l'enum de SImply Movie du Windows Store pour correspodnre au model type_film de cette applicatio
    if type > 3:
        type = type - 1
    print("Id=" + str(idInternet) + "-Type=" + str(type))

    # vérification si la donnée est déjà présente en base
    if not models.verifier_film_en_base(idInternet, type):
        # récupération des données d'internet
        data, casting, affiche = myMovieDbConnector.get_data(recherche, idInternet)
        # ajout du film en base
        models.ajouter_film(data, casting, type, False, False, affiche)
        print(str(data["id"]) + " ajouté")
    else:
        print("Deja présent")
