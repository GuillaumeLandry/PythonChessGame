# -*- coding: utf-8 -*-
"""Module contenant la classe de base Piece, ainsi qu'une classe fille pour chacun des types de pièces du jeu d'échecs.

"""
# TODO: Si votre système n'affiche pas correctement les caractères unicodes du jeu d'échecs,
# mettez cette constante (variable globale) à False. Un tutoriel est présent sur le site Web
# du cours pour vous aider à faire fonctionner les caractères Unicoe sous Windows.
UTILISER_UNICODE = False


def position_split(position_source, position_cible):
    """Prend les arguments positions_sources et position_cible et sépare la lettre et le chiffre. Les chiffres sont
        transformé en entier dans l'objectif d'appliquer des opérations mathématiques. La lettre est transformé en
        index dans l'objectif d'apliquer des opérations mathématiques.

    Args:
        position_source (str): La position source, suivant le format ci-haut. Par exemple, 'a8', 'f3', etc.
        position_cible (str): La position cible, suivant le format ci-haut. Par exemple, 'b6', 'h1', etc.

    Returns:
        depart: Nombre entier.
        arrive: Nombre entier.
        index_depart: Nombre entier.
        index_arrive: Nombre entier.
        positon_source: Liste contenant deux chaînes de caractères.
        position_cible: Liste contenant deux chaînes de caractères.
    """

    position_source = position_source[0].split() + position_source[1].split()
    depart = int(position_source[1])
    position_cible = position_cible[0].split() + position_cible[1].split()
    arrive = int(position_cible[1])

    list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    index_depart = list.index(position_source[0])
    index_arrive = list.index(position_cible[0])

    return [depart, arrive, index_depart, index_arrive, position_source, position_cible]


class Piece:
    """Une classe de base représentant une pièce du jeu d'échecs. C'est cette classe qui est héritée plus bas pour fournir
    une classe par type de pièce (Pion, Tour, etc.).

    Attributes:
        couleur (str): La couleur de la pièce, soit 'blanc' ou 'noir'.
        peut_sauter (bool): Si oui ou non la pièce peut "sauter" par dessus d'autres pièces sur un échiquier.

    Args:
        couleur (str): La couleur avec laquelle créer la pièce.
        peut_sauter (bool): La valeur avec laquelle l'attribut peut_sauter doit être initialisé.

    """

    def __init__(self, couleur, peut_sauter):
        # Validation si la couleur reçue est valide.
        assert couleur in ('blanc', 'noir')

        # Création des attributs avec les valeurs reçues.
        self.couleur = couleur
        self.peut_sauter = peut_sauter

    def est_blanc(self):
        """Retourne si oui ou non la pièce est blanche.

        Returns:
            bool: True si la pièce est blanche, et False autrement.

        """
        return self.couleur == 'blanc'

    def est_noir(self):
        """Retourne si oui ou non la pièce est noire.

        Returns:
            bool: True si la pièce est noire, et False autrement.

        """
        return self.couleur == 'noir'

    def peut_se_deplacer_vers(self, position_source, position_cible):
        """Vérifie si, selon les règles du jeu d'échecs, la pièce peut se déplacer d'une position à une autre.

        Une position est une chaîne de deux caractères.
            Le premier caractère est une lettre entre a et h, représentant la colonne de l'échiquier.
            Le second caractère est un chiffre entre 1 et 8, représentant la rangée de l'échiquier.

        Args:
            position_source (str): La position source, suivant le format ci-haut. Par exemple, 'a8', 'f3', etc.
            position_cible (str): La position cible, suivant le format ci-haut. Par exemple, 'b6', 'h1', etc.

        Returns:
            bool: True si le déplacement est valide en suivant les règles de la pièce, et False autrement.

        """

        # On lance une exception (on y reviendra) indiquant que ce code n'a pas été implémenté. Ne touchez pas
        # à cette méthode : réimplémentez-la dans les classes filles!
        raise NotImplementedError

    def peut_faire_une_prise_vers(self, position_source, position_cible):
        """Vérifie si, selon les règles du jeu d'échecs, la pièce peut "manger" (faire une prise) une pièce ennemie.
        Pour la plupart des pièces, la règle est la même, on appelle donc la méthode peut_se_deplacer_vers.

        Si ce n'est pas le cas pour une certaine pièce, on peut simplement redéfinir cette méthode pour programmer
        la règle.

        Args:
            position_source (str): La position source, suivant le format ci-haut. Par exemple, 'a8', 'f3', etc.
            position_cible (str): La position cible, suivant le format ci-haut. Par exemple, 'b6', 'h1', etc.

        Returns:
            bool: True si la prise est valide en suivant les règles de la pièce, et False autrement.

        """

        return self.peut_se_deplacer_vers(position_source, position_cible)


class Pion(Piece):
    def __init__(self, couleur):
        super().__init__(couleur, False)

    def peut_se_deplacer_vers(self, position_source, position_cible):
        """Vérifie si, selon les règles du jeu d'échecs, la pièce peut se déplacer d'une position à une autre.

        Une position est une chaîne de deux caractères.
            Le premier caractère est une lettre entre a et h, représentant la colonne de l'échiquier.
            Le second caractère est un chiffre entre 1 et 8, représentant la rangée de l'échiquier.

        Args:
            position_source (str): La position source, suivant le format ci-haut. Par exemple, 'a8', 'f3', etc.
            position_cible (str): La position cible, suivant le format ci-haut. Par exemple, 'b6', 'h1', etc.

        Returns:
            bool: True si le déplacement est valide en suivant les règles de la pièce, et False autrement.

        """

        pos = position_split(position_source, position_cible)

        if self.est_blanc() and pos[4][0] == pos[5][0] and pos[4][1] < pos[5][1]: # Si le pion avance, mais ne change pas de rangée
            if pos[0] == 2 and pos[1] - pos[0] <= 2: # Si le pion est sur sa case départ, il avance de 1 ou 2
                return True

            elif pos[0] != 2 and pos[1] - pos[0] == 1: # Si le pion n'est plus sur sa case départ, il avance de 1
                return True

        elif self.est_noir() and pos[4][0] == pos[5][0] and pos[4][1] > pos[5][1]:
            if pos[0] == 7 and pos[0] - pos[1] <= 2:
                return True

            elif pos[0] != 7 and pos[0] - pos[1] == 1:
                return True

        else:
            return False

    def peut_faire_une_prise_vers(self, position_source, position_cible):
        """Vérifie si, selon les règles du jeu d'échecs, la pièce peut "manger" (faire une prise) une pièce ennemie.

        Args:
            position_source (str): La position source, suivant le format ci-haut. Par exemple, 'a8', 'f3', etc.
            position_cible (str): La position cible, suivant le format ci-haut. Par exemple, 'b6', 'h1', etc.

        Returns:
            bool: True si la prise est valide en suivant les règles de la pièce, et False autrement.

        """

        pos = position_split(position_source, position_cible) # Voir fonction position_split

        if self.est_blanc() and pos[1] == pos[0]+1 and pos[3] == pos[2]+1: # Diagonale haut-droite
            return True
        elif self.est_blanc() and pos[1] == pos[0]+1 and pos[3] == pos[2]-1: # Diagonale haut-gauche
            return True

        elif self.est_noir() and pos[1] == pos[0]-1 and pos[3] == pos[2]+1: # Diagonale bas-droite
            return True
        elif self.est_noir() and pos[1] == pos[0]-1 and pos[3] == pos[2]-1: # Diagonale bas-gauche
            return True

        else:
            return False

    def __repr__(self):
        """Redéfinit comment on affiche un pion à l'écran. Nous utilisons la constante UTILISER_UNICODE
        pour déterminer comment afficher le pion.

        Returns:
            str: La chaîne de caractères représentant le pion.

        """

        if self.est_blanc():
            return 'Pion Blanc'
        else:
            return 'Pion Noir'


class Tour(Piece):
    def __init__(self, couleur):
        super().__init__(couleur, False)

    def peut_se_deplacer_vers(self, position_source, position_cible):
        """Vérifie si, selon les règles du jeu d'échecs, la pièce peut se déplacer d'une position à une autre.

        Une position est une chaîne de deux caractères.
            Le premier caractère est une lettre entre a et h, représentant la colonne de l'échiquier.
            Le second caractère est un chiffre entre 1 et 8, représentant la rangée de l'échiquier.

        Args:
            position_source (str): La position source, suivant le format ci-haut. Par exemple, 'a8', 'f3', etc.
            position_cible (str): La position cible, suivant le format ci-haut. Par exemple, 'b6', 'h1', etc.

        Returns:
            bool: True si le déplacement est valide en suivant les règles de la pièce, et False autrement.

        """

        pos = position_split(position_source, position_cible)

        if position_source == position_cible: # Deplacement sur la meme case
            return False

        elif pos[0] == pos[1] and pos[2] != pos[3]: # Deplacement vertical
            return True

        elif pos[2] == pos[3] and pos[0] != pos[1]: # Deplacement horizontal
            return True

        else:
            return False

    def peut_faire_une_prise_vers(self, position_source, position_cible):
        """Vérifie si, selon les règles du jeu d'échecs, la pièce peut "manger" (faire une prise) une pièce ennemie.

        Args:
            position_source (str): La position source, suivant le format ci-haut. Par exemple, 'a8', 'f3', etc.
            position_cible (str): La position cible, suivant le format ci-haut. Par exemple, 'b6', 'h1', etc.

        Returns:
            bool: True si la prise est valide en suivant les règles de la pièce, et False autrement.

        """

        return self.peut_se_deplacer_vers(position_source, position_cible)

    def __repr__(self):
        if self.est_blanc():
            return 'Tour Blanc'
        else:
            return 'Tour Noir'


class Cavalier(Piece):
    def __init__(self, couleur):
        super().__init__(couleur, True)

    def peut_se_deplacer_vers(self, position_source, position_cible):
        """Vérifie si, selon les règles du jeu d'échecs, la pièce peut se déplacer d'une position à une autre.

        Une position est une chaîne de deux caractères.
            Le premier caractère est une lettre entre a et h, représentant la colonne de l'échiquier.
            Le second caractère est un chiffre entre 1 et 8, représentant la rangée de l'échiquier.

        Args:
            position_source (str): La position source, suivant le format ci-haut. Par exemple, 'a8', 'f3', etc.
            position_cible (str): La position cible, suivant le format ci-haut. Par exemple, 'b6', 'h1', etc.

        Returns:
            bool: True si le déplacement est valide en suivant les règles de la pièce, et False autrement.

        """

        pos = position_split(position_source, position_cible)

        if position_source == position_cible: # Deplacement sur la meme case
            return False

        # Deplacement en "L" vertical
        elif (pos[1] == pos[0] + 2 and (pos[3] == pos[2] + 1 or pos[3] == pos[2] - 1)) or (pos[1] == pos[0] - 2 and (pos[3] == pos[2] + 1 or pos[3] == pos[2] - 1)):
            return True

        # Deplacement en "L" horizontal
        elif (pos[1] == pos[0] + 1 and (pos[3] == pos[2] + 2 or pos[3] == pos[2] - 2)) or (pos[1] == pos[0] - 1 and (pos[3] == pos[2] + 2 or pos[3] == pos[2] - 2)):
            return True

        else:
            return False

    def peut_faire_une_prise_vers(self, position_source, position_cible):
        """Vérifie si, selon les règles du jeu d'échecs, la pièce peut "manger" (faire une prise) une pièce ennemie.

        Args:
            position_source (str): La position source, suivant le format ci-haut. Par exemple, 'a8', 'f3', etc.
            position_cible (str): La position cible, suivant le format ci-haut. Par exemple, 'b6', 'h1', etc.

        Returns:
            bool: True si la prise est valide en suivant les règles de la pièce, et False autrement.

        """

        return self.peut_se_deplacer_vers(position_source, position_cible)

    def __repr__(self):
        if self.est_blanc():
            return 'Cavalier Blanc'
        else:
            return 'Cavalier Noir'


class Fou(Piece):
    def __init__(self, couleur):
        super().__init__(couleur, False)

    def peut_se_deplacer_vers(self, position_source, position_cible):
        """Vérifie si, selon les règles du jeu d'échecs, la pièce peut se déplacer d'une position à une autre.

        Une position est une chaîne de deux caractères.
            Le premier caractère est une lettre entre a et h, représentant la colonne de l'échiquier.
            Le second caractère est un chiffre entre 1 et 8, représentant la rangée de l'échiquier.

        Args:
            position_source (str): La position source, suivant le format ci-haut. Par exemple, 'a8', 'f3', etc.
            position_cible (str): La position cible, suivant le format ci-haut. Par exemple, 'b6', 'h1', etc.

        Returns:
            bool: True si le déplacement est valide en suivant les règles de la pièce, et False autrement.

        """

        pos = position_split(position_source, position_cible)
        dia = pos[1] - pos[0]

        if position_source == position_cible: # Deplacement sur la même case
            return False

        # Deplacement diagonal
        elif (pos[1] == pos[0] + dia and (pos[3] == pos[2] + dia or pos[3] == abs(pos[2] - dia))) or (
                pos[1] == pos[0] + dia and (pos[3] == pos[2] + dia or pos[3] == abs(pos[2] - dia))):
            return True

        else:
            return False

    def peut_faire_une_prise_vers(self, position_source, position_cible):
        """Vérifie si, selon les règles du jeu d'échecs, la pièce peut "manger" (faire une prise) une pièce ennemie.

        Args:
            position_source (str): La position source, suivant le format ci-haut. Par exemple, 'a8', 'f3', etc.
            position_cible (str): La position cible, suivant le format ci-haut. Par exemple, 'b6', 'h1', etc.

        Returns:
            bool: True si la prise est valide en suivant les règles de la pièce, et False autrement.

        """

        return self.peut_se_deplacer_vers(position_source, position_cible)

    def __repr__(self):
        if self.est_blanc():
            return 'Fou Blanc'
        else:
            return 'Fou Noir'


class Roi(Piece):
    def __init__(self, couleur):
        super().__init__(couleur, False)

    def peut_se_deplacer_vers(self, position_source, position_cible):
        """Vérifie si, selon les règles du jeu d'échecs, la pièce peut se déplacer d'une position à une autre.

        Une position est une chaîne de deux caractères.
            Le premier caractère est une lettre entre a et h, représentant la colonne de l'échiquier.
            Le second caractère est un chiffre entre 1 et 8, représentant la rangée de l'échiquier.

        Args:
            position_source (str): La position source, suivant le format ci-haut. Par exemple, 'a8', 'f3', etc.
            position_cible (str): La position cible, suivant le format ci-haut. Par exemple, 'b6', 'h1', etc.

        Returns:
            bool: True si le déplacement est valide en suivant les règles de la pièce, et False autrement.

        """

        pos = position_split(position_source, position_cible)

        if position_source[0] == position_cible[0] and position_source[1] != position_cible[1]: # Deplacement vertical
            if pos[1] == pos[0] + 1 or pos[1] == pos[0] - 1:
                return True

        if position_source[0] != position_cible[0] and position_source[1] == position_cible[1]: # Deplacement horizontal
            if pos[3] == pos[2] + 1 or pos[3] == pos[2] -1:
                return True

        if position_source[0] != position_cible[0] and position_source[1] != position_cible[1]: # Deplacement diagonal
            if pos[1] == pos[0] + 1 and pos[3] == pos[2] + 1:
                return True
            if pos[1] == pos[0] + 1 and pos[3] == pos[2] - 1:
                return True
            if pos[1] == pos[0] - 1 and pos[3] == pos[2] + 1:
                return True
            if pos[1] == pos[0] - 1 and pos[3] == pos[2] - 1:
                return True

        return False

    def peut_faire_une_prise_vers(self, position_source, position_cible):
        """Vérifie si, selon les règles du jeu d'échecs, la pièce peut "manger" (faire une prise) une pièce ennemie.

        Args:
            position_source (str): La position source, suivant le format ci-haut. Par exemple, 'a8', 'f3', etc.
            position_cible (str): La position cible, suivant le format ci-haut. Par exemple, 'b6', 'h1', etc.

        Returns:
            bool: True si la prise est valide en suivant les règles de la pièce, et False autrement.

        """

        return self.peut_se_deplacer_vers(position_source, position_cible)

    def __repr__(self):
        if self.est_blanc():
            return 'Roi Blanc'
        else:
            return 'Roi Noir'


class Dame(Piece):
    def __init__(self, couleur):
        super().__init__(couleur, False)

    def peut_se_deplacer_vers(self, position_source, position_cible):
        """Vérifie si, selon les règles du jeu d'échecs, la pièce peut se déplacer d'une position à une autre.

        Une position est une chaîne de deux caractères.
            Le premier caractère est une lettre entre a et h, représentant la colonne de l'échiquier.
            Le second caractère est un chiffre entre 1 et 8, représentant la rangée de l'échiquier.

        Args:
            position_source (str): La position source, suivant le format ci-haut. Par exemple, 'a8', 'f3', etc.
            position_cible (str): La position cible, suivant le format ci-haut. Par exemple, 'b6', 'h1', etc.

        Returns:
            bool: True si le déplacement est valide en suivant les règles de la pièce, et False autrement.

        """

        pos = position_split(position_source, position_cible)
        dia = pos[1] - pos[0]

        if position_source == position_cible: # Deplacement sur la meme case
            return False

        elif pos[0] == pos[1] and pos[2] != pos[3]: # Deplacement horizontal
            return True

        elif pos[2] == pos[3] and pos[0] != pos[1]: # Deplacement vertical
            return True

        elif (pos[1] == pos[0] + dia and (pos[3] == pos[2] + dia or pos[3] == abs(pos[2] - dia))) or (
                pos[1] == pos[0] + dia and (pos[3] == pos[2] + dia or pos[3] == abs(pos[2] - dia))): # Deplacement diagonal
            return True

        else:
            return False

    def peut_faire_une_prise_vers(self, position_source, position_cible):
        """Vérifie si, selon les règles du jeu d'échecs, la pièce peut "manger" (faire une prise) une pièce ennemie.

        Args:
            position_source (str): La position source, suivant le format ci-haut. Par exemple, 'a8', 'f3', etc.
            position_cible (str): La position cible, suivant le format ci-haut. Par exemple, 'b6', 'h1', etc.

        Returns:
            bool: True si la prise est valide en suivant les règles de la pièce, et False autrement.

        """

        return self.peut_se_deplacer_vers(position_source, position_cible)

    def __repr__(self):
        if self.est_blanc():
            return 'Dame Blanc'
        else:
            return 'Dame Noir'
