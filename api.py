"""
Module d'API du jeu Quixo

Attributes:
    URL (str): Constante représentant le début de l'URL du serveur de jeu.

Functions:
    * initialiser_partie - Crée une nouvelle partie et retourne l'état de cette dernière.
    * jouer_un_coup - Exécute un coup et retourne le nouvel état de jeu.
    * récupérer_une_partie - Retrouve l'état d'une partie spécifique.
"""

import requests

URL = "https://pax.ulaval.ca/quixo/api/a24/"


def initialiser_partie(idul, secret):
    """Initialiser une partie.

    Effectue une requête POST pour initialiser une nouvelle partie.

    Args:
        idul (str): idul du joueur.
        secret (str): secret récupéré depuis le site de PAX.

    Raises:
        PermissionError: Si le serveur retourne un code 401.
        RuntimeError: Si le serveur retourne un code 406.
        ConnectionError: Si le serveur retourne un code autre que 200, 401 ou 406.

    Returns:
        tuple: Tuple de 3 éléments constitué de l'identifiant de la partie en cours,
            de la liste des joueurs et de l'état du plateau.
    """
    url = f"{URL}partie/"
    auth = (idul, secret)
    response = requests.post(url, auth=auth)
    data = response.json()

    print("Réponse de l'API :", data)

    if response.status_code == 401:
        raise PermissionError(response.json().get("message", "Accès refusé."))
    elif response.status_code == 406:
        raise RuntimeError(response.json().get("message", "Requête non acceptable."))
    elif response.status_code != 200:
        raise ConnectionError("Erreur de connexion au serveur.")

    data = response.json()
    return data["id"], data["joueurs"], data["plateau"]


def jouer_un_coup(id_partie, origine, direction, idul, secret):
    """Jouer un coup.

    Effectue une requête PUT pour jouer un coup dans une partie existante.

    Args:
        id_partie (str): Identifiant de la partie.
        origine (list): La position [x, y] du bloc à déplacer.
        direction (str): La direction du déplacement du bloc :
            'haut': Déplacement d'un bloc du bas pour l'insérer en haut.
            'bas': Déplacement d'un bloc du haut pour l'insérer en bas.
            'gauche': Déplacement d'un bloc de droite pour l'insérer à gauche.
            'droite': Déplacement d'un bloc de gauche pour l'insérer à droite.
        idul (str): idul du joueur.
        secret (str): secret récupéré depuis le site de PAX.

    Raises:
        StopIteration: Si un gagnant est trouvé dans la réponse du serveur.
        PermissionError: Si le serveur retourne un code 401.
        RuntimeError: Si le serveur retourne un code 406.
        ConnectionError: Si le serveur retourne un code autre que 200, 401 ou 406.

    Returns:
        tuple: Tuple de 3 éléments constitué de l'identifiant de la partie en cours,
            de la liste des joueurs et de l'état du plateau.
    """
    url = f"{URL}jouer/"
    auth = (idul, secret)
    payload = {"id": id_partie, "origine": origine, "direction": direction}
    response = requests.put(url, json=payload, auth=auth)

    if response.status_code == 401:
        raise PermissionError(response.json().get("message", "Accès refusé."))
    elif response.status_code == 406:
        raise RuntimeError(response.json().get("message", "Requête non acceptable."))
    elif response.status_code != 200:
        raise ConnectionError("Erreur de connexion au serveur.")

    data = response.json()
    if data.get("gagnant"):
        raise StopIteration(f"Partie terminée! Gagnant: {data['gagnant']}")

    return data["id"], data["joueurs"], data["plateau"]


def récupérer_une_partie(id_partie, idul, secret):
    """Récupérer une partie.

    Effectue une requête GET pour récupérer l'état d'une partie spécifique.

    Args:
        id_partie (str): Identifiant de la partie à récupérer.
        idul (str): idul du joueur.
        secret (str): secret récupéré depuis le site de PAX.

    Raises:
        PermissionError: Si le serveur retourne un code 401.
        RuntimeError: Si le serveur retourne un code 406.
        ConnectionError: Si le serveur retourne un code autre que 200, 401 ou 406.

    Returns:
        tuple: Tuple de 4 éléments constitué de l'identifiant de la partie en cours,
            de la liste des joueurs, de l'état du plateau et du vainqueur.
    """
    url = f"{URL}partie/{id_partie}/"
    auth = (idul, secret)
    response = requests.get(url, auth=auth)

    if response.status_code == 401:
        raise PermissionError(response.json().get("message", "Accès refusé."))
    elif response.status_code != 200:
        raise ConnectionError("Erreur de connexion au serveur.")

    data = response.json()
    return data["id"], data["état"]["joueurs"], data["état"]["plateau"], data.get("gagnant")
