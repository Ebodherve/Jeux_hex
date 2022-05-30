from math import cos, sin, radians
from tkinter import Tk, Canvas, Frame, Button, Label
import os

from GameBoard import *
from Joueurs import *


class Point:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def distance(self, point):
        return ((self.x-point.x)**2 + (self.y-point.y)**2)**(1/2)

    # tracer un hexagone sur le canvas
    def tracerHexagone(self,p1,p2,p3,p4,p5,canvas):
        canvas.create_polygon(self.x,self.y, p1.x, p1.y, p2.x, p2.y, p3.x,p3.y, p4.x,p4.y, p5.x,p5.y,fill= "white", outline='black')

    # tracer un cercle d'un certain rayon et d'une certaine couleur sur le canvas
    def tracerCercle(self,r,couleur,canvas,hover=''):
        canvas.create_oval(self.x-r,self.y-r,self.x+r,self.y+r,fill=couleur,outline='',activefill=hover)

    def tracer_ligne(self, p, couleur, canvas):
        canvas.create_line(self.x, self.y, p.x, p.y, fill=couleur)


class HexagoneView:

    def __init__(self, rayon_cercle=30, centre=Point()):
        self.rayon_cercle = rayon_cercle
        self.couleur = None
        self.centre = centre
        self.points = []

    def colorier(self, couleur,canvas):
        self.couleur = couleur
        self.centre.tracerCercle(self.rayon_cercle, couleur, canvas)

    def dessiner(self, canvas):
        norme = self.rayon_cercle*((4/3)**(1/2))
        points = []
        centre = self.centre
        angle = 90
        for i in range(6):
            direction = norme*cos(radians(angle)), norme*sin(radians(angle))
            points.append(Point(centre.x+direction[0], centre.y+direction[1]))
            angle += 60
        self.points = points
        self.trace = self.points[0].tracerHexagone(self.points[1],self.points[2],
            self.points[3],self.points[4],self.points[5],canvas)
        # cree un cercle qui s'affiche quand l'Hexqagone est survole
        self.centre.tracerCercle(self.rayon_cercle,'',canvas,'#ddd')

    def colori_bordure_dessus(self, couleur, canvas):
        self.points[2].tracer_ligne(self.points[3], couleur, canvas)
        self.points[3].tracer_ligne(self.points[4], couleur, canvas)

    def colori_bordure_dessous(self, couleur, canvas):
        self.points[-1].tracer_ligne(self.points[0], couleur, canvas)
        self.points[0].tracer_ligne(self.points[1], couleur, canvas)

    def colori_bordure_gauche(self, couleur, canvas):
        self.points[0].tracer_ligne(self.points[1], couleur, canvas)
        self.points[1].tracer_ligne(self.points[2], couleur, canvas)

    def colori_bordure_droite(self, couleur, canvas):
        self.points[3].tracer_ligne(self.points[4], couleur, canvas)
        self.points[4].tracer_ligne(self.points[5], couleur, canvas)

    def taille_self(self):
        return self.rayon_cercle*3


class HexView:

    def __init__(self, canvas=None, taille=14, rayon_hex=20):
        self.taille = taille
        self.hexagones = [[] for i in range(taille)]
        self.hexboard = HexBoard(self,taille=taille, rayon_hex=rayon_hex)
        self.rayon_hex = rayon_hex
        self.canvas = canvas
        self.joueur1 = "blue"
        self.joueur2 = "red"
        self.joueur_arriere = None
        self.joueur_courant = self.joueur1
        self.fenetreMenu = None
        self.fenetreVictoire = None
        self.fenetreMain = None
        self.construire_grille()

    def construire_grille(self):
        centres_hex = self.hexboard.construire_tableau()
        for i in range(self.taille):
            for j in range(self.taille):
                centre = centres_hex[i][j]
                centre = Point(x=centre[0], y=centre[1])
                self.hexagones[i].append(HexagoneView(rayon_cercle=self.rayon_hex, centre=centre))

    def afficher_grille(self):
        couleur1 = "blue"
        couleur2 = "red"
        for ligne in self.hexagones:
            for h in ligne :
                h.dessiner(self.canvas)
        #coloriage des bordures
        for i in range(self.taille):
            self.hexagones[0][i].colori_bordure_dessus(couleur1, self.canvas)
            self.hexagones[self.taille-1][i].colori_bordure_dessous(couleur1, self.canvas)
            self.hexagones[i][0].colori_bordure_gauche(couleur2, self.canvas)
            self.hexagones[i][self.taille-1].colori_bordure_droite(couleur2, self.canvas)

    #Connection à la grille
    def setboard(self, hexboard):
        self.hexboard = hexboard

    #Affichage de la grille
    def demmarrage(self):
        #initialisation du joueur ia ou random
        self.canvas.bind("<Button-1>",self.jouer_clic)

    def jouer_clic(self, event):
        if self.joueur_arriere :
            joueur = self.interface_joueur_couleur(self.joueur1)
        else:
            joueur = self.interface_joueur_couleur(self.joueur_courant)
        x, y = event.x, event.y
        valide = self.hexboard.isValide((x, y), joueur)
        if valide[0]:
            i, j = valide[1], valide[2]
            self.jouer((i, j), joueur)
            self.test_joueur_arriere()

    def jouer(self, ind, joueur):
        #os.system("clear")
        i, j = ind
        couleur = self.interface_couleur_joueur(joueur)
        self.hexagones[i][j].colorier(couleur, self.canvas)
        trouver = self.hexboard.trouver_chemin(joueur, ind)
        self.passer_la_main()
        if trouver :
            if self.joueur_arriere:
                self.victoire("Vous")
            else:
                self.victoire(f"Le joueur : {self.interface_couleur_joueur(joueur)}")

    def interface_joueur_couleur(self, couleur):
        return 1 if couleur==self.joueur1 else 2 

    def interface_couleur_joueur(self, joueur):
        return self.joueur1 if joueur==1 else self.joueur2

    def passer_la_main(self):
        if self.joueur_courant == self.joueur1:
            self.joueur_courant = self.joueur2
        else:
            self.joueur_courant = self.joueur1

    def test_joueur_arriere(self):
        if self.joueur_arriere:
            self.joueur_arriere.jouer()

    def colorier_hex(self, ind, joueur):
        i, j = ind
        couleur = self.interface_couleur_joueur(joueur)
        self.hexagones[i][j].colorier(couleur, self.canvas)

    def init_joueur_random(self):
        ja = self.joueur2
        self.joueur_arriere = JoueurRandom("Joueur Random", 
            self.hexboard,
            self.taille, 
            couleur=self.interface_joueur_couleur(ja))
        self.fenetreMenu.quit()
        self.fenetreMenu.destroy()
        self.commencer()

    def init_joueur_ia(self):
        ja = self.joueur2
        self.joueur_arriere = JoueurIa("Joueur Ia", 
            self.hexboard, 
            self.taille, 
            couleur=self.interface_joueur_couleur(ja))
        self.fenetreMenu.destroy()
        self.commencer()

    def menu(self):
        self.fenetreMenu = Tk(className='Choisir le type joueur avec lequel jouer')
        self.fenetreMenu.resizable(width=False, height=False)
        self.fenetreMenu.geometry('320x200+700+300')
        brandom = Button(self.fenetreMenu, text="Joueur Random",
            command=self.init_joueur_random)
        bia = Button(self.fenetreMenu, text="Joueur Ia", 
            command=self.init_joueur_ia)
        brandom.pack()
        bia.pack()
        self.fenetreMenu.mainloop()

    def commencer(self):
        self.fenetreMain = Tk(className=f'Vous jouez contre : {self.joueur_arriere.getName()}')
        taille_unit = self.hexagones[0][0].taille_self()
        self.canvas = Canvas(self.fenetreMain, width=self.taille*taille_unit, height=(self.taille/(1.5))*taille_unit, bg ='ivory')
        self.canvas.grid()
        self.afficher_grille()
        self.demmarrage()
        self.fenetreMain.mainloop()

    def victoire(self, victorieux):
        self.fenetreVictoire = Tk(className="Gagnant")
        label_victoire = Label(self.fenetreVictoire, text=f"Le gagnant est {victorieux}")
        b_recommencer = Button(self.fenetreVictoire, text="Recommencer", command=self.recommencer)
        label_victoire.pack()
        b_recommencer.pack()

    def recommencer(self):
        if self.fenetreMain:
            self.fenetreMain.destroy()
        if self.fenetreVictoire:
            self.fenetreVictoire.destroy()
        self.__init__()
        self.menu()


if __name__=="__main__":
    h1 = HexView()
    h1.menu()
    
