import tkinter as tk
from tkinter import messagebox
import random
import numpy as np

###############################################################################
# création de la fenêtre principale - ne pas toucher

LARG = 300
HAUT = 300

Window = tk.Tk()
Window.geometry(str(LARG) + "x" + str(HAUT))  # taille de la fenêtre
Window.title("ESSIE - Morpion")

# création de la frame principale stockant toutes les pages

F = tk.Frame(Window)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)

# gestion des différentes pages

ListePages = {}
PageActive = 0


def CreerUnePage(id):
    Frame = tk.Frame(F)
    ListePages[id] = Frame
    Frame.grid(row=0, column=0, sticky="nsew")
    return Frame


def AfficherPage(id):
    global PageActive
    PageActive = id
    ListePages[id].tkraise()


Frame0 = CreerUnePage(0)

canvas = tk.Canvas(Frame0, width=LARG, height=HAUT, bg="black")
canvas.place(x=0, y=0)

#################################################################################
#
#  Paramètres du jeu

Grille = [[0, 0, 0],
          [0, 0, 0],
          [0, 0, 0]]  # attention les lignes représentent les colonnes de la grille

Grille = np.array(Grille)
Grille = Grille.transpose()  # pour avoir x,y

# Score des joueurs
Score_Player = 0
Score_IA = 0

# Couleur des joueurs
COULEUR_JOUEUR = "RED"
COULEUR_IA = "YELLOW"

# Etat de la partie
DEBUT = False

H  = 10
N  = 20
IA = 30


def Init():
    global Grille

    Grille = np.zeros(Grille.shape, dtype=np.int32)


def Full():
    """
    Permet de savoir si la grille est pleine

    :return:
        Boolean
    """
    for x in range(len(Grille[0])):
        for y in range(len(Grille[1])):
            if Grille[x][y] == 0:
                return False
    return True


###############################################################################
#
# gestion du joueur humain et de l'IA
# VOTRE CODE ICI

def Victoire():
    """
    On teste pour les 8 configurations victorieuses si cela est le cas.

        Si ce n'est pas le cas alors on renvoie 0 de manière, à savoir que ce n'est pas gagnant
        Sinon on renvoie la ligne/diagonale/colonne mettant en évidence la victoire

    :return: Si victoire il y a et où
    """
    # Contient la liste des configurations gagnantes possibles
    Victoire = [
         [Grille[0][0], Grille[1][1], Grille[2][2]],
         [Grille[2][0], Grille[1][1], Grille[0][2]]
         ]

    for index in range(3):
        # 3 configurations avec colonnes gagnantes
        Victoire.append([Grille[index][0], Grille[index][2], Grille[index][1]])
        # 3 configurations avec lignes gagnantes
        Victoire.append([Grille[0][index], Grille[1][index], Grille[2][index]])

    # Si parmi la liste de configurations disponibles, tous ses termes sont != 0 donc non vide, cela implique la
    # victoire
    for config in Victoire:
        if config[0] == config[1] == config[2] != 0:
            # La valeur contenue dans config[0] est soit 1 soit 2 et on pourra déterminer qui de IA ou PLAYER gagne
            return config[0]


def LPossibleMove():
    global Grille

    L = []
    # Pour chaque colonne
    for x in range(3):
        # Pour chaque ligne
        for y in range(3):
            # Si la case est vide alors ses coordonnées sont ajoutés dans la liste des moves possibles
            if Grille[x][y] == 0:
                L.append([x, y])
    return L


def Result():
    if Victoire() == 1:
        return H
    elif Victoire() == 2:
        return IA
    elif Full():
        return N
    return 0


def SimuleIA():
    global Grille

    RES = Result()

    # Dans le cas d'une victoire d'un des deux camps ou nul, on retient qui gagne (H/IA/N)
    if RES != 0:
        return [100, 100, RES]

    # On récupère la liste des coups possibles(cases vides)
    L = LPossibleMove()

    Results = []

    # Pour chaque coup possible
    for K in L:
        # On récupère les coordonnées pour remplir la grille par un pion de l'IA
        x, y = K[0], K[1]
        Grille[x][y] = 2

        # On simule un coup de l'humain et on récupère le résultat de son coup
        R = SimuleHumain()[2]

        # On stock dans le résultat [déplacement en abs, déplacement en ord, Victoire de IA/PLAYER ou N]
        Results.append([x, y, R])

        # On retire le coup K
        Grille[x][y] = 0

    for Data in Results:
        # Si Victoire de l'IA alors on adopte ce coup-là
        if Data[2] == IA:
            return Data

    for Data in Results:
        if Data[2] == N:
            return Data

    return Results[0]


def SimuleHumain():
    global Grille

    RES = Result()

    # Dans le cas d'une victoire d'un des deux camps ou nul, on retient qui gagne (H/IA/N)
    if RES != 0:
        return [100, 100, RES]

    # On récupère la liste des coups possibles(cases vides)
    L = LPossibleMove()

    Results = []

    # Pour chaque coup possible
    for K in L:
        # On récupère les coordonnées pour remplir la grille par un pion de PLAYER
        x, y = K[0], K[1]
        Grille[x][y] = 1

        # On simule un coup de l'humain
        R = SimuleIA()[2]

        # On stock les deux moves dans résultats
        Results.append([x, y, R])

        # On retire le coup K
        Grille[x][y] = 0

    for Data in Results:
        # Si Victoire de l'IA alors on adopte ce coup-là
        if Data[2] == H:
            return Data

    for Data in Results:
        if Data[2] == N:
            return Data

    return Results[0]


################################################################################
#    
# Dessine la grille de jeu

def Dessine(Grille_Color, PartieGagnee=False):
    # DOC canvas : http://tkinter.fdex.eu/doc/caw.html
    canvas.delete("all")

    for i in range(4):
        canvas.create_line(i * 100, 0, i * 100, 300, fill=Grille_Color, width="4")
        canvas.create_line(0, i * 100, 300, i * 100, fill=Grille_Color, width="4")

    for x in range(3):
        for y in range(3):
            xc = x * 100
            yc = y * 100
            if Grille[x][y] == 1:
                canvas.create_line(xc + 10, yc + 10, xc + 90, yc + 90, fill="red", width="4")
                canvas.create_line(xc + 90, yc + 10, xc + 10, yc + 90, fill="red", width="4")
            if Grille[x][y] == 2:
                canvas.create_oval(xc + 10, yc + 10, xc + 90, yc + 90, outline="yellow", width="4")

    # Affichage du score (en reprenant le code de Tron)
    Text_Player = "[J1]", str(Score_Player)
    Text_IA = "[IA]", str(Score_IA)

    canvas.create_text(275, 13, font='Helvetica 12 bold', fill=COULEUR_IA, text=Text_IA)
    canvas.create_text(25, 13, font='Helvetica 12 bold', fill=COULEUR_JOUEUR, text=Text_Player)


####################################################################################
#
#  fnt appelée par un clic souris sur la zone de dessin

def MouseClick(event):
    global DEBUT, Score_Player, Score_IA, COULEUR_IA, COULEUR_JOUEUR

    Window.focus_set()

    x = event.x // 100  # convertit une coordonnée pixel écran en coord grille de jeu
    y = event.y // 100

    if (x < 0) or (x > 2) or (y < 0) or (y > 2):
        return

    print("clicked at", x, y)

    # Initialisation de la partie => Clear + Dessin de la grille vierge + Mise à False du début de la partie
    if DEBUT:
        Init()
        DEBUT = False
        Dessine("blue")
        return

    # Si la case sur laquelle on clique n'est pas vierge alors on arrête
    if Grille[x][y] != 0:
        return

    # Si nous avons fini l'initialisation et que la case n'est pas déjà occupée, on peut la remplir (PLAYER)
    Grille[x][y] = 1

    # Victoire de PLAYER
    if Victoire() == 1:
        Score_Player += 1
        DEBUT = True
        Dessine(COULEUR_JOUEUR)
        return

    if Full():
        DEBUT = True
        Dessine("white")
        return

    Dessine("blue")

    # On génère les coordonnées les plus avantageux pour l'IA
    xIA, yIA = SimuleIA()[0:2]

    # Et on les assigne sur la grille à un pion IA
    Grille[xIA][yIA] = 2

    if Victoire() == 2:
        DEBUT = True
        Score_IA += 1
        Dessine(COULEUR_IA)
        return

    if Full():
        DEBUT = True
        Dessine("white")
        return

    Dessine("blue")


canvas.bind('<ButtonPress-1>', MouseClick)

#####################################################################################
#
#  Mise en place de l'interface - ne pas toucher

AfficherPage(0)
Dessine("blue")
Window.mainloop()
