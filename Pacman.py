# ﻿import math
import random
import tkinter as tk
from tkinter import font as tkfont
import numpy as np


##########################################################################
#
#   Partie I : variables du jeu - placez votre code dans cette section
#
#########################################################################

# Plan du labyrinthe

# 0 vide
# 1 mur
# 2 maison des fantômes (ils peuvent circuler, mais pas pacman)

def CreateArray(L):
    T = np.array(L, dtype=np.int32)
    # ainsi, on peut écrire TBL[x][y]
    T = T.transpose()
    return T


TBL = CreateArray([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 1, 2, 2, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]);

HAUTEUR = TBL.shape[1]
LARGEUR = TBL.shape[0]


# placements des pacgums et des fantômes

def PlacementsGUM():  # placements des pacgums
    GUM = np.zeros(TBL.shape, dtype=np.int32)

    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if TBL[x][y] == 0:
                GUM[x][y] = 1
    return GUM


GUM = PlacementsGUM()


def PlacementsDIST():
    DIST = np.zeros(TBL.shape, dtype=np.int32)

    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if TBL[x][y] == 1 or TBL[x][y] == 2:
                DIST[x][y] = 500
            if GUM[x][y] == 1:
                DIST[x][y] = 0
            else:
                DIST[x][y] = 100
    return DIST


DIST = PlacementsDIST()

PacManPos = [5, 5]

score = 0


def EatGums():
    global score
    x, y = PacManPos
    if GUM[x][y] == 1:
        GUM[x][y] = 0
        score += 100


Ghosts = [[LARGEUR // 2, HAUTEUR // 2, "pink", "bas"], [LARGEUR // 2, HAUTEUR // 2, "orange", "bas"],
          [LARGEUR // 2, HAUTEUR // 2, "cyan", "bas"], [LARGEUR // 2, HAUTEUR // 2, "red", "bas "]]


def PlacementsGhost():
    GHST = np.zeros(TBL.shape, dtype=np.int32)

    # Pour chaque ligne
    for y in range(HAUTEUR):
        # Pour chaque colonne
        for x in range(LARGEUR):
            # Boolean pour savoir si la présence d'un fantôme sur la case est détectée
            ghost = False
            # Si la case actuelle est un mur ou la maison des fantômes alors cette case vaut une très grande valeur
            if TBL[x][y] == 1:
                GHST[x][y] = 500
            else:
                GHST[x][y] = 100
    for F in Ghosts:
        # On récupère ses coordonnées
        X = F[0]
        Y = F[1]
        GHST[X][Y] = 0
    return GHST


GHST = PlacementsGhost()

##############################################################################
#
#   Partie II :  AFFICHAGE -- NE PAS MODIFIER jusqu'à la prochaine section
#
##############################################################################


ZOOM = 40  # taille d'une case en pixels
EPAISS = 8  # épaisseur des murs bleus en pixels

screeenWidth = (LARGEUR + 1) * ZOOM
screenHeight = (HAUTEUR + 2) * ZOOM

Window = tk.Tk()
Window.geometry(str(screeenWidth) + "x" + str(screenHeight))  # taille de la fenêtre
Window.title("ESIEE - PACMAN")

# gestion de la pause

PAUSE_FLAG = False


def keydown(e):
    global PAUSE_FLAG
    if e.char == ' ':
        PAUSE_FLAG = not PAUSE_FLAG


Window.bind("<KeyPress>", keydown)

# création de la frame principale stockant plusieurs pages

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


def WindowAnim():
    MainLoop()
    Window.after(500, WindowAnim)


Window.after(100, WindowAnim)

# Ressources

PoliceTexte = tkfont.Font(family='Arial', size=22, weight="bold", slant="italic")

# création de la zone de dessin

Frame1 = CreerUnePage(0)

canvas = tk.Canvas(Frame1, width=screeenWidth, height=screenHeight)
canvas.place(x=0, y=0)
canvas.configure(background='black')


#  FNT AFFICHAGE


def To(coord):
    return coord * ZOOM + ZOOM


# dessine l'ensemble des éléments du jeu par-dessus le décor

anim_bouche = 0
animPacman = [5, 10, 15, 10, 5]


def Affiche(PacmanColor, message, data1, data2):
    global anim_bouche

    def CreateCircle(x, y, r, coul):
        canvas.create_oval(x - r, y - r, x + r, y + r, fill=coul, width=0)

    canvas.delete("all")

    # murs

    for x in range(LARGEUR - 1):
        for y in range(HAUTEUR):
            if TBL[x][y] == 1 and TBL[x + 1][y] == 1:
                xx = To(x)
                xxx = To(x + 1)
                yy = To(y)
                canvas.create_line(xx, yy, xxx, yy, width=EPAISS, fill="blue")

    for x in range(LARGEUR):
        for y in range(HAUTEUR - 1):
            if TBL[x][y] == 1 and TBL[x][y + 1] == 1:
                xx = To(x)
                yy = To(y)
                yyy = To(y + 1)
                canvas.create_line(xx, yy, xx, yyy, width=EPAISS, fill="blue")

    # pacgum
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if GUM[x][y] == 1:
                xx = To(x)
                yy = To(y)
                e = 5
                canvas.create_oval(xx - e, yy - e, xx + e, yy + e, fill="orange")

    # extra info
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            xx = To(x)
            yy = To(y) - 11
            txt = data1[x][y]
            canvas.create_text(xx, yy, text=txt, fill="white", font=("Purisa", 8))

    # extra info 2
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            xx = To(x) + 10
            yy = To(y)
            txt = data2[x][y]
            canvas.create_text(xx, yy, text=txt, fill="yellow", font=("Purisa", 8))

    # dessine pacman
    xx = To(PacManPos[0])
    yy = To(PacManPos[1])
    e = 20
    anim_bouche = (anim_bouche + 1) % len(animPacman)
    ouv_bouche = animPacman[anim_bouche]
    tour = 360 - 2 * ouv_bouche
    canvas.create_oval(xx - e, yy - e, xx + e, yy + e, fill=PacmanColor)
    canvas.create_polygon(xx, yy, xx + e, yy + ouv_bouche, xx + e, yy - ouv_bouche, fill="black")  # bouche

    # dessine les fantômes
    dec = -3
    for P in Ghosts:
        xx = To(P[0])
        yy = To(P[1])
        e = 16

        coul = P[2]
        # corps du fantôme
        CreateCircle(dec + xx, dec + yy - e + 6, e, coul)
        canvas.create_rectangle(dec + xx - e, dec + yy - e, dec + xx + e + 1, dec + yy + e, fill=coul, width=0)

        # œil gauche
        CreateCircle(dec + xx - 7, dec + yy - 8, 5, "white")
        CreateCircle(dec + xx - 7, dec + yy - 8, 3, "black")

        # œil droit
        CreateCircle(dec + xx + 7, dec + yy - 8, 5, "white")
        CreateCircle(dec + xx + 7, dec + yy - 8, 3, "black")

        dec += 3

    # texte

    canvas.create_text(screeenWidth // 2, screenHeight - 50, text="PAUSE : PRESS SPACE", fill="yellow",
                       font=PoliceTexte)
    canvas.create_text(screeenWidth // 2, screenHeight - 20, text=message, fill="yellow", font=PoliceTexte)


AfficherPage(0)


#########################################################################
#
#  Partie III :   Gestion de partie - placez votre code dans cette section
#
#########################################################################

def PacManPossibleMove():
    L = []
    x, y = PacManPos
    if TBL[x][y - 1] == 0: L.append((0, -1))
    if TBL[x][y + 1] == 0: L.append((0, 1))
    if TBL[x + 1][y] == 0: L.append((1, 0))
    if TBL[x - 1][y] == 0: L.append((-1, 0))
    return L


def GhostsPossibleMove(x, y):
    L = []
    if not TBL[x][y - 1] == 1: L.append((0, -1))
    if not TBL[x][y + 1] == 1: L.append((0, 1))
    if not TBL[x + 1][y] == 1: L.append((1, 0))
    if not TBL[x - 1][y] == 1: L.append((-1, 0))
    return L


def Collision():
    global PAUSE_FLAG
    COLL = False
    x, y = PacManPos
    for F in Ghosts:
        if F[0] == x and F[1] == y: COLL = True
    if COLL: PAUSE_FLAG = True
    return COLL


def IA():
    global PacManPos, Ghosts, GHST, DIST
    finish = 0

    # Le temps que finish ne vaut pas 1, continue à balayer, car pas fini
    while not finish:
        finish = 1
        # Pour chaque ligne (intérieur)
        for y in range(1, 10):
            # On balaye chaque colonne (intérieur)
            for x in range(1, 19):
                # Les 4 cases adjacentes sont :
                caseup = DIST[x][y - 1]
                casedown = DIST[x][y + 1]
                caseleft = DIST[x - 1][y]
                caseright = DIST[x + 1][y]
                # Si présence de Pacgum
                if GUM[x][y] == 1:
                    DIST[x][y] = 0
                # Sinon
                else:
                    # Cas où c'est un mur
                    if DIST[x][y] >= 100:
                        continue
                    # Cas entouré de murs/case à 100
                    if min(caseup, caseright, caseleft, casedown) == 100:
                        DIST[x][y] = 100
                        finish = 0
                    if min(caseup, caseright, caseleft, casedown) < 100:
                        if not (DIST[x][y] == min(caseup, caseright, caseleft, casedown) + 1):
                            DIST[x][y] = min(caseup, caseright, caseleft, casedown) + 1
                            finish = 0

    # déplacement Pacman
    L = PacManPossibleMove()

    # Obtenir parmi la liste l'indice correspondant au mouvement menant à la case la plus proche d'une gum
    x, y = PacManPos
    lower_index = 0
    current_value = DIST[PacManPos[0] + L[0][0], PacManPos[1] + L[0][1]]

    for i in range(1, len(L)):
        new_value = DIST[PacManPos[0] + L[i][0], PacManPos[1] + L[i][1]]
        if new_value < current_value:
            current_value = new_value
            lower_index = i

    choix = lower_index
    PacManPos[0] += L[choix][0]
    PacManPos[1] += L[choix][1]

    if Collision(): return

    finish = 0

    while not finish:
        finish = 1
        # Pour chaque ligne (intérieur)
        for y in range(1, 10):
            # On balaye chaque colonne (intérieur)
            for x in range(1, 19):
                # Si 1 des 4 fantômes alors ⇒ fin directement en mettant à 0
                ghost = 0
                for F in Ghosts:
                    X = F[0]
                    Y = F[1]
                    # Si présence de Fantômes
                    if x == X and y == Y:
                        GHST[x][y] = 0
                        ghost = 1
                # Les 4 cases adjacentes sont :
                caseup = GHST[x][y - 1]
                casedown = GHST[x][y + 1]
                caseleft = GHST[x - 1][y]
                caseright = GHST[x + 1][y]
                # Cas sans fantôme
                if not ghost:
                    # Cas où la case est un mur
                    if TBL[x][y] == 1:
                        continue  # tu avais mis: break erreur si il y a un mur tu arrete pas de parcourir le tableau
                    # Cas entouré de cases non balayées
                    elif min(caseup, caseright, caseleft, casedown) == 100:
                        continue  # tu avais mis: finish = 0 c une erreur si l'entourage n'as pas d'element sup a 100 il faut faire aucune modif est si il y a que ces cas la c'est fini donc il faut surtout pas mettre de finish=0 ce qui reviendrait a dire que ces cas necessite un nouveau passage
                    elif min(caseup, caseright, caseleft, casedown) < 100:
                        if GHST[x][y] != min(caseup, caseright, caseleft,
                                             casedown) + 1:  # si element pas coherent par rapport a son entourage
                            GHST[x][y] = min(caseup, caseright, caseleft, casedown) + 1
                            finish = 0

    # déplacement Fantôme
    for F in Ghosts:
        L = GhostsPossibleMove(F[0], F[1])
        X = F[0]
        Y = F[1]
        # Cas Intersection
        if (not ((TBL[X - 1][Y] == 1 and TBL[X + 1][Y] == 1) or (TBL[X][Y - 1] == 1 and TBL[X][Y + 1] == 1))) or len(
                L) == 1:
            choix = random.randrange(len(L))
            F[0] += L[choix][0]
            F[1] += L[choix][1]
            # On assigne la nouvelle direction en fonction du choix aléatoire :
            # x + 1 => droite
            if L[choix][0] == 1: F[3] = "droite"
            # x - 1 => gauche
            if L[choix][0] == -1: F[3] = "gauche"
            # y + 1 => bas
            if L[choix][1] == 1: F[3] = "bas"
            # y - 1 => haut
            if L[choix][1] == -1: F[3] = "haut"
        elif F[3] == "haut":
            F[1] -= 1
        elif F[3] == "bas":
            F[1] += 1
        elif F[3] == "gauche":
            F[0] -= 1
        elif F[3] == "droite":
            F[0] += 1

    if Collision(): return


#  Boucle principale de votre jeu appelée toutes les 500 ms

def MainLoop():
    if not PAUSE_FLAG:
        PlacementsDIST()
        PlacementsGhost()
        IA()
        EatGums()
        Affiche(PacmanColor="yellow", message=("SCORE : " + str(score)), data1=GHST, data2=DIST)


###########################################:
#  démarrage de la fenêtre - ne pas toucher

Window.mainloop()
