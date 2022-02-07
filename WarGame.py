import tkinter as tk
import random
import numpy as np
import copy
import time

#################################################################################
#
#   Données de partie

Data = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

GInit = np.array(Data, dtype=np.int8)
GInit = np.flip(GInit, 0).transpose()

LARGEUR = len(Data[0])
HAUTEUR = len(Data)

# gestion du clavier

Keys = ['z', 'd', 's', 'q', 'k']
LastKey = '0'
List_color = ["blue", "red", "yellow"]


def keydown(e):
    global LastKey
    if hasattr(e, 'char') and e.char in Keys:
        LastKey = e.char


class Game:
    def __init__(self):
        self.ListPerso = []
        self.Grille = np.copy(GInit)
        self.ListCaseHit = []

    def copy(self):
        return copy.deepcopy(self)

    def addBot(self, bot):
        self.ListPerso.append(bot)

    def relateChar(self):
        for i in range(len(self.ListPerso)):
            self.ListPerso[i].game = self

    def reloadGame(self):
        self.Grille = np.copy(GInit)
        for bot in self.ListPerso:
            x, y = bot.X, bot.Y
            if not bot.death:   self.Grille[x, y] = bot.team
            self.ListCaseHit = []

    def foundCharacter(self, x, y):
        L = [i for i in range(len(self.ListPerso)) if (self.ListPerso[i].X == x and self.ListPerso[i].Y == y)]
        return L


G = Game()


class Character:
    def __init__(self, X, Y, team, IA):
        self.X = X
        self.Y = Y
        self.team = team
        self.death = False
        self.HP = 0
        self.speed = 0  # 0-100
        self.pos_attack = 0
        self.pos_move = 0
        self.color = List_color[team - 2]
        self.freeze = 0  # ms
        self.IA = IA

    def actualizeDeath(self):
        if self.HP <= 0:
            self.HP = 0
            self.death = True

    def PossibleMove(self):
        x, y = self.X, self.Y
        list_possible_move = []
        for move in self.pos_move:
            if G.Grille[x + move[0], y + move[1]] == 0:
                list_possible_move.append(move)
        return list_possible_move

    def Move(self, move_id):
        # 0 : HAUT 1 : DROITE 2 : BAS 3 : GAUCHE
        global G
        L = self.PossibleMove()
        if self.pos_move[move_id] in L:
            G.Grille[self.X][self.Y] = 0
            new_X, new_Y = self.X + self.pos_move[move_id][0], self.Y + self.pos_move[move_id][1]
            self.X, self.Y = new_X, new_Y
            G.Grille[new_X][new_Y] = self.team

    def Attack(self):
        global G
        L = G.ListPerso
        for bot in L:
            if bot == self:
                continue
            if bot.team == self.team:
                continue
            else:
                for move in self.pos_attack:
                    for i in range(1,self.range+1):
                        x, y = self.X + i*move[0] , self.Y + i*move[1]
                        if G.Grille[x, y] == 1 or G.Grille[x, y] == self.team:
                            break
                        G.ListCaseHit.append([x, y])
                        if x == bot.X and y == bot.Y:
                            bot.HP -= self.power
                            bot.actualizeDeath()


class Guerrier(Character):
    def __init__(self, X, Y, team, IA):
        # attribut de la sous classe
        super().__init__(X, Y, team, IA)
        self.speed = 40
        self.HP = 100
        self.pos_move = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        self.power = 40
        self.pos_attack = [[0, 1], [1, 0], [0, -1], [-1, 0], [1, 1], [-1, -1], [1, -1], [-1, 1]]
        self.attacking = False
        self.range = 1
        self.freeze = 100/self.speed

class Archer(Character):
    def __init__(self, X, Y, team, IA):
        # attribut de la sous classe
        super().__init__(X, Y, team, IA)
        self.speed = 30
        self.HP = 75
        self.pos_move = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        self.power = 40
        self.pos_attack = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        self.attacking = False
        self.range = 3
        self.freeze = 100/self.speed

G0 = Guerrier(2, 8, 2)
G1 = Guerrier(2, 6, 2)
G2 = Guerrier(2, 3, 3)
A1 = Archer(9, 9, 3)

G.addBot(A1)
#G.addBot(G0)
G.addBot(G1)
#G.addBot(G2)

#class QIA():
    




##############################################################
#
#   création de la fenetre principale  - NE PAS TOUCHER

L = 20  # largeur d'une case du jeu en pixel
largeurPix = LARGEUR * L
hauteurPix = HAUTEUR * L

Window = tk.Tk()
Window.geometry(str(largeurPix) + "x" + str(hauteurPix))  # taille de la fenetre
Window.title("WAR")

# création de la frame principale stockant toutes les pages

F = tk.Frame(Window)
F.bind("<KeyPress>", keydown)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)
F.focus_set()

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

    def DrawPerso():
        for bot in Game.ListPerso:
            if bot.death:
                continue
            x, y = bot.X * L, bot.Y * L
            if isinstance(bot, Guerrier):
                canvas.create_rectangle(x, H - y, x + L, H - y - L, fill=bot.color)
            if isinstance(bot, Archer):
                canvas.create_oval(x, H - y, x + L, H - y - L, fill=bot.color)

    def PrintScore():
        a, b = 80, 13
        for bot in Game.ListPerso:
            info = "HP : " + str(bot.HP)
            canvas.create_text(a, b, font='Helvetica 12 bold', fill=bot.color, text=info)
            a += 60

    # dessin des murs
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if Game.Grille[x, y] == 1:
                DrawCase(x, y, "gray")

    def PrintCaseHit():
        for case in Game.ListCaseHit:
            x, y = case[0] * L, case[1] * L
            canvas.create_rectangle(x, H - y, x + L, H - y - L, fill="white")

    DrawPerso()
    PrintScore()
    PrintCaseHit()

###########################################################
#
# gestion du joueur IA


def JeuClavier():
    F.focus_force()
    global LastKey, G

    # decisions bots

    if LastKey != '0':
        if LastKey == Keys[0]: G.ListPerso[0].Move(0)
        if LastKey == Keys[1]: G.ListPerso[0].Move(1)
        if LastKey == Keys[2]: G.ListPerso[0].Move(2)
        if LastKey == Keys[3]: G.ListPerso[0].Move(3)
        if LastKey == Keys[4]: G.ListPerso[0].Attack()

    for bot in G.ListPerso:
        if bot.freeze != 0:
            bot.freeze -= 1
        elif bot.IA:
            print("inachevé")


    Affiche(G)
    LastKey = '0'
    G.reloadGame()
    Window.after(10, JeuClavier)

#  Mise en place de l'interface - ne pas toucher

AfficherPage(0)
Window.after(100, JeuClavier)
Window.mainloop()
