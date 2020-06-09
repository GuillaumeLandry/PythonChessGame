# -*- coding: utf-8 -*-
from pychecs2.echecs.piece import Pion, Tour, Fou, Cavalier, Dame, Roi, position_split, UTILISER_UNICODE
from pychecs2.echecs.exceptions import ExceptionDeplacer


class Echiquier:
    """Classe Echiquier, implémentée avec un dictionnaire de pièces.


    Attributes:
        dictionnaire_pieces (dict): Un dictionnaire dont les clés sont des positions, suivant le format suivant:
            Une position est une chaîne de deux caractères.
            Le premier caractère est une lettre entre a et h, représentant la colonne de l'échiquier.
            Le second caractère est un chiffre entre 1 et 8, représentant la rangée de l'échiquier.
        chiffres_rangees (list): Une liste contenant, dans l'ordre, les chiffres représentant les rangées.
        lettres_colonnes (list): Une liste contenant, dans l'ordre, les lettres représentant les colonnes.

    """
    def __init__(self):
        # Le dictionnaire de pièces, vide au départ, mais ensuite rempli par la méthode initialiser_echiquier_depart().
        self.dictionnaire_pieces = {}

        # Ces listes pourront être utilisées dans les autres méthodes, par exemple pour valider une position.
        self.chiffres_rangees = ['1', '2', '3', '4', '5', '6', '7', '8']
        self.lettres_colonnes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        self.initialiser_echiquier_depart()


    def position_est_valide(self, position):
        """Vérifie si une position est valide (dans l'échiquier). Une position est une concaténation d'une lettre de
        colonne et d'un chiffre de rangée, par exemple 'a1' ou 'h8'.

        Args:
            position (str): La position à valider.

        Returns:
            bool: True si la position est valide, False autrement.

        """

        if len(position) == 2:
            position = position[0].split() + position[1].split()
            if position[0] in self.lettres_colonnes and position[1] in self.chiffres_rangees:
                return True

        return False


    def recuperer_piece_a_position(self, position):
        """Retourne la pièce qui est située à une position particulière, reçue en argument. Si aucune pièce n'est
        située à cette position, retourne None.

        Args:
            position (str): La position où récupérer la pièce.

        Returns:
            Piece or None: Une instance de type Piece si une pièce était située à cet endroit, et None autrement.

        """

        if position in self.dictionnaire_pieces.keys():
            Piece = self.dictionnaire_pieces[position]
            return Piece

        else:
            return None


    def couleur_piece_a_position(self, position):
        """Retourne la couleur de la pièce située à la position reçue en argument, et une chaîne vide si aucune
        pièce n'est à cet endroit.

        Args:
            position (str): La position où récupérer la couleur de la pièce.

        Returns:
            str: La couleur de la pièce s'il y en a une, et '' autrement.

        """

        if position in self.dictionnaire_pieces.keys():
            couleur = self.dictionnaire_pieces[position].couleur
            return couleur

        else:
            return ""


    def rangees_entre(self, rangee_debut, rangee_fin):
        """Retourne la liste des rangées qui sont situées entre les deux rangées reçues en argument, exclusivement.
        Attention de conserver le bon ordre.

        Args:
            rangee_debut (str): Le caractère représentant la rangée de début, par exemple '1'.
            rangee_fin (str): Le caractère représentant la rangée de fin, par exemple '4'.

        Returns:
            list: Une liste des rangées (en str) entre le début et la fin, dans le bon ordre.

        """

        list_rangee = []
        debut = int(rangee_debut)
        fin = int(rangee_fin)

        if rangee_debut in self.chiffres_rangees and rangee_fin in self.chiffres_rangees:
            if debut < fin:
                while debut + 1 < fin:
                    debut += 1
                    list_rangee.append(str(debut))

            if debut > fin:
                while debut -1 > fin:
                    debut -= 1
                    list_rangee.append(str(debut))

        return list_rangee


    def colonnes_entre(self, colonne_debut, colonne_fin):
        """Retourne la liste des colonnes qui sont situées entre les deux colonnes reçues en argument, exclusivement.
        Attention de conserver le bon ordre.

        Args:
            colonne_debut (str): Le caractère représentant la colonne de début, par exemple 'a'.
            colonne_fin (str): Le caractère représentant la colonne de fin, par exemple 'h'.

        Returns:
            list: Une liste des colonnes (en str) entre le début et la fin, dans le bon ordre.

        """

        list_colonne = []
        debut = self.lettres_colonnes.index(colonne_debut)
        fin = self.lettres_colonnes.index(colonne_fin)

        if colonne_debut in self.lettres_colonnes and colonne_fin in self.lettres_colonnes:
            if debut < fin:
                while debut + 1 < fin:
                    debut += 1
                    list_colonne.append(self.lettres_colonnes[debut])

            if debut > fin:
                while debut -1 > fin:
                    debut -= 1
                    list_colonne.append(self.lettres_colonnes[debut])

        return list_colonne


    def chemin_libre_entre_positions(self, position_source, position_cible):
        """Vérifie si la voie est libre entre deux positions, reçues en argument. Cette méthode sera pratique
        pour valider les déplacements: la plupart des pièces ne peuvent pas "sauter" par dessus d'autres pièces,
        il faut donc s'assurer qu'il n'y a pas de pièce dans le chemin.

        On distingue quatre possibilités (à déterminer dans votre code): Soit les deux positions sont sur la même
        rangée, soit elles sont sur la même colonne, soit il s'agit d'une diagonale, soit nous sommes dans une
        situation où nous ne pouvons pas chercher les positions "entre" les positions source et cible. Dans les trois
        premiers cas, on fait la vérification et on retourne True ou False dépendamment la présence d'une pièce ou non.
        Dans la dernière situation, on considère que les positions reçues sont invalides et on retourne toujours False.

        Args:
            position_source (str): La position source.
            position_cible (str): La position cible.

        Returns:
            bool: True si aucune pièce n'est située entre les deux positions, et False autrement (ou si les positions
                ne permettaient pas la vérification).

        """

        pos = position_split(position_source, position_cible)

        # Deplacement valide sur une meme colonne
        if pos[2] == pos[3] and pos[0] != pos[1]:
            cd = self.rangees_entre(position_source[1], position_cible[1])
            if len(cd) == 0:
                return True

            else:
                liste_disponible = [(position_source[0] + cd) for cd in cd]

                for element in liste_disponible:
                    if element in self.dictionnaire_pieces.keys():
                        return False
                    else:
                        return True

        # Deplacement valide sur une meme rangee
        if pos[0] == pos[1] and pos[2] != pos[3]:
            cd = self.colonnes_entre(position_source[0], position_cible[0])
            if len(cd) == 0:
                return True

            else:
                liste_disponible = [(cd + position_source[1]) for cd in cd]

                for element in liste_disponible:
                    if element in self.dictionnaire_pieces.keys():
                        return False
                    else:
                        return True

        # Deplacement valide sur une diagonale
        if (pos[0] + 1 <= pos[1] and pos[2] + 1 <= pos[3] or pos[0] - 1 >= pos[1] and pos[2] - 1 >= pos[3]
                or pos[0] + 1 <= pos[1] and pos[2] - 1 >= pos[3] or pos[0] -1 >= pos[1] and pos[2] + 1 <= pos[3]):
            cdr = self.rangees_entre(position_source[1], position_cible[1])
            cdc = self.colonnes_entre(position_source[0], position_cible[0])
            i = 0
            liste_disponible = []

            if len(cdr) == 0 or len(cdc) == 0:
                return True

            while i < len(cdc):
                liste_disponible.append(cdc[i] + cdr[i])
                i += 1

            for element in liste_disponible:
                if element in self.dictionnaire_pieces.keys():
                    return False
                else:
                    return True

        return False


    def deplacement_est_valide(self, position_source, position_cible):
        """Vérifie si un déplacement serait valide dans l'échiquier actuel.

        Règles pour qu'un déplacement soit valide:
            1. Il doit y avoir une pièce à la position source.
            2. La position cible doit être valide (dans l'échiquier).
            3. Si la pièce ne peut pas sauter, le chemin doit être libre entre les deux positions.
            4. S'il y a une pièce à la position cible, elle doit être de couleur différente.
            5. Le déplacement doit être valide pour cette pièce particulière.

        Args:
            position_source (str): La position source du déplacement.
            position_cible (str): La position cible du déplacement.

        Returns:
            bool: True si le déplacement est valide, et False autrement.

        """

        if position_source in self.dictionnaire_pieces.keys():
            if self.position_est_valide(position_cible):
                # Dans le cas ou la piece ne peut pas sauter
                if self.dictionnaire_pieces[position_source].peut_sauter is False:
                    if self.chemin_libre_entre_positions(position_source, position_cible):
                        if self.couleur_piece_a_position(position_source) != self.couleur_piece_a_position(position_cible):
                            # Dans le cas ou le deplacement est le meme pour une prise que pour un mouvement normal
                            if self.recuperer_piece_a_position(position_source).peut_se_deplacer_vers(position_source, position_cible):
                                return True

                            # Dans le cas ou le deplacement n'est pas le meme pour une prise ou un mouvement normal (pion)
                            if isinstance(self.dictionnaire_pieces[position_source], Pion):
                                if position_cible in self.dictionnaire_pieces.keys():
                                    if Pion.peut_faire_une_prise_vers(self.dictionnaire_pieces[position_source], position_source, position_cible) is True:
                                        return True

                # Dans le cas ou la piece peut sauter (cavalier)
                else:
                    if self.couleur_piece_a_position(position_source) != self.couleur_piece_a_position(position_cible):
                        if self.recuperer_piece_a_position(position_source).peut_se_deplacer_vers(position_source, position_cible):
                            return True

        return False


    def deplacer(self, position_source, position_cible):
        """Effectue le déplacement d'une pièce en position source, vers la case en position cible. Vérifie d'abord
        si le déplacement est valide, et ne fait rien (puis retourne False) dans ce cas. Si le déplacement est valide,
        il est effectué (dans l'échiquier actuel) et la valeur True est retournée.

        Args:
            position_source (str): La position source.
            position_cible (str): La position cible.

        Returns:
            bool: True si le déplacement était valide et a été effectué, et False autrement.

        """
        if not self.deplacement_est_valide(position_source, position_cible):
            raise ExceptionDeplacer("Ce déplacement n'est pas valide")

        self.dictionnaire_pieces[position_cible] = self.dictionnaire_pieces[position_source]
        del self.dictionnaire_pieces[position_source]

    def roi_de_couleur_est_dans_echiquier(self, couleur):
        """Vérifie si un roi de la couleur reçue en argument est présent dans l'échiquier.

        Args:
            couleur (str): La couleur (blanc ou noir) du roi à rechercher.

        Returns:
            bool: True si un roi de cette couleur est dans l'échiquier, et False autrement.

        """

        if couleur == 'blanc':
            for i in self.dictionnaire_pieces:
                if isinstance(self.dictionnaire_pieces[i], Roi) is True:
                    if self.dictionnaire_pieces[i].est_blanc():
                        return True

        if couleur == 'noir':
            for i in self.dictionnaire_pieces:
                if isinstance(self.dictionnaire_pieces[i], Roi) is True:
                    if self.dictionnaire_pieces[i].est_noir():
                        return True

        return False


    def initialiser_echiquier_depart(self):
        """Initialise l'échiquier à son contenu initial. Pour faire vos tests pendant le développement,
        nous vous suggérons de vous fabriquer un échiquier plus simple, en modifiant l'attribut
        dictionnaire_pieces de votre instance d'Echiquier.

        """
        self.dictionnaire_pieces = {
            'a1': Tour('blanc'),
            'b1': Cavalier('blanc'),
            'c1': Fou('blanc'),
            'd1': Dame('blanc'),
            'e1': Roi('blanc'),
            'f1': Fou('blanc'),
            'g1': Cavalier('blanc'),
            'h1': Tour('blanc'),
            'a2': Pion('blanc'),
            'b2': Pion('blanc'),
            'c2': Pion('blanc'),
            'd2': Pion('blanc'),
            'e2': Pion('blanc'),
            'f2': Pion('blanc'),
            'g2': Pion('blanc'),
            'h2': Pion('blanc'),
            'a7': Pion('noir'),
            'b7': Pion('noir'),
            'c7': Pion('noir'),
            'd7': Pion('noir'),
            'e7': Pion('noir'),
            'f7': Pion('noir'),
            'g7': Pion('noir'),
            'h7': Pion('noir'),
            'a8': Tour('noir'),
            'b8': Cavalier('noir'),
            'c8': Fou('noir'),
            'd8': Dame('noir'),
            'e8': Roi('noir'),
            'f8': Fou('noir'),
            'g8': Cavalier('noir'),
            'h8': Tour('noir'),
        }

    def __repr__(self):
        """Affiche l'échiquier à l'écran. Utilise des codes Unicode, si la constante UTILISER_UNICODE est à True dans
        le module piece. Sinon, utilise seulement des caractères standards.

        Vous n'avez pas à comprendre cette partie du code.

        """
        chaine = ""
        if UTILISER_UNICODE:
            chaine += '  \u250c' + '\u2500\u2500\u2500\u252c' * 7 + '\u2500\u2500\u2500\u2510\n'
        else:
            chaine += '  +' + '----+' * 8 + '\n'

        for rangee in range(7, -1, -1):
            if UTILISER_UNICODE:
                chaine += '{} \u2502 '.format(self.chiffres_rangees[rangee])
            else:
                chaine += '{} | '.format(self.chiffres_rangees[rangee])
            for colonne in range(8):
                piece = self.dictionnaire_pieces.get('{}{}'.format(self.lettres_colonnes[colonne], self.chiffres_rangees[rangee]))
                if piece is not None:
                    if UTILISER_UNICODE:
                        chaine += str(piece) + ' \u2502 '
                    else:
                        chaine += str(piece) + ' | '
                else:
                    if UTILISER_UNICODE:
                        chaine += '  \u2502 '
                    else:
                        chaine += '   | '

            if rangee != 0:
                if UTILISER_UNICODE:
                    chaine += '\n  \u251c' + '\u2500\u2500\u2500\u253c' * 7 + '\u2500\u2500\u2500\u2524\n'
                else:
                    chaine += '\n  +' + '----+' * 8 + '\n'

        if UTILISER_UNICODE:
            chaine += '\n  \u2514' + '\u2500\u2500\u2500\u2534' * 7 + '\u2500\u2500\u2500\u2518\n'
        else:
            chaine += '\n  +' + '----+' * 8 + '\n'

        chaine += '    '
        for colonne in range(8):
            if UTILISER_UNICODE:
                chaine += self.lettres_colonnes[colonne] + '   '
            else:
                chaine += self.lettres_colonnes[colonne] + '    '
        chaine += '\n'
        return chaine


if __name__ == '__main__':
    echiquier = Echiquier()
    print(echiquier)
