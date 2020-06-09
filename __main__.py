# -*- coding: utf-8 -*-
"""Module principal du package pychecs2. C'est ce module que nous allons exécuter pour démarrer votre jeu.
Importez les modules nécessaires et démarrez votre programme à partir d'ici. Le code fourni n'est qu'à titre d'exemple.

"""
from echecs.partie import Partie
from interface.HUD import Fenetre

if __name__ == '__main__':
    # Création d'une instance de Partie.
    p = Partie()

    # Création et affichage d'une fenêtre (aucun lien avec la partie ci-haut).
    Fenetre().mainloop()
