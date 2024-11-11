
import requests


class QuixoAPI:
    BASE_URL = "https://exemple.com/quixo/api/a24/"

    def __init__(self, idul, token):
        self.auth = (idul, token)

    def create_game(self):
        """Crée une nouvelle partie et retourne l'ID de la partie, l'état initial et le gagnant (si disponible)."""
        url = f"{self.BASE_URL}partie/"
        response = requests.post(url, auth=self.auth)
        
        if response.status_code == 200:
            data = response.json()
            return data["id"], data["état"], data["gagnant"]
        
        elif response.status_code == 401:
            raise ValueError("Erreur d'authentification : IDUL ou jeton incorrect.")
        
        elif response.status_code == 406:
            raise ValueError("Paramètres invalides pour créer la partie.")
        
        else:
            response.raise_for_status()

    def play_move(self, game_id, origin, direction):
        """Joue un coup dans la partie spécifiée et retourne l'état du jeu mis à jour et le gagnant."""
        url = f"{self.BASE_URL}partie/{game_id}/"
        move_data = {
            "origine": origin,
            "direction": direction
        }
        
        response = requests.put(url, auth=self.auth, json=move_data)
        
        if response.status_code == 200:
            data = response.json()
            return data["id"], data["état"], data["gagnant"]
        
        elif response.status_code == 401:
            raise ValueError("Erreur d'authentification : IDUL ou jeton incorrect.")
        
        elif response.status_code == 406:
            raise ValueError("Paramètres invalides pour jouer le coup.")
        
        else:
            response.raise_for_status()