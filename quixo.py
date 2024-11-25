"""
Module Quixo

Classes:
    * Quixo - Classe principale du jeu Quixo.
    * QuixoError - Classe d'erreur pour le jeu Quixo.

Functions:
    * interpréter_la_commande - Génère un interpréteur de commande.
"""

import argparse
from quixo_error import QuixoError
from plateau import Plateau


class Quixo:
    def __init__(self, joueurs, plateau=None) -> None:
        """Constructeur de la classe Quixo

        Vous ne devez rien modifier dans cette méthode.

        Args:
            joueurs (list[str]): La liste des deux joueurs.
                Le premier joueur possède le symbole "X" et le deuxième "O".
            plateau (list[list[str]], optional): La représentation du plateau
                tel que retourné par le serveur de jeu ou la valeur None par défaut.
        """
        self.joueurs = joueurs
        self.plateau = Plateau(plateau)

    def état_partie(self):
        """Retourne une copie du jeu

        Retourne une copie du jeu pour éviter les effets de bord.
        Vous ne devez rien modifier dans cette méthode.

        Returns:
            dict: La représentation du jeu tel que retourné par le serveur de jeu.
        """
        return {
            "joueurs": self.joueurs,
            "plateau": self.plateau.état_plateau(),
        }

    def __str__(self):
        """Retourne une représentation en chaîne de caractères de la partie.

        Inclut la légende des joueurs ainsi que le plateau formaté.

        Returns:
            str: Une représentation en chaîne de caractères de la partie.
        """
        légende = (
            f"Joueur 1 (X): {self.joueurs[0]}\n"
            f"Joueur 2 (O): {self.joueurs[1]}\n"
        )
        plateau = str(self.plateau)  # Utilisation de la méthode __str__ de Plateau
        return f"{légende}\n{plateau}"

    def déplacer_un_cube(self, joueur, origine, direction):
        """Déplace un cube sur le plateau.

        Args:
            joueur (str): Le nom du joueur effectuant le déplacement.
            origine (list[int]): La position d'origine du cube [x, y].
            direction (str): La direction du déplacement, soit "haut", "bas", "gauche" ou "droite".

        Raises:
            QuixoError: Si une erreur survient lors de l'insertion du cube.
        """
        # Déterminer le symbole associé au joueur
        symbole = "X" if self.joueurs[0] == joueur else "O"
        try:
            # Insérer le cube via la méthode du plateau
            self.plateau.insérer_un_cube(symbole, origine, direction)
        except QuixoError as e:
            # Répropager l'erreur pour qu'elle soit gérée à un niveau supérieur
            raise QuixoError(f"Erreur lors du déplacement : {e}")

    def choisir_un_coup(self):
        """Demande au joueur d'entrer un coup valide.

        Returns:
            tuple: Tuple composé de l'origine du bloc [x, y] et de la direction.

        Raises:
            QuixoError: Si les positions ou la direction sont invalides.
        """
        try:
            x = int(input("Donnez la position d'origine du bloc (x) : "))
            y = int(input("Donnez la position d'origine du bloc (y) : "))
            if not (1 <= x <= 5 and 1 <= y <= 5):
                raise QuixoError("Les positions x et y doivent être entre 1 et 5 inclusivement.")

            direction = input(
                "Quelle direction voulez-vous insérer? ('haut', 'bas', 'gauche', 'droite') : "
            ).strip().lower()
            if direction not in ["haut", "bas", "gauche", "droite"]:
                raise QuixoError("La direction doit être 'haut', 'bas', 'gauche' ou 'droite'.")

            return [x, y], direction
        except ValueError:
            raise QuixoError("Les positions x et y doivent être des entiers.")

    def jouer(self):
        """Gestion d'un tour de jeu."""
        print(self)
        joueur_actuel = self.joueurs[0]  # Exemple : Alterner ou gérer le joueur actuel
        print(f"C'est au tour de : {joueur_actuel}")
        try:
            origine, direction = self.choisir_un_coup()
            self.déplacer_un_cube(joueur_actuel, origine, direction)
        except QuixoError as e:
            print(f"Erreur : {e}")


def interpréter_la_commande():
    """Génère un interpréteur de commande.

    Returns:
        Namespace: Un objet Namespace tel que retourné par parser.parse_args().
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'idul', type=str, help = 'IDUL du joueur'
    )
    return parser.parse_args()
