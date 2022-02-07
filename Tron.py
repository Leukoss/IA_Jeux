import time
import tkinter as tk
import random
import numpy as np
import copy

#################################################################################
#
#   Données de partie

Data = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

GInit = np.array(Data, dtype=np.int8)
GInit = np.flip(GInit, 0).transpose()

LARGEUR = 13
HAUTEUR = 17


# container pour passer efficacement toutes les données de la partie

class Game:
    def __init__(self, Grille, PlayerX, PlayerY, Score=0):
        self.PlayerX = PlayerX
        self.PlayerY = PlayerY
        self.Score = Score
        self.Grille = Grille

    def copy(self):
        return copy.deepcopy(self)


GameInit = Game(GInit, 3, 5)

##############################################################
#
#   création de la fenetre principale  - NE PAS TOUCHER

L = 20  # largeur d'une case du jeu en pixel    
largeurPix = LARGEUR * L
hauteurPix = HAUTEUR * L

Window = tk.Tk()
Window.geometry(str(largeurPix) + "x" + str(hauteurPix))  # taille de la fenetre
Window.title("TRON")

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

canvas = tk.Canvas(Frame0, width=largeurPix, height=hauteurPix, bg="black")
canvas.place(x=0, y=0)


#   Dessine la grille de jeu - ne pas toucher


def Affiche(Game):
    canvas.delete("all")
    H = canvas.winfo_height()

    def DrawCase(x, y, coul):
        x *= L
        y *= L
        canvas.create_rectangle(x, H - y, x + L, H - y - L, fill=coul)

    # dessin des murs 

    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if Game.Grille[x, y] == 1: DrawCase(x, y, "gray")
            if Game.Grille[x, y] == 2: DrawCase(x, y, "cyan")

    # dessin de la moto
    DrawCase(Game.PlayerX, Game.PlayerY, "red")


def AfficheScore(Game):
    info = "SCORE : " + str(Game.Score)
    canvas.create_text(80, 13, font='Helvetica 12 bold', fill="yellow", text=info)


###########################################################
#
# gestion du joueur IA

def PossibleMove(Game):
    L = []
    x, y = Game.PlayerX, Game.PlayerY
    if Game.Grille[x][y - 1] == 0: L.append((0, -1))  # Haut
    if Game.Grille[x][y + 1] == 0: L.append((0, 1))  # Bas
    if Game.Grille[x + 1][y] == 0: L.append((1, 0))  # Droite
    if Game.Grille[x - 1][y] == 0: L.append((-1, 0))  # Gauche
    return L


def SetWall(Game, x, y):
    Game.Grille[x, y] = 2


def SimulationPartie(Game):
    Loop = True
    while Loop:
        x, y = Game.PlayerX, Game.PlayerY

        L = PossibleMove(Game)

        if len(L) == 0:
            return Game.Score

        INDEX = random.randrange(len(L))

        SetWall(Game, x, y)

        x += L[INDEX][0]
        y += L[INDEX][1]

        v = Game.Grille[x, y]

        if v > 0:
            return Game.Score  # collision détectée
        else:
            Game.PlayerX = x  # valide le déplacement
            Game.PlayerY = y  # valide le déplacement
            Game.Score += 1


def MonteCarlo(Game, Iteration):
    Total = 0

    for i in range(Iteration):
        Game2 = Game.copy()
        Total += SimulationPartie(Game2)
    return Total


def Play(Game):
    x, y = Game.PlayerX, Game.PlayerY
    L = PossibleMove(Game)
    AVERAGE = []

    for test in L:
        X = x + test[0]
        Y = y + test[1]

        Game.PlayerX, Game.PlayerY = X, Y

        AVERAGE.append(MonteCarlo(Game, 1000))  # Après le déplacement dans une des directions possibles, on enregistre
        # le score pour X simulation

    INDEX = 0

    if len(AVERAGE) == 0:
        return Game.Score  # collision détectée

    SetWall(Game, x, y)

    MOVE = L[AVERAGE.index(max(AVERAGE))]

    SetWall(Game, x, y)

    x += MOVE[0]
    y += MOVE[1]

    v = Game.Grille[x, y]

    if v > 0:
        return Game.Score  # collision détectée
    else:
        Game.PlayerX = x  # valide le déplacement
        Game.PlayerY = y  # valide le déplacement
        Game.Score += 1


################################################################################

CurrentGame = GameInit.copy()


def Partie():
    Tstart = time.time()
    PartieTermine = Play(CurrentGame)

    print(time.time() - Tstart)

    if not PartieTermine:
        Affiche(CurrentGame)
        # rappelle la fonction Partie() dans 30ms
        # entre temps laisse l'OS réafficher l'interface
        Window.after(100, Partie)
    else:
        AfficheScore(CurrentGame)


#####################################################################################
#
#  Mise en place de l'interface - ne pas toucher

AfficherPage(0)
Window.after(100, Partie)
Window.mainloop()
