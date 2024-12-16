""" Definition d"une classe qui gere les erreurs"""

class QuixoError(Exception):
    """classe QuixoError..."""
    def __init__(self, message):
        super().__init__(message)
