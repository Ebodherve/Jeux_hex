from random import shuffle, choice
import time


class Joueur:

    def __init__(self, name, hexboard=None, taille=14, couleur=2):
        self.name = name
        self.taille_space = taille
        self.space = self.init_space(taille)
        self.hexboard = hexboard
        self.couleur = couleur
        self.__free = self.space
        if hexboard:
            self.hexboard.ajout_joueur_arriere(self)

    def getName(self):
        return self.name

    def init_space(self, taille):
        return [(i,j) for i in range(taille) for j in range(taille)]

    def ajouthexboard(self, hexboard):
        self.hexboard = hexboard

    def jouer(self, ind):
        time.sleep(0.4)
        self.hexboard.colorier_hex_arriere(ind, self.couleur, self.getName())
        try:
            self.__free.remove(self.hexboard.dernier_coup_jouer())
        except:
            pass
        

class JoueurIa(Joueur):

    def __init__(self, name, hexboard=None, taille=14, couleur=2):
        Joueur.__init__(self, name, hexboard=hexboard, taille=taille, couleur=couleur)
        self.__free = self.space
        self.grille_hex = self.tableau_hex()
        self.liste_chemins = []

    def strategies(self):
        #recherche de chemin 
        self.grille_hex = self.tableau_hex()
        liste_chemins = self.recherche_chemin_verticale(self.grille_hex)
        
        #Choix d'indice pour la contre-attaque à partir du dernier hexagone d'un chemin
        shuffle(liste_chemins)
        ind = liste_chemins[0][-1].indice_self()
        choix = self.trouver_voisinage(ind, self.grille_hex)
        while not choix and len(liste_chemins) > 0:
            ind = liste_chemins[0][-1].indice_self()
            choix = self.trouver_voisinage(ind, self.grille_hex)
            liste_chemins = liste_chemins[1:]
        if choix:
            self.__free.remove(choix)
            return choix
        return self.__free.pop()

    def recherche_chemin_verticale(self, grille):
        #recherche de chemin de haut à en bas
        taille = self.taille_space
        liste_chemins = []
        for j in range(taille):
            chemin = []
            for i in range(taille):
                h = grille[i][j]
                couleur = h.couleur()
                if not couleur==self.couleur and couleur:
                    if i < taille-1:
                        if couleur == grille[i+1][j].couleur():
                            chemin.append(h)
                        else:
                            chemin.append(h)
                            liste_chemins.append(chemin)
                            chemin = []
                    else:
                        chemin.append(h)
                        liste_chemins.append(chemin)
                        chemin = []
        return liste_chemins

    def trouver_voisinage(self, ind, grille):
        i, j = ind
        liste_voisins = []
        for v in grille[i][j].freres():
            if self.hexboard.indice_valide(v):
                if grille[v[0]][v[1]].peut_se_colorier():
                    liste_voisins.append(v)
        if len(liste_voisins) > 0:
            return choice(liste_voisins)
        return False

    def tableau_hex(self):
        if self.hexboard:
            return self.hexboard.hexagones.copy()

    def jouer(self):
        ind = self.strategies()
        Joueur.jouer(self,ind)


class JoueurRandom(Joueur):

    def __init__(self, name, hexboard=None, taille=14, couleur=2):
        Joueur.__init__(self, name, hexboard=hexboard, taille=taille, couleur=couleur)
        self.__free = self.space
        shuffle(self.__free)

    def jouer(self):
        ind = self.__free.pop()
        Joueur.jouer(self,ind)



