"""Jeu Quixo

Ce programme permet de joueur au jeu Quixo.
"""

from api import initialiser_partie, jouer_un_coup
from quixo import Quixo, interpréter_la_commande


SECRET = "b0bda578-f449-4cea-8589-82f13e3cf57e"


if __name__ == "__main__":
    args = interpréter_la_commande()
    id_partie, joueurs, plateau = initialiser_partie(args.idul, SECRET)
    while True:
        # Créer une instance de Quixo
        quixo = Quixo(joueurs, plateau)
        # Afficher la partie
        print(quixo)
        # Demander au joueur de choisir son prochain coup
        origine, direction = quixo.choisir_un_coup()
        # Envoyez le coup au serveur
        id_partie, joueurs, plateau = jouer_un_coup(
            id_partie,
            origine,
            direction,
            args.idul,
            SECRET,
        )

    
    
