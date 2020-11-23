#!/usr/bin/python3
# -*- coding: utf-8 -*-

from random import *
from tkinter import *
import time
import os


class Cellule:

    def __init__(self, valeur):
        """
        Fonction constructeur __init__ : False = cellule morte ; True = cellule vivante
        """
        self._actuel = valeur
        self._futur = False
        self._voisins = None


    def set_actuel(self, valeur):
        self._actuel = valeur

    def est_vivant(self):
        return self._actuel

    def set_voisins(self, liste_voisins):
        self._voisins = liste_voisins

    def get_voisins(self):
        return self._voisins

    def naitre(self):
        self._futur = True    # Donne naissance à une cellule

    def mourir(self):
        self._futur = False     # Donne la mort d'une cellule

    def basculer(self):
        self._actuel = self._futur

    def calcule_etat_future(self):
        """
        Fontion calcule_etat_future : Calcule l'état future de la cellule avec les règles du jeu
        - Si une cellule est vivante, elle le reste si elle possède 2 ou 3 voisines vivantes et meurt sinon
        - Si une cellule est morte, elle devient vivante si elle possède exactement 3 voisines vivantes.
        """
        vivante = 0
        for i in self.get_voisins():     # [(i, j, bool), ....]
            if i[2]:    # Comptage nombre de voisins en vie
                vivante += 1
        if self.est_vivant():   # Si cellule est vivante
            if 2 == vivante or vivante == 3:    # Si elle à 2 ou 3 voisines vivantes
                self.naitre()
            else:
                self.mourir()
        else:
            if vivante == 3:
                self.naitre()
            else:
                self.mourir()


class Grille:
    def __init__(self):
        """
        Fonction constructeur __init__
        """

        self.dico = {}  # De la forme {(i,j):objet cellule;...}
        self.taille_cellule = 10
        self.hauteur_grille = 500
        self.largeur_grille = 500
        self.largeur = self.largeur_grille // self.taille_cellule
        self.hauteur = self.hauteur_grille // self.taille_cellule
        self.taux = 20

    def remplir_vide(self):
        """
        Remplit la grille à vide, tout est mort
        """
        for j in range(self.get_hauteur()):
            for i in range(self.get_largeur()):
                tpl = (i, j)
                self.dico[tpl] = Cellule(False)

    def remplir_alea(self):
        """
        Fonction qui remplit aleatoirement la grille de cellule vivante et morte. Le nombre de cellule vivante est
        défini par un taux. Enfin, un algorithme plus complexe permet de faire un aléatoire propre (ex: que 10 cellules
        vivantes sur 100 ne soient pas que dans les 30 première, mais éparpiller partout
        """
        self.dico = {}
        vivante = 0
        morte = 0
        nb_cellule = self.get_largeur() * self.get_hauteur()    # Nb de cellule dans la grille
        nb_vivante = int((self.taux * nb_cellule) / 100)             # Nb cellule vivante dans la grille
        nb_morte = int(nb_cellule - nb_vivante)                 # Nb cellule morte dans la grille
        random = 10000 - (self.taux * 100)                      # nb définis pour un aléatoire 'propre'
        for j in range(self.get_hauteur()):
            for i in range(self.get_largeur()):
                if vivante < nb_vivante and morte < nb_morte:   # Dans le cas ou l'on a pas assez de vivante et de morte
                    r = randint(0, 10000)   # Dans certains, 2000 donnera une vivante, et d'en d'autre, une morte
                    if r >= random:
                        r = True
                        vivante += 1
                    else:
                        r = False
                        morte += 1
                    tpl = (i, j)    # tuple Coordonnees
                    self.dico[tpl] = Cellule(r)     # Instanciation objet Cellule
                elif vivante < nb_vivante:
                    tpl = (i, j)
                    self.dico[tpl] = Cellule(True)
                    vivante += 1
                elif morte < nb_morte:
                    tpl = (i, j)
                    self.dico[tpl] = Cellule(False)
                    morte += 1
        self.afficher_case_noir()   # Affichage grille à l'écran

    def get_8_voisin(self, i, j):
        """
        Trouve les 8 voisins (ou moins) de chaque cellule suivant ce principe :

        (x-1,y+1)  (x,y+1)  (x+1,y+1)
         (x-1,y)    (x,y)    (x+1,y)
        (x-1,y-1)  (x,y-1)  (x+1,y-1)

        On verif à chaque fois que la point est dans la grille avec self.dans_grille,
        Puis un chek si le point est bien voisin de l'autres avec self.est_voisin
        """
        liste_voisins = []
        r = 1  # Le fameux 1 dans x+1, y-1, y+1 ...
        for h in range(-1, 2):  # pour x = -1 et y = -1, 0, et 1 (ligne du bas)
            if self.dans_grille(i + r, j + h) and self.est_voisin(i, j, i + r, j + h):
                tupl = (i + r, j + h, self.getXY(i + r, j + h)._actuel)
                liste_voisins.append(tupl)
        for h in range(-1, 2):  # Ligne du milieu
            if self.dans_grille(i - r, j + h) and self.est_voisin(i, j, i - r, j + h):
                tupl = (i - r, j + h, self.getXY(i - r, j + h)._actuel)
                liste_voisins.append(tupl)
        for h in range(-1, 2, 2):  # ligne du haut
            if self.dans_grille(i, j + h) and self.est_voisin(i, j, i, j + h):
                tupl = (i, j + h, self.getXY(i, j + h)._actuel)
                liste_voisins.append(tupl)
        return liste_voisins

    def dans_grille(self, x, y):
        """
        Vérifie que (x,y) est dans la grille.
        Le try est utile car si on cherche quelque chose qui n'existe pos, l'erreur est renvoyer. Ici, grace a try,
        si une erreur que le point est introuvable, alors il est pas dans la grille. on return False
        """
        tpl = (x, y)
        try:
            if self.dico[tpl] or not self.dico[tpl]:
                return True
        except:
            return False

    @staticmethod
    def est_voisin(i, j, x, y):
        """
        Vérifie que (i, j) à bien (x, y) comme voisin
        """
        if x == i and (y == j + 1 or y == j - 1):   # Trois cellules du haut
            return True
        elif x == i - 1 and (y == j + 1 or y == j - 1 or y == j):   # Cellules droite et gauche
            return True
        elif x == i + 1 and (y == j + 1 or y == j - 1 or y == j):   # Trois cellules du bas
            return True
        else:
            return False

    def getXY(self, i, j):
        """
        Récupere l'objet cellule au coordonnées (i, j)
        """
        tpl = (i, j)
        return self.dico[tpl]


    def get_largeur(self):
        return self.largeur

    def get_hauteur(self):
        return self.hauteur

    def Jeu(self):
        """
        Calcule les voisins de chaque cellules, son état future
        """
        for cle, valeur in self.dico.items():
            valeur.set_voisins(self.get_8_voisin(cle[0], cle[1]))
            valeur.calcule_etat_future()
        self.actualiser()

    def actualiser(self):
        """
        Passe l'état future à l'état suivant
        """
        for cle, valeur in self.dico.items():
            valeur.basculer()


    '''_______________ Tkinter ________________'''

    def damier(self):  # fonction dessinant le tableau
        self.ligne_vertical()
        self.ligne_horizontale()

    def ligne_vertical(self):   # Dessine les lignes verticals
        c_x = 0
        while c_x != self.largeur_grille:
            can1.create_line(c_x, 0, c_x, self.hauteur_grille, width=1, fill='black')
            c_x += self.taille_cellule

    def ligne_horizontale(self):    # Dessine les lignes horizontales
        c_y = 0
        while c_y != self.hauteur_grille:
            can1.create_line(0, c_y, self.largeur_grille, c_y, width=1, fill='black')
            c_y += self.taille_cellule

    def afficher_case_noir(self):
        """
        Affiche case noir : Les cellule vivantes sont affiché en noir
        """
        for cle, valeur in self.dico.items():
            if valeur._actuel:
                x = cle[0] * 10     # * 10 car les cellules physique font 10*10
                y = cle[1] * 10
                can1.create_rectangle(x, y, x + g.taille_cellule, y + g.taille_cellule, fill='black')
            elif not valeur._actuel:
                x = cle[0] * 10
                y = cle[1] * 10
                can1.create_rectangle(x, y, x + g.taille_cellule, y + g.taille_cellule, fill='white')


def click_droit(event):
    """
    Si on clique droit, on récupere les coordonnées du curseur, et on modifie la valeur de la cellule à cet endroit
    """
    x = event.x - (event.x % g.taille_cellule)
    y = event.y - (event.y % g.taille_cellule)
    can1.create_rectangle(x, y, x + g.taille_cellule, y + g.taille_cellule, fill='white')
    for cle, valeur in g.dico.items():
        if cle[0] == x // 10 and cle[1] == y // 10:
            valeur.set_actuel(False)


def click_gauche(event):
    """
    Si on clique gauche, on récupere les coordonnées du curseur, et on modifie la valeur de la cellule à cet endroit
    """
    x = event.x - (event.x % g.taille_cellule)
    y = event.y - (event.y % g.taille_cellule)
    can1.create_rectangle(x, y, x + g.taille_cellule, y + g.taille_cellule, fill='black')
    for cle, valeur in g.dico.items():
        if cle[0] == x // 10 and cle[1] == y // 10:
            valeur.set_actuel(True)


def redessiner():
    """
    Efface la canvas et redessine un nouveau damier, et réafiche les cases noires
    """
    can1.delete(ALL)
    g.damier()
    g.afficher_case_noir()


def alea():
    """
    Génération aléatoire de la grille avec le taux récupérer du scale
    """
    g.taux = scale_taux.get()
    g.remplir_alea()


def vitesse():
    """
    Définition de la vitesse avec le taux récupérer du scale
    """
    global speed
    speed = scale_vitesse.get() // 60


def go():
    """
    Lance le jeu
    """
    global flag, nb_gen, speed
    while flag == 0:
        nb_gen += 1
        gen.config(text="Nombres générations :  " + str(nb_gen))
        g.Jeu()
        redessiner()
        return fen1.after(1000//speed, go)  # Relance la fonction avec delai


def relancer():
    """
    Modifier valeur de flag pour relancer
    """
    global flag
    flag = 0
    go()


def stop(value):
    """
    Stop le jeu
    """
    global flag
    flag = value


def pause(a):
    """
    Met le jeu en pose quand on appuie sur espace, et la relance si on réappuie
    """
    global nb_pause
    global flag
    nb_pause += 1
    if nb_pause % 2 == 0:
        relancer()
    else:
        stop(1)


def vider():
    """
    Relance la jeu de 0, Tout le monde prend la valeur False
    """
    global nb_gen
    g.remplir_vide()
    redessiner()
    nb_gen = 0


if __name__=='__main__':
    flag = 0  # 0 = arret, 1 = marche
    nb_pause = 0
    nb_gen = 0
    speed = 1
    color = '#1B1A1A'
    color_text = '#E7AE09'
    instruction = "Le jeu de la vie est un" + "\n" + "automate cellulaire imaginé" + "\n" + "par John Horton Conway" + \
                  "\n" + "en 1970. Il répond à ces" + "\n" + "critères :" + "\n" + "\n" + "- une cellule vivante reste" \
                  + "\n" + "vivante si elle est entourée" + "\n" + "de 2 ou 3 voisines vivantes" + "\n" + "et meurt sinon." \
                  + "\n" + "\n" + "- une cellule morte devient" + "\n" + "vivante si elle possède" + "\n" + \
                  "exactement 3 voisines" + "\n" + "vivantes."+ "\n" + "\n" + "\n" + "Démarrer => Lance la" + "\n" + \
                  "            simulation" + "\n" + "\n" + "Vider => Vide la grille" + "\n" + "" + "\n" + "\n" + \
                  "Vitesse => Valide la vitesse" + "\n" + "           séléctionnée" + "\n" + "\n" + "Aléatoire => Génération " \
                  + "\n" + "             aléatoire de la" + "\n" + "             grille avec le" + "\n" + \
                  "             taux sélectionné" + "\n" + "" + "\n" + "\n" + "Clique gauche => Donner" + "\n" + \
                  "                 naissance à" + "\n" + "                 une cellule" + "\n" + "\n" + "Clique droit => Tuer une" + "\n" + "cellule"



    g = Grille()        # Instantiation Grille
    g.remplir_vide()    # Remplissage avec tout cellules mortes


    fen1 = Tk()
    fen1.geometry('1000x800')   # Taille fenetre
    fen1.configure(bg=color)
    fen1.winfo_pointerxy()
    fen1.bind('<space>', pause)

    can1 = Canvas(fen1, width=g.largeur_grille, height=g.hauteur_grille, bg='white')    # Création canvas
    can1.bind("<Button-3>", click_droit)    # écoute les actions de la souris
    can1.bind("<Button-1>", click_gauche)
    can1.place(x=243, y=200)

    g.damier()  # Création damier

    """______________________________ Zones de texte ____________________________________"""

    titre = Label(fen1, text="Jeu de la Vie", bg=color, fg=color_text)
    titre.config(font=("Lucida Console", 44))
    titre.place(x=260, y=40)

    gen = Label(fen1, text="Nombres générations :  " + str(nb_gen), bg=color, fg=color_text)
    gen.config(font=("Lucida Console", 25), text="Nombres générations :  " + str(nb_gen))
    gen.place(x=240, y=730)

    ins = Label(fen1, text=instruction, bg=color, fg=color_text, justify='left', bd=0)
    ins.config(font=("Lucida Console", 10))
    ins.place(x=5, y=200)

    """______________________________ Boutons ____________________________________"""

    b1 = Button(fen1, text='Démarrer', command=go, bg=color, fg=color_text, width=10)
    b1.config(font=("Lucida Console", 20))
    b1.place(x=800, y=240)

    b2 = Button(fen1, text='Vider', command=vider, bg=color, fg=color_text, width=10)
    b2.config(font=("Lucida Console", 20))
    b2.place(x=800, y=300)

    b3 = Button(fen1, text='Aléatoire', command=alea, bg=color, fg=color_text, width=10)
    b3.config(font=("Lucida Console", 20))
    b3.place(x=800, y=420)

    b4 = Button(fen1, text='vitesse', command=vitesse, bg=color, fg=color_text, width=10)
    b4.config(font=("Lucida Console", 20))
    b4.place(x=800, y=360)

    """______________________________ Scale ____________________________________"""
    scale_taux = Scale(fen1, orient='horizontal', bg=color, fg=color_text, highlightthickness=0, from_=0, to=100, resolution=1, length=168, label='       Taux %', bd=0)
    scale_taux.config(font=("Lucida Console", 10))
    scale_taux.place(x=800, y=655)

    scale_vitesse = Scale(fen1, orient='horizontal', bg=color, fg=color_text, highlightthickness=0, from_=60, to=450, resolution=10, length=168, label='   génération / m', bd=0)
    scale_vitesse .config(font=("Lucida Console", 10))
    scale_vitesse .place(x=800, y=580)


    fen1.mainloop()

