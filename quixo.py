"""Module Quixo

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
    """Classe representant le jeux de quixo..."""
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
        """Retourne une représentation en chaîne de caractères de la partie

        Déplacer le code de vos fonctions formater_légende et formater_jeu ici.
        Adaptez votre code en conséquence et faites appel à Plateau
        pour obtenir la représentation du plateau.

        Returns:
            str: Une représentation en chaîne de caractères du plateau.
        """
        return ("Légende:\n"
                + f"   X={self.état_partie()['joueurs'][0]}\n"
                + f"   O={self.état_partie()['joueurs'][1]}\n"
                + f"{Plateau(self.état_partie()['plateau'])}")

    def déplacer_pion(self, pion, origine, direction):
        """Déplacer un pion dans une direction donnée.

        Applique le changement au Plateau de jeu

        Args:
            pion (str): Le pion à déplacer, soit "X" ou "O".
            origine (list[int]): La position (x, y) du pion sur le plateau.
            direction (str): La direction du déplacement, soit "haut", "bas", "gauche" ou "droite".
        """
        self.plateau.insérer_un_cube(pion, origine, direction)

    def choisir_un_coup(self):
        """Demander le prochain coup à jouer au joueur.

        Déplacer le code de votre fonction récupérer_le_coup ici et ajuster le en conséquence.
        Vous devez maintenant valider les entrées de l'utilisateur.

        Returns:
            tuple: Tuple de 2 éléments composé de l'origine du bloc à déplacer et de sa direction.
                L'origine est une liste de 2 entiers [x, y].
                La direction est une chaîne de caractères.

        Raises:
            QuixoError: Les positions x et y doivent être entre 1 et 5 inclusivement.
            QuixoError: La direction doit être "haut", "bas", "gauche" ou "droite".

        Examples:
            Donnez la position d'origine du bloc (x,y) :
            Quelle direction voulez-vous insérer? ('haut', 'bas', 'gauche', 'droite') :
        """
        directions_valide = ['haut', 'bas', 'gauche', 'droite']

        ori = input("Donnez la position d'origine du bloc (x,y) :")
        origine = [int(ori[0]), int(ori[2])]
        direction = input("Direction d'insertion du bloc?"
                          " ('haut', 'bas', 'gauche', 'droite') :")

        if (origine[0] or origine[1]) > 5 or (origine[0] or origine[1]) < 1:
            raise QuixoError("Les positions x et y doivent être entre 1 et 5 inclusivement.")
        if direction not in directions_valide:
            raise QuixoError('La direction doit être "haut", "bas", "gauche" ou "droite".')

        return origine, direction

def interpréter_la_commande():
    """Génère un interpréteur de commande.
    Returns:
        Namespace: Un objet Namespace tel que retourné par parser.parse_args().
            Cet objet aura l'attribut «idul» représentant l'idul du joueur
            et l'attribut «parties» qui est un booléen True/False.
    """
    parser = argparse.ArgumentParser(description="Quixo")
    parser.add_argument('idul', type=str, help= 'IDUL du joueur')
    # Option pour jouer de façon autonome contre l'IA
    parser.add_argument(
        '-a', '--autonome', 
        action="store_true", 
        help="Jouer de façon autonome"
    )
    # Complétez le code ici
    # vous pourriez aussi avoir à ajouter des arguments dans ArgumentParser(...)

    return parser.parse_args()

def determiner_vainqueur(self):
        # Vérification des lignes horizontales
        for i in range(5):
            ligne = self.plateau.get_ligne(i)  # Méthode qui renvoie la i-ème ligne sous forme de liste
            if len(set(ligne)) == 1 and ligne[0] != " ":
                return ligne[0]
            
            # Vérification des lignes verticales
            colonne = self.plateau.get_colonne(i)  # Méthode qui renvoie la i-ème colonne sous forme de liste
            if len(set(colonne)) == 1 and colonne[0] != " ":
                return colonne[0]

        # Vérification des diagonales
        diagonale1 = [self.plateau.get_case(i, i) for i in range(5)]  # Méthode pour obtenir la diagonale principale
        diagonale2 = [self.plateau.get_case(i, 4 - i) for i in range(5)]  # Méthode pour obtenir l'autre diagonale
        
        if len(set(diagonale1)) == 1 and diagonale1[0] != " ":
            return diagonale1[0]
        if len(set(diagonale2)) == 1 and diagonale2[0] != " ":
            return diagonale2[0]

        # Aucun vainqueur
        return None
