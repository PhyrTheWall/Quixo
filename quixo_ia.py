from quixo import Quixo, QuixoError
import random

class QuixoIA(Quixo):
    def __init__(self, joueurs, plateau=None):
        super().__init__(joueurs, plateau)  # Appel au constructeur de la classe Quixo

    def lister_les_coups_possibles(self, plateau, cube):
        if cube not in ["X", "O"]:
            raise QuixoError('Le cube doit être "X" ou "O".')
        if self.partie_terminée():
            raise QuixoError("La partie est déjà terminée.")

        coups = []
        for i in range(5):
            for j in range(5):
                if plateau[i][j] in [cube, " "]:  # Cube valide ou vide
                    if i == 0 or i == 4 or j == 0 or j == 4:  # Bords ou coins
                        directions = self.obtenir_directions_valides(i, j)
                        for direction in directions:
                            coups.append({"origine": [i, j], "direction": direction})
        return coups
    
    def analyser_le_plateau(self, plateau):
        resultats = {"X": {2: 0, 3: 0, 4: 0, 5: 0}, "O": {2: 0, 3: 0, 4: 0, 5: 0}}
        joueurs = ["X", "O"]
        
        for joueur in joueurs:
            lignes = self.compter_lignes(plateau, joueur)
            for taille, nombre in lignes.items():
                resultats[joueur][taille] = nombre
        
        return resultats
    
    def verifier_vainqueur(self, plateau):
        for i in range(5):
            # Vérification des lignes horizontales
            if len(set(plateau[i])) == 1 and plateau[i][0] != " ":
                return plateau[i][0]
        
        # Vérification des colonnes verticales
        colonne = [plateau[j][i] for j in range(5)]
        if len(set(colonne)) == 1 and colonne[0] != " ":
            return colonne[0]
        # Vérification des diagonales
        diagonale1 = [plateau[i][i] for i in range(5)]
        diagonale2 = [plateau[i][4 - i] for i in range(5)]  
        if len(set(diagonale1)) == 1 and diagonale1[0] != " ":
            return diagonale1[0]
        if len(set(diagonale2)) == 1 and diagonale2[0] != " ":
            return diagonale2[0]
        return None  # Aucun vainqueur
    
    def partie_terminée(self):
        # Utilisation de la méthode determiner_vainqueur() héritée de Quixo
        vainqueur = self.determiner_vainqueur()
        return vainqueur is not None  # Si un vainqueur est trouvé, la partie est terminée

    def trouver_un_coup_vainqueur(self, cube):
        for coup in self.lister_les_coups_possibles(self.plateau, cube):
            self.deplacer_un_cube(coup["origine"], coup["direction"])
            if self.determiner_vainqueur() == cube:
                self.annuler_deplacement()  # Réinitialiser pour l'analyse
                return coup
        return None
    
    def trouver_un_coup_bloquant(self, cube):
        adversaire = "O" if cube == "X" else "X"
        for coup in self.lister_les_coups_possibles(self.plateau, cube):
            self.deplacer_un_cube(coup["origine"], coup["direction"])
            if self.determiner_vainqueur() == adversaire:
                self.annuler_deplacement()
                return coup
        return None

    def jouer_un_coup(self, cube):
        if self.partie_terminée():
            raise QuixoError("La partie est déjà terminée.")
    
        # Vérification supplémentaire du cube
        if cube not in ["X", "O"]:
            raise QuixoError(f"Le symbole doit être 'X' ou 'O'. Mais reçu : {cube}")

        coup_vainqueur = self.trouver_un_coup_vainqueur(cube)
        if coup_vainqueur:
            self.deplacer_un_cube(coup_vainqueur["origine"], coup_vainqueur["direction"])
            return coup_vainqueur

        coup_bloquant = self.trouver_un_coup_bloquant(cube)
        if coup_bloquant:
            self.deplacer_un_cube(coup_bloquant["origine"], coup_bloquant["direction"])
            return coup_bloquant

        # Coup aléatoire sinon
        coups_possibles = self.lister_les_coups_possibles(self.plateau, cube)
        coup_choisi = random.choice(coups_possibles)
        self.deplacer_un_cube(coup_choisi["origine"], coup_choisi["direction"])
        return coup_choisi
    # Ajout de la méthode determiner_vainqueur
    def determiner_vainqueur(self):

        # Logique pour déterminer si un joueur a gagné
        # Par exemple, si une ligne entière est remplie avec le même cube (X ou O)
        
        for i in range(5):
            # Vérifier les lignes horizontales
            ligne = [self.plateau[i, j] for j in range(5)]  # Utilisation du bon index (i, j)
            if len(set(ligne)) == 1 and ligne[0] != " ":
                return ligne[0]
        
            # Vérifier les lignes verticales
            colonne = [self.plateau[j, i] for j in range(5)]  # Utilisation du bon index (j, i)
            if len(set(colonne)) == 1 and colonne[0] != " ":
                return colonne[0]

        # Vérification des diagonales
        diagonale1 = [self.plateau[i, i] for i in range(5)]
        diagonale2 = [self.plateau[i, 4 - i] for i in range(5)]
    
        if len(set(diagonale1)) == 1 and diagonale1[0] != " ":
            return diagonale1[0]
        if len(set(diagonale2)) == 1 and diagonale2[0] != " ":
            return diagonale2[0]
    # Si aucune ligne, colonne ou diagonale n'est remplie, il n'y a pas de vainqueur
        return None
        
