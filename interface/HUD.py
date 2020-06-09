import webbrowser
import json
from tkinter import Canvas, Label, Tk, Button, LabelFrame, messagebox
from echecs.partie import Partie
from echecs.exceptions import ExceptionDeplacer, MauvaiseCouleur
from echecs.piece import Pion, Tour, Fou, Cavalier, Roi, Dame

# Variables globales utilisées
theme = '#4897c7'
theme_echiquier = '#74a6c4'
theme_selection = '#3d5869'
position = None
piece_mangee = {}
qte_pieces_avant = 0
qte_pieces_apres = 0


class CanvasEchiquier(Canvas):
    """Classe héritant d'un Canvas, et affichant un échiquier qui se redimensionne automatique lorsque
    la fenêtre est étirée.

    """
    def __init__(self, parent, n_pixels_par_case, partie, selection):
        # Nombre de lignes et de colonnes.
        self.n_lignes = 8
        self.n_colonnes = 8

        # Noms des lignes et des colonnes.
        self.chiffres_rangees = ['1', '2', '3', '4', '5', '6', '7', '8']
        self.lettres_colonnes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        # Nombre de pixels par case, variable.
        self.n_pixels_par_case = n_pixels_par_case

        # Importe les données de la partie et la sélection actuelle
        self.partie = partie
        self.position_selectionnee = selection

        # Appel du constructeur de la classe de base (Canvas).
        # La largeur et la hauteur sont déterminés en fonction du nombre de cases.
        super().__init__(parent, width=self.n_lignes * n_pixels_par_case,
                         height=self.n_colonnes * self.n_pixels_par_case)

        # On fait en sorte que le redimensionnement du canvas redimensionne son contenu. Cet événement étant également
        # généré lors de la création de la fenêtre, nous n'avons pas à dessiner les cases et les pièces dans le
        # constructeur.
        self.bind('<Configure>', self.redimensionner)

    def coordonnee_a_position(self, ligne, colonne):
        ligne = ligne // self.n_pixels_par_case
        colonne = colonne // self.n_pixels_par_case
        position = "{}{}".format(self.lettres_colonnes[colonne], int(self.chiffres_rangees[self.n_lignes - ligne - 1]))

        return position

    def dessiner_cases(self):
        """Méthode qui dessine les cases de l'échiquier.

        """
        for i in range(self.n_lignes):
            for j in range(self.n_colonnes):
                debut_ligne = i * self.n_pixels_par_case
                fin_ligne = debut_ligne + self.n_pixels_par_case
                debut_colonne = j * self.n_pixels_par_case
                fin_colonne = debut_colonne + self.n_pixels_par_case

                # On détermine la couleur.
                if position == self.coordonnee_a_position(debut_ligne, debut_colonne):
                    couleur = theme_selection
                elif (i + j) % 2 == 0:
                    couleur = 'white'
                else:
                    couleur = theme_echiquier

                # On dessine le rectangle. On utilise l'attribut "tags" pour être en mesure de récupérer les éléments
                # par la suite.
                self.create_rectangle(debut_colonne, debut_ligne, fin_colonne, fin_ligne, fill=couleur, tags='case')

    def dessiner_pieces(self):
        # Caractères unicode représentant les pièces. Vous avez besoin de la police d'écriture DejaVu.
        caracteres_pieces = {'Pion Blanc': '\u2659',
                             'Pion Noir': '\u265f',
                             'Tour Blanc': '\u2656',
                             'Tour Noir': '\u265c',
                             'Cavalier Blanc': '\u2658',
                             'Cavalier Noir': '\u265e',
                             'Fou Blanc': '\u2657',
                             'Fou Noir': '\u265d',
                             'Roi Blanc': '\u2654',
                             'Roi Noir': '\u265a',
                             'Dame Blanc': '\u2655',
                             'Dame Noir': '\u265b'
                             }

        # Pour tout paire position, pièce:
        for position, piece in self.partie.echiquier.dictionnaire_pieces.items():#self.pieces.dictionnaire_pieces.items():
            # On dessine la pièce dans le canvas, au centre de la case. On utilise l'attribut "tags" pour être en
            # mesure de récupérer les éléments dans le canvas.
            coordonnee_y = (self.n_lignes - self.chiffres_rangees.index(position[1]) - 1) * self.n_pixels_par_case + self.n_pixels_par_case // 2
            coordonnee_x = self.lettres_colonnes.index(position[0]) * self.n_pixels_par_case + self.n_pixels_par_case // 2
            self.create_text(coordonnee_x, coordonnee_y, text=caracteres_pieces[str(piece)],
                             font=('Deja Vu', self.n_pixels_par_case//2), tags='piece')

    def redimensionner(self, event):
        # Nous recevons dans le "event" la nouvelle dimension dans les attributs width et height. On veut un damier
        # carré, alors on ne conserve que la plus petite de ces deux valeurs.
        nouvelle_taille = min(event.width, event.height)

        # Calcul de la nouvelle dimension des cases.
        self.n_pixels_par_case = nouvelle_taille // self.n_lignes

        self.raffraichir_echiquier()

    def raffraichir_echiquier(self):
        # On supprime les anciennes cases et on ajoute les nouvelles.
        self.delete('case')
        self.dessiner_cases()

        # On supprime les anciennes pièces et on ajoute les nouvelles.
        self.delete('piece')
        self.dessiner_pieces()


class CanvasInformation(Canvas):
    def __init__(self, echiquier, partie, selection):
        super().__init__()

        # Importe la sélection actuelle, l'échiquier et les données de la partie
        self.position_selectionnee = selection
        self.echiquier = echiquier
        self.partie = partie

        # Crée le menu de partie affichant les données initiales
        self.annuler_boutton = Button(self, text="Annuler dernier déplacement", command=self.annuler_deplacement, bg=theme, relief='ridge', bd=3)
        self.annuler_boutton.grid(row=4, column=0)

        self.vide_label = LabelFrame(self)
        self.vide_label.grid(row=5, column=0, pady=20)

        self.nouvelle_boutton = Button(self, text="Nouvelle partie", command=self.nouvelle, bg=theme, relief='ridge', bd=3)
        self.nouvelle_boutton.grid(row=6, column=0)

        self.charger_boutton = Button(self, text="Charger une partie", command=self.charger, bg=theme, relief='ridge', bd=3)
        self.charger_boutton.grid(row=7, column=0)

        self.sauvegarder_boutton = Button(self, text="Sauvegarder la partie", command=self.sauvegarder, bg=theme, relief='ridge', bd=3)
        self.sauvegarder_boutton.grid(row=8, column=0)

        self.vide_label = LabelFrame(self)
        self.vide_label.grid(row=9, column=0, pady=20)

        self.quit_button = Button(self, text="Historique des déplacements", command=self.afficher_historique, bg=theme, relief='ridge', bd=3)
        self.quit_button.grid(row=10, column=0, sticky='s')

        self.quit_button = Button(self, text=" Ouvrir menu principal", command=self.retour_menu, bg=theme, relief='ridge', bd=3)
        self.quit_button.grid(row=11, column=0, sticky='s')

    def retour_menu(self):
        self.destroy()

    def raffraichir_info(self):
        self.boite_dialogue.destroy()
        self.chrono_blanc.destroy()
        self.chrono_noir.destroy()

        self.load_info()

    def load_info(self):
        # Ajout de la boite de dialogue.
        self.boite_dialogue = LabelFrame(self, text=f"Au tour du joueur {self.partie.joueur_actif}", relief="ridge", font='20')
        self.boite_dialogue.grid(row=0, column=0)

        self.messages = Label(self.boite_dialogue, text="Choisissez votre pièce")
        self.messages.pack()

        self.vide = LabelFrame(self)
        self.vide.grid(row=1, column=0, pady=40)

        self.chrono_noir = Label(self, text=f"Temps total du joueur noir:\n{self.partie.temps_str_noir}")
        self.chrono_noir.grid(row=1, column=0)
        self.chrono_blanc = Label(self, text=f"Temps total du joueur blanc:\n{self.partie.temps_str_blanc}")
        self.chrono_blanc.grid(row=2, column=0)

    def annuler_deplacement(self):
        # Ouvre le fichier et retrouve les positions souhaitées (à la dernière ligne)
        with open('historique.txt', 'r') as historique:
            # Trouve la dernière ligne de l'historique et y récupère les informations sur le tour précédent
            for derniere_ligne in historique:
                pass
            derniere_ligne = derniere_ligne.strip()
            derniere_ligne = derniere_ligne.split(' ')
            position_a_retrouver = derniere_ligne[-3]
            position_actuelle = derniere_ligne[-1]

            # Déplace la pièce à sa position antérieure
            self.partie.echiquier.dictionnaire_pieces[position_a_retrouver] = self.partie.echiquier.dictionnaire_pieces[position_actuelle]
            del self.partie.echiquier.dictionnaire_pieces[position_actuelle]

            # Repasse au joueur précédent
            self.partie.joueur_suivant()

        if qte_pieces_avant != qte_pieces_apres:
            # Rajoute la piece précédemment mangée
            self.partie.echiquier.dictionnaire_pieces[position_actuelle] = piece_mangee[position_actuelle]

        # Indique qu'un déplacement a été annulé
        with open('historique.txt', 'a') as historique:
            historique.write('DÉPLACEMENT ANNULÉ\n')
        # Raffraichit l'affichage
        self.raffraichir_info()
        self.echiquier.raffraichir_echiquier()

    def nouvelle(self):
        reponse = messagebox.askquestion("Création d'une nouvelle partie...", "Voulez-vous sauvegarder avant de commencer une autre partie?")
        if reponse == 'yes':
            self.sauvegarder()

        # Remet tout à zéro
        self.partie.echiquier.initialiser_echiquier_depart()
        self.partie.joueur_actif = 'blanc'
        self.position_selectionnee = None
        self.supprimer_historique()

        self.partie.temps_total_blanc = 0
        self.partie.temps_total_noir = 0

        self.partie.chrono_blanc_debut = 0
        self.partie.chrono_noir_debut = 0

        self.partie.chrono_blanc_fin = 0
        self.partie.chrono_noir_fin = 0

        self.partie.temps_str_blanc = '-'
        self.partie.temps_str_noir = '-'

        self.raffraichir_info()
        self.echiquier.raffraichir_echiquier()

    def charger(self):
        reponse = messagebox.askquestion("Chargement d'une partie...", "Voulez-vous sauvegarder avant de charger une autre partie?")
        if reponse == 'yes':
            self.sauvegarder()

        nom_fichier = input("Entrez un nom de sauvegarde à charger: ")
        with open(nom_fichier, "r") as file:
            dic = json.load(file)
            piece = dic['piece']
            joueur = dic['joueur']
            temps_blanc = dic['temps_blanc']
            temps_noir = dic['temps_noir']

            table = {'Pion' : Pion, 'Tour': Tour, 'Cavalier': Cavalier, 'Fou': Fou, 'Roi': Roi, 'Dame': Dame}
            dic_cls = {}
            for i in piece:
                clsname, color = piece[i].split()
                cls = table[clsname]
                color = color.lower()
                instance = cls(color)
                dic_cls[i] = instance

            # Charge les différentes composantes de la partie
            self.partie.echiquier.dictionnaire_pieces = dic_cls
            self.partie.joueur_actif = joueur

            self.partie.temps_total_blanc = temps_blanc
            self.partie.temps_total_noir = temps_noir
            self.partie.temps_str_blanc = self.partie.temps_total_a_string(temps_blanc)
            self.partie.temps_str_noir = self.partie.temps_total_a_string(temps_noir)

            self.raffraichir_info()
            self.echiquier.raffraichir_echiquier()

    def sauvegarder(self):
        nom_fichier = input("Entrez un nom pour la sauvegarde: ")
        dic_piece = self.partie.echiquier.dictionnaire_pieces
        ser_piece = {}
        for piece in dic_piece:
            ser_piece[piece] = str(dic_piece[piece])

        # Sauvegarde les différentes composantes de la partie dans un dictionnaire, puis enregistre ce dictionnaire dans un fichier
        ser_joueur = self.partie.joueur_actif
        temps_blanc = self.partie.temps_total_blanc
        temps_noir = self.partie.temps_total_noir
        dic = {'piece': ser_piece, 'joueur': ser_joueur, 'temps_blanc': temps_blanc, 'temps_noir': temps_noir}

        with open(nom_fichier, "w") as file:
            json.dump(dic, file)

    @staticmethod
    def afficher_historique():
        with open('historique.txt', 'r') as historique:
            info_deplacement = ""
            for ligne in historique:
                info_deplacement += ligne.strip() + '\n'
            messagebox.showinfo(title="Historique des déplacements", message=info_deplacement)

    @staticmethod
    def supprimer_historique():
        with open('historique.txt', 'w') as historique:
            historique.write('')


class CanvasMenuPrincipal(Canvas):
    def __init__(self, partie, echiquier):
        super().__init__()

        # Importe les données de la partiem l'échiquier et load l'affichage du menu
        self.echiquier = echiquier
        self.partie = partie
        self.load_menu()

    def load_menu(self):
        self.bienvenue_label = Label(self, text="Bienvenue!", bg=theme, font='20', relief='ridge')
        self.bienvenue_label.grid(row=0, column=0, ipadx=30, ipady=0, sticky='n')

        self.vide_label = LabelFrame(self)
        self.vide_label.grid(row=1, column=0, pady=10)

        self.style_label = Label(self, text="Choisissez votre style graphique:")
        self.style_label.grid(row=2, column=0, sticky='w')

        self.theme1 = Button(self, text="Bleu", command=self.theme_1, bg='#4897c7', relief='ridge')
        self.theme2 = Button(self, text="Rouge", command=self.theme_2, bg='#b85a5a', relief='ridge')
        self.theme3 = Button(self, text="Mauve", command=self.theme_3, bg='#8d79b3', relief='ridge')
        self.theme1.grid(row=3, column=0, sticky="w")
        self.theme2.grid(row=4, column=0, sticky="w")
        self.theme3.grid(row=5, column=0, sticky="w")

        self.vide_label = LabelFrame(self)
        self.vide_label.grid(row=6, column=0, pady=20)

        self.nouvelle_button = Button(self, text="Continuer / Commencer le jeu", command=self.commencer_jeu, bg=theme, relief='ridge', bd=3)
        self.nouvelle_button.grid(row=7, column=0, ipady=10)

        self.vide_label = LabelFrame(self)
        self.vide_label.grid(row=8, column=0, pady=30)

        self.regles_button = Button(self, text="Voir les règlements du jeu d'échec", command=self.reglements, bg=theme, relief='ridge', bd=3)
        self.regles_button.grid(row=9, column=0)

        self.coffin_button = Button(self, text="Et si par malheur je perds?", command=self.coffin, bg=theme, relief='ridge', bd=3)
        self.coffin_button.grid(row=10, column=0)

        self.vide_label = LabelFrame(self)
        self.vide_label.grid(row=11, column=0)

        self.quit_button = Button(self, text="Quitter le jeu", command=self.on_close, bg=theme, relief='ridge', bd=3)
        self.quit_button.grid(row=12, column=0, sticky='s')

    def raffraichir_menu(self):
        self.bienvenue_label.destroy()
        self.nouvelle_button.destroy()
        self.regles_button.destroy()
        self.coffin_button.destroy()
        self.quit_button.destroy()

        self.load_menu()

    def on_close(self):
        reponse = messagebox.askquestion("Fermeture du jeu...", "Voulez-vous sauvegarder avant de quitter?")
        if reponse == 'yes':
            self.partie.canvas_information.sauvegarder()
            self.quit()
        if reponse == 'no':
            self.quit()

    def commencer_jeu(self):
        Fenetre.afficher_partie(self.partie)

    def theme_1(self):
        global theme
        global theme_echiquier
        global theme_selection
        theme_selection = '#3d5869'
        theme_echiquier = '#74a6c4'
        theme = '#4897c7'

        self.raffraichir_menu()
        self.echiquier.raffraichir_echiquier()

    def theme_2(self):
        global theme
        global theme_echiquier
        global theme_selection
        theme_selection = '#664141'
        theme_echiquier = '#b07272'
        theme = '#b85a5a'

        self.raffraichir_menu()
        self.echiquier.raffraichir_echiquier()

    def theme_3(self):
        global theme
        global theme_echiquier
        global theme_selection
        theme_selection = '#52436b'
        theme_echiquier = '#9382d1'
        theme = '#8d79b3'

        self.raffraichir_menu()
        self.echiquier.raffraichir_echiquier()

    @staticmethod
    def reglements():
        webbrowser.open('https://www.instructables.com/id/Playing-Chess/')

    @staticmethod
    def coffin():
        webbrowser.open('https://www.youtube.com/watch?v=qgDCM91f7NY')


class Fenetre(Tk):
    def __init__(self):
        super().__init__()

        # Quelques paramètres d'initialisation
        self.title("Jeu d'échec IFT-1004")

        self.partie = Partie()
        self.position_selectionnee = None
        self.supprimer_historique()

        self.canvas_echiquier = CanvasEchiquier(self, 60, self.partie, self.position_selectionnee)
        self.canvas_echiquier.grid(row=0, column=0)

        self.afficher_menu_principal()

        # Truc pour le redimensionnement automatique des éléments de la fenêtre.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def afficher_menu_principal(self):
        self.canvas_menu_principal = CanvasMenuPrincipal(self, self.canvas_echiquier)
        self.canvas_menu_principal.grid(row=0, column=1, padx=50, pady=50)

    def afficher_partie(self):
        # Création du canvas d'information.
        self.canvas_information = CanvasInformation(self.canvas_echiquier, self.partie, self.position_selectionnee)
        self.canvas_information.load_info()
        self.canvas_information.grid(row=0, column=1)

        self.canvas_echiquier.bind('<Button-1>', self.selectionner)

    def selectionner(self, event):
        # On trouve le numéro de ligne/colonne en divisant les positions en y/x par le nombre de pixels par case.
        ligne = event.y // self.canvas_echiquier.n_pixels_par_case
        colonne = event.x // self.canvas_echiquier.n_pixels_par_case
        global position
        position = "{}{}".format(self.canvas_echiquier.lettres_colonnes[colonne], int(self.canvas_echiquier.chiffres_rangees[self.canvas_echiquier.n_lignes - ligne - 1]))
        self.canvas_information.raffraichir_info()

        # Si aucune position sélectionnée
        if self.position_selectionnee is None:
            try:
                piece = self.canvas_echiquier.partie.echiquier.dictionnaire_pieces[position]
                self.position_selectionnee = position
                # si la piece sélectionnée appartient au joueur
                if self.canvas_echiquier.partie.echiquier.couleur_piece_a_position(position) == self.partie.joueur_actif:
                    self.messages = Label(self.canvas_information.boite_dialogue, text='Pièce sélectionnée : {} à la position {}.'.format(piece, self.position_selectionnee))
                    self.messages.pack()
                else:
                    self.messages = Label(self.canvas_information.boite_dialogue, text="Ce n'est pas votre pièce", fg="dark red")
                    self.messages.pack()
                    self.position_selectionnee = None
                    position = None
                    self.canvas_echiquier.raffraichir_echiquier()
                    raise MauvaiseCouleur

            except KeyError:
                self.messages = Label(self.canvas_information.boite_dialogue, text="Aucune pièce à cet endroit.", fg="dark red")
                self.messages.pack()
                self.position_selectionnee = None
                position = None
                self.canvas_echiquier.raffraichir_echiquier()

        # Si c'est le deuxième clic
        else:
            if self.position_selectionnee == position:
                self.position_selectionnee = None
                position = None
                self.canvas_echiquier.raffraichir_echiquier()
            else:
                try:
                    global piece_mangee
                    global qte_pieces_avant
                    global qte_pieces_apres

                    # Bloc qui prend en compte si le déplacement a mangé un pion ou pas
                    piece_mangee = {}
                    qte_pieces_avant = len(self.partie.echiquier.dictionnaire_pieces)
                    if self.partie.echiquier.recuperer_piece_a_position(position):
                        piece_mangee[position] = self.partie.echiquier.recuperer_piece_a_position(position)
                    self.partie.deplacer_piece(self.position_selectionnee, position)
                    qte_pieces_apres = len(self.partie.echiquier.dictionnaire_pieces)
                    # Différents messages selon si une pièce mange ou pas
                    if qte_pieces_avant != qte_pieces_apres:
                        self.sauvegarder_historique_mange(self.canvas_echiquier.partie.echiquier.dictionnaire_pieces[position], piece_mangee[position], self.position_selectionnee, position)
                    else:
                        self.sauvegarder_historique(self.canvas_echiquier.partie.echiquier.dictionnaire_pieces[position], self.position_selectionnee, position)

                    self.canvas_information.raffraichir_info()

                    self.position_selectionnee = None
                    position = None
                    self.canvas_echiquier.raffraichir_echiquier()

                    # Regarde si la partie est terminée
                    if self.canvas_echiquier.partie.partie_terminee():
                        self.messages = Label(self.canvas_information.boite_dialogue, text=f"Partie terminée\n Bravo {self.partie.determiner_gagnant()}!", fg="dark red")
                        self.gagnant = messagebox.showinfo(title='Partie Terminée!', message=f"Partie terminée\n Bravo joueur {self.partie.determiner_gagnant()}!")
                        self.messages.pack()
                        self.canvas_echiquier.bind = self.canvas_echiquier.unbind('<Button-1>')
                # Exception si le déplacement ne peut être effectué
                except ExceptionDeplacer:
                    self.messages = Label(self.canvas_information.boite_dialogue, text="Déplacement invalide", fg="dark red")
                    self.messages.pack()
                    self.position_selectionnee = None
                    position = None
                    self.canvas_echiquier.raffraichir_echiquier()

        self.canvas_echiquier.raffraichir_echiquier()

    @staticmethod
    def sauvegarder_historique(piece, depart, arrivee):
        with open('historique.txt', 'a') as historique:
            historique.write(f'{piece} de {depart} vers {arrivee}\n')

    @staticmethod
    def sauvegarder_historique_mange(piece_deplacee, piece_mangee, depart, arrivee):
        with open('historique.txt', 'a') as historique:
            historique.write(f'{piece_deplacee} MANGE {piece_mangee} de {depart} vers {arrivee}\n')

    @staticmethod
    def supprimer_historique():
        with open('historique.txt', 'w') as historique:
            historique.write('')


if __name__ == "__main__":
    Fenetre().mainloop()
