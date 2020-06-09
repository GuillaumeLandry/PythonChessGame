# -*- coding: utf-8 -*-
"""Ce module contient une classe contenant les informations sur une partie d'échecs,
dont un objet échiquier (une instance de la classe Echiquier).

"""
from pychecs2.echecs.echiquier import Echiquier
from pychecs2.echecs.exceptions import AucunePiece, MauvaiseCouleur
import time


class Partie:
    """La classe Partie contient les informations sur une partie d'échecs, c'est à dire un échiquier, puis
    un joueur actif (blanc ou noir). Des méthodes sont disponibles pour faire avancer la partie et interagir
    avec l'utilisateur.

    La classe partie gère également les chronomètres des joueurs. Sachant que chaque joueur bénificie de son premier tour
    sans compteur de temps, les chronos de chaque joueurs commencent à leur deuxième tour.

    """

    def __init__(self):
        # Le joueur débutant une partie d'échecs est le joueur blanc.
        self.joueur_actif = 'blanc'

        # Création d'une instance de la classe Echiquier, qui sera manipulée dans les méthodes de la classe.
        self.echiquier = Echiquier()

        # Création des variables nécessaires pour la gestion du chronomètre
        self.temps_total_blanc = 0
        self.temps_total_noir = 0

        self.chrono_blanc_debut = 0
        self.chrono_noir_debut = 0

        self.chrono_blanc_fin = 0
        self.chrono_noir_fin = 0

        self.temps_str_blanc = '-'
        self.temps_str_noir = '-'

    def determiner_gagnant(self):
        """Détermine la couleur du joueur gagnant, s'il y en a un. Pour déterminer si un joueur est le gagnant,
        le roi de la couleur adverse doit être absente de l'échiquier.

        Returns:
            str: 'blanc' si le joueur blanc a gagné, 'noir' si c'est plutôt le joueur noir, et 'aucun' si aucun
                joueur n'a encore gagné.

        """

        if self.echiquier.roi_de_couleur_est_dans_echiquier('blanc') is False:
            return 'noir'

        if self.echiquier.roi_de_couleur_est_dans_echiquier('noir') is False:
            return 'blanc'

        return 'aucun'

    def partie_terminee(self):
        """Vérifie si la partie est terminée. Une partie est terminée si un gagnant peut être déclaré.

        Returns:
            bool: True si la partie est terminée, et False autrement.

        """

        if self.determiner_gagnant() != 'aucun':
            return True

        return False

    def deplacer_piece(self, position_source, position_cible):
        """Effectue le déplacement d'une pièce en position source, vers la case en position cible.

        Args:
            position_source (str): La position source.
            position_cible (str): La position cible.
        """
        piece = self.echiquier.recuperer_piece_a_position(position_source)

        if piece is None:
            raise AucunePiece("Il n'y a pas de pièce à cette position")
        elif piece.couleur != self.joueur_actif:
            raise MauvaiseCouleur("Cette pièce ne vous appartient pas")

        self.echiquier.deplacer(position_source, position_cible)

        self.joueur_suivant()

    def joueur_suivant(self):
        """Change le joueur actif: passe de blanc à noir, ou de noir à blanc, selon la couleur du joueur actif.
           Gère du même coup les chronomètres utilisés pour suivre les temps de jeu des joueurs.

        """
        # Lorsque le jour passe de blanc à noir
        if self.joueur_actif == 'blanc':
            self.joueur_actif = 'noir'

            # Départ du chrono noir
            self.chrono_noir_debut = time.time()

            if self.chrono_blanc_fin == 0:
                self.chrono_blanc_fin = time.time()
            else:
                # Arrêt du chrono blanc
                self.chrono_blanc_fin = time.time()
                # Création de l'affichage du temps
                self.temps_total_blanc += self.chrono_blanc_fin - self.chrono_blanc_debut
                self.temps_str_blanc = self.temps_total_a_string(float(self.temps_total_blanc))
                # Reset des chronos blanc
                self.chrono_blanc_debut = 0
                self.chrono_blanc_fin = 0

        # Lorsque le jour passe de noir à blanc
        elif self.joueur_actif == 'noir':
            self.joueur_actif = 'blanc'

            # Départ du chrono blanc
            self.chrono_blanc_debut = time.time()

            if self.chrono_noir_fin == 0:
                self.chrono_noir_fin = time.time()
            else:
                # Arrêt du chrono noir
                self.chrono_noir_fin = time.time()
                # Création de l'affichage du temps
                self.temps_total_noir += self.chrono_noir_fin - self.chrono_noir_debut
                self.temps_str_noir = self.temps_total_a_string(float(self.temps_total_noir))
                # Reset des chronos noir
                self.chrono_noir_debut = 0
                self.chrono_noir_fin = 0

    @staticmethod
    def temps_total_a_string(temps):
        """Transforme les chronomètres, qui comptent les secondes avec une grande précision, en un affichage prêt
           à être affiché dans le jeu.

        """
        # Formate les heures, minutes, secondes pour l'affichage
        heures = round(temps // 3600)
        temps = temps - 3600 * heures
        minutes = round(temps // 60)
        secondes = round(temps - 60 * minutes, 1)

        # Différents affichages selon le temps passé
        if minutes == 0 and heures == 0:
            return f"{secondes} sec"

        elif heures == 0:
            return f"{minutes} min {secondes} sec"

        else:
            return f"{heures} hr {minutes} min {secondes} sec"
