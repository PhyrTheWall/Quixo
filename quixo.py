class QuixoGame:
    def __init__(self, players, board):
        self.players = players
        self.board = board

    def display_board(self):
        """Affiche le plateau dans une représentation lisible."""
        print("Plateau actuel:")
        for row in self.board:
            print(" | ".join(row))
            print("-" * 13)

    def update_board(self, new_board):
        """Met à jour le plateau avec un nouvel état."""
        self.board = new_board

    def is_winner(self, winner_name):
        """Affiche le gagnant si la partie est terminée."""
        if winner_name:
            print(f"Le gagnant est : {winner_name}")
            return True
        return False

    def get_move(self):
        """Demande à l'utilisateur de saisir l'origine et la direction du coup."""
        try:
            origin = list(map(int, input("Entrez l'origine du coup (colonne, ligne): ").split(",")))
            direction = input("Entrez la direction (haut, bas, gauche, droite): ").strip().lower()
            if direction not in ["haut", "bas", "gauche", "droite"]:
                raise ValueError("Direction invalide.")
            return origin, direction
        except ValueError as e:
            print(f"Erreur: {e}")
            return None, None

