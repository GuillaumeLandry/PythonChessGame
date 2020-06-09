# -*- coding: utf-8 -*-
class ExceptionDeplacer(Exception):
    """
    Cette exception est levées lorsque la fonction déplacer ne peut pas être réalisée
    """
    pass


class AucunePiece(Exception):
    """
    Cette exception est levées lorsqu'il n'y a pas de pièce à la position sélectionnée.
    """
    pass


class MauvaiseCouleur(Exception):
    """
    Cette exception est levées lorsque la couleur de la pièce n'est pas celle du joueur actif.
    """
    pass
