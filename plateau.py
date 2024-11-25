"""
Module Plateau

Classes:
    * Plateau - Classe principale du plateau de jeu Quixo.
"""

from copy import deepcopy
from quixo_error import QuixoError


class Plateau:
    def __init__(self, plateau=None):
        """Constructeur de la classe Plateau

        Vous ne devez rien modifier dans cette méthode.

        Args:
            plateau (list[list[str]], optional): La représentation du plateau
                tel que retourné par le serveur de jeu ou la valeur None par défaut.
        """
        self.plateau = self.générer_le_plateau(deepcopy(plateau))

    def état_plateau(self):
        """Retourne une copie du plateau

        Retourne une copie du plateau pour éviter les effets de bord.
        Vous ne devez rien modifier dans cette méthode.

        Returns:
            list[list[str]]: La représentation du plateau
            tel que retourné par le serveur de jeu.
        """
        return deepcopy(self.plateau)

    def __str__(self):
        """Retourne une représentation en chaîne de caractères du plateau

        Returns:
            str: Une représentation en chaîne de caractères du plateau.
        """
        lignes = []
        for ligne in self.plateau:
            lignes.append(' | '.join(ligne))
        return '\n' + '\n'.join(lignes) + '\n'

    def __getitem__(self, position):
        """Retourne la valeur à la position donnée

        Args:
            position (tuple[int, int]): La position (x, y) du cube sur le plateau.

        Returns:
            str: La valeur à la position donnée, soit "X", "O" ou " ".

        Raises:
            QuixoError: Les positions x et y doivent être entre 1 et 5 inclusivement.
        """
        x, y = position
        if not (1 <= x <= 5 and 1 <= y <= 5):
            raise QuixoError("Les positions x et y doivent être entre 1 et 5 inclusivement.")
        return self.plateau[x - 1][y - 1]

    def __setitem__(self, position, valeur):
        """Modifie la valeur à la position donnée

        Args:
            position (tuple[int, int]): La position (x, y) du cube sur le plateau.
            valeur (str): La valeur à insérer à la position donnée, soit "X", "O" ou " ".

        Raises:
            QuixoError: Les positions x et y doivent être entre 1 et 5 inclusivement.
            QuixoError: Valeur du cube invalide.
        """
        x, y = position
        if not (1 <= x <= 5 and 1 <= y <= 5):
            raise QuixoError("Les positions x et y doivent être entre 1 et 5 inclusivement.")
        if valeur not in ["X", "O", " "]:
            raise QuixoError("Valeur du cube invalide.")
        self.plateau[x - 1][y - 1] = valeur

    def générer_le_plateau(self, plateau):
        """Génère un plateau de jeu

        Si un plateau est fourni, il est retourné tel quel.
        Sinon, si la valeur est None, un plateau vide de 5x5 est retourné.

        Args:
            plateau (list[list[str]] | None): La représentation du plateau
                tel que retourné par le serveur de jeu ou la valeur None.

        Returns:
            list[list[str]]: La représentation du plateau
                tel que retourné par le serveur de jeu.

        Raises:
            QuixoError: Format du plateau invalide.
            QuixoError: Valeur du cube invalide.
        """
        if plateau is None:
            return [[" " for _ in range(5)] for _ in range(5)]
        if len(plateau) != 5 or any(len(ligne) != 5 for ligne in plateau):
            raise QuixoError("Format du plateau invalide.")
        for ligne in plateau:
            if any(cube not in ["X", "O", " "] for cube in ligne):
                raise QuixoError("Valeur du cube invalide.")
        return plateau

    def insérer_un_cube(self, cube, origine, direction):
        """Insère un cube dans le plateau

        Cette méthode appelle la méthode d'insertion appropriée selon la direction donnée.

        Args:
            cube (str): La valeur du cube à insérer, soit "X" ou "O".
            origine (list[int]): La position [x, y] d'origine du cube à insérer.
            direction (str): La direction de l'insertion, soit "haut", "bas", "gauche" ou "droite".

        Raises:
            QuixoError: La direction doit être "haut", "bas", "gauche" ou "droite".
            QuixoError: Le cube à insérer ne peut pas être vide.
        """
        if cube not in ["X", "O"]:
            raise QuixoError("Le cube à insérer ne peut pas être vide.")
        directions = {
            "haut": self.insérer_par_le_haut,
            "bas": self.insérer_par_le_bas,
            "gauche": self.insérer_par_la_gauche,
            "droite": self.insérer_par_la_droite,
        }
        if direction not in directions:
            raise QuixoError("La direction doit être 'haut', 'bas', 'gauche' ou 'droite'.")
        directions[direction](cube, origine)

    def insérer_par_le_bas(self, cube, origine):
        x, y = origine
        for i in range(4, 0, -1):
            self[x + i, y] = self[x + i - 1, y]
        self[x, y] = cube

    def insérer_par_le_haut(self, cube, origine):
        x, y = origine
        for i in range(4):
            self[x + i, y] = self[x + i + 1, y]
        self[x + 4, y] = cube

    def insérer_par_la_gauche(self, cube, origine):
        x, y = origine
        for i in range(4):
            self[x, y + i] = self[x, y + i + 1]
        self[x, y + 4] = cube

    def insérer_par_la_droite(self, cube, origine):
        x, y = origine
        for i in range(4, 0, -1):
            self[x, y + i] = self[x, y + i - 1]
        self[x, y] = cube
