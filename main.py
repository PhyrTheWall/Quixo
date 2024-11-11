from api import QuixoAPI
from quixo import QuixoGame

def main():
    idul = input("Entrez votre IDUL: ")
    token = input("Entrez votre jeton d'authentification: ")
    api = QuixoAPI(idul, token)

    try:
        # Créer une nouvelle partie
        game_id, initial_state, winner = api.create_game()
        print("Nouvelle partie créée!")
        
        game = QuixoGame(initial_state["joueurs"], initial_state["plateau"])
        game.display_board()

        # Boucle de jeu
        while not game.is_winner(winner):
            origin, direction = game.get_move()
            if not origin or not direction:
                print("Coup invalide, réessayez.")
                continue

            # Jouer le coup
            try:
                game_id, new_state, winner = api.play_move(game_id, origin, direction)
                game.update_board(new_state["plateau"])
                game.display_board()
            except ValueError as e:
                print(e)
                continue

        print("Partie terminée!")
    except ValueError as e:
        print(f"Erreur: {e}")

if __name__ == "__main__":
    main()