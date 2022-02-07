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


def RandomMove(Game):
    LPossibleMove = PossibleMove(Game)

    if len(LPossibleMove) == 0: LPossibleMove = ((-1, 0), (1, 0), (0, -1), (0, 1))

    return LPossibleMove[random.randrange(len(LPossibleMove))]


# Pas une fonction demandée mais souvent utilisée donc pour éviter la duplication de code !
def Action(Game, Direction):
    x, y = Game.PlayerX, Game.PlayerY

    Game.Grille[x, y] = 2

    x += Direction[0]
    y += Direction[1]

    if Game.Grille[x, y] > 0:
        return True
    else:
        Game.PlayerX = x  # valide le déplacement
        Game.PlayerY = y  # valide le déplacement
        Game.Score += 1
        return False


###########################################################
#
# simulation en parallèle des parties

# Liste des directions :
# 0 : sur place
# 1 : à gauche
# 2 : en haut
# 3 : à droite
# 4 : en bas

dx = np.array([0, -1, 0, 1, 0], dtype=np.int32)
dy = np.array([0, 0, 1, 0, -1], dtype=np.int32)

# scores associés à chaque déplacement
ds = np.array([0, 1, 1, 1, 1], dtype=np.int32)

nb = 10000  # nb de parties


# Permet de simuler une partie et de renvoyer son score
def SimulationPartie(Game):
    # on copie les datas de départ pour créer plusieurs parties en //
    G = np.tile(Game.Grille, (nb, 1, 1))
    X = np.tile(Game.PlayerX, nb)
    Y = np.tile(Game.PlayerY, nb)
    S = np.tile(Game.Score, nb)
    I = np.arange(nb)  # Nombre de simulations en //
    boucle = True
    while boucle:
        # marque le passage de la moto
        G[I, X, Y] = 2

        # Vecteur pour les directions et un vecteur pour la taille de chaque vecteur de direction
        LPossibles = np.zeros((nb, 4), dtype=np.int32)
        Tailles = np.zeros(nb, dtype=np.int32)

        # Directions
        Gauche = G[I, X - 1, Y]
        Gauche = (Gauche == 0) * 1

        LPossibles[I, Tailles] = Gauche
        Tailles += Gauche

        Haut = G[I, X, Y + 1]
        Haut = (Haut == 0) * 1

        LPossibles[I, Tailles] = Haut * 2
        Tailles += Haut

        Droite = G[I, X + 1, Y]
        Droite = (Droite == 0) * 1

        LPossibles[I, Tailles] = Droite * 3
        Tailles += Droite

        Bas = G[I, X, Y - 1]
        Bas = (Bas == 0) * 1

        LPossibles[I, Tailles] = Bas * 4
        Tailles += Bas

        # Pour rester sur place on change les tailles à 0 pour 1
        Tailles[Tailles == 0] = 1

        # Génération d'une direction aléatoire
        R = np.random.randint(Tailles)

        Choix = LPossibles[I, R]

        # DEPLACEMENT
        DX = dx[Choix]
        DY = dy[Choix]
        DS = ds[Choix]

        # Condition de fin de partie => plus de score donc :
        if np.sum(DS) == 0:
            boucle = False

        X += DX
        Y += DY
        S += DS

    return np.sum(S)


# Permet de simuler beaucoup de parties et de choisir celle avec le meilleur score
def MonteCarlo(Game, Direction):
    ScoreTot = 0
    Game2 = Game.copy()
    Action(Game2, Direction)

    return SimulationPartie(Game2)


def BetterMove(Game):
    L = PossibleMove(Game)
    AVERAGE = []

    # sans direction, on lui assigne une aléatoire
    if len(L) == 0:
        return RandomMove(Game)

    for DIRECTION in L:
        AVERAGE.append(MonteCarlo(Game, DIRECTION))

    return L[AVERAGE.index(max(AVERAGE))]


def Play(Game):
    L = PossibleMove(Game)
    AVERAGE = []

    # sans direction, on lui assigne une aléatoire afin de pouvoir mettre un terme au jeu
    if len(L) == 0:
        return RandomMove(Game)

    for DIRECTION in L:
        AVERAGE.append(MonteCarlo(Game, DIRECTION))

    DIRECTION = L[AVERAGE.index(max(AVERAGE))]

    # Retourne si le jeu est fini ou non (auquel cas il faudra afficher le score dans Partie())
    return Action(Game, DIRECTION)


################################################################################

CurrentGame = GameInit.copy()


def Partie():
    PartieTermine = Play(CurrentGame)

    if not PartieTermine:
        Affiche(CurrentGame)
        Window.after(100, Partie)
    else:
        AfficheScore(CurrentGame)


#####################################################################################
#
#  Mise en place de l'interface - ne pas toucher

AfficherPage(0)
Window.after(100, Partie)
Window.mainloop()
