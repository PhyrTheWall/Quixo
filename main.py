from api import initialiser_partie, jouer_un_coup
from quixo import Quixo, interpréter_la_commande
from quixo_ia import QuixoIA

SECRET = "b0bda578-f449-4cea-8589-82f13e3cf57e"

if __name__ == "__main__":
    args = interpréter_la_commande()
    id_partie, joueurs, plateau = initialiser_partie(args.idul, SECRET)
    ia_active = args.autonome  # Activer le mode IA si --autonome est spécifié

    # Association des identifiants à des symboles
    joueurs_symbols = {"raauc8": "X", "autre_id": "O"}  # Remplace "autre_id" par l'ID réel du deuxième joueur

    while True:
        if ia_active:
            # Utiliser l'IA pour choisir un coup
            quixo_ia = QuixoIA(joueurs, plateau)
            joueur_courant = joueurs[0]
            symbole_joueur_courant = joueurs_symbols[joueur_courant]
            print(f"Joueur courant : {joueur_courant} avec symbole {symbole_joueur_courant}")
            origine, direction = quixo_ia.jouer_un_coup(symbole_joueur_courant)
        else:
            # Jeu standard : demander au joueur son coup
            quixo = Quixo(joueurs, plateau)
            print(quixo)
            origine, direction = quixo.choisir_un_coup()
        
        # Envoyer le coup au serveur
        id_partie, joueurs, plateau = jouer_un_coup(
            id_partie,
            origine,
            direction,
            args.idul,
            SECRET,
        )
