
class Joueur:

    def __init__(self, name):
        self.name = name

    def getName(self):
        return self.name

    def colorier(self):
        pass


class JoueurIa(Joueur):

    def __init__(self, name):
        Joueur.__init__(self, name)


class JoueurRandom(Joueur):

    def __init__(self, name):
        Joueur.__init__(self, name)


class HexagonesBoard:

    def __init__(self, etat_couleur=None, taille=14, rayon=30, centre=(100, 100)):
        self.etat_couleur = etat_couleur
        self.taille = taille
        self.rayon = rayon
        self.centre = centre

    def distance_centre(self, coord):
        #Calcule la distance d'un point au centre de l'hexagone
        return ((self.centre[0]-coord[0])**2+(self.centre[1]-coord[1])**2)**(1/2)

    def est_dans_rayon(self, coord):
        # Teste si des coordonnées sont dans le rayon de l'hexagone
        return self.distance_centre(coord) <= self.rayon

    def peut_se_colorier(self):
        # Teste si l'hexagone peut se colorier
        return not self.etat_couleur

    def colorier(self, couleur):
        #L'hexagone se colorie
        self.etat_couleur = couleur

    def couleur(self):
        #retourne la couleur de l'hexagone
        return self.etat_couleur

    def correspond_joueur(self, joueur):
        #Teste si le joueur à poser un pion sur cette case
        return self.etat_couleur == joueur


class HexBoard:

    def __init__(self, taille=14, rayon_hex=30, token=None):
        self.rayon_sommet = rayon_hex
        self.taille = taille
        #deux etats -> 1 : encour, 0: fin 
        self.etat = None 
        self.token = token
        self.hexagones = [[] for i in range(taille)]
        self.joueur1 = 1
        self.joueur2 = 2

    def setjoueurs(self, joueur1, joueur2):
        self.joueur1 = joueur1
        self.joueur2 = joueur2

    def construire_tableau(self):
        sommet = 2*self.rayon_sommet, 2*self.rayon_sommet
        hexagones = [[] for i in range(self.taille)]
        self.hexagones = [[] for i in range(self.taille)]
        for i in range(self.taille):
            hexagones[i].append(sommet)
            self.hexagones[i].append(HexagonesBoard(rayon=self.rayon_sommet, centre=sommet))
            for j in range(1,self.taille):
                h = hexagones[i][-1]
                h = h[0]+ 2*self.rayon_sommet, h[1]
                hexagones[i].append(h)
                self.hexagones[i].append(HexagonesBoard(rayon=self.rayon_sommet, centre=h))
            sommet = sommet[0]+self.rayon_sommet, sommet[1]+(3/2)*((4/3)**(1/2))*self.rayon_sommet
        return hexagones

    #Fonction permettant de verifier si les coordonnées x et y sont valides
    def isValide(self, coord, joueur):
        if self.token == joueur:
            for i in range(self.taille):
                for j in range(self.taille) :
                    h = self.hexagones[i][j]
                    if h.est_dans_rayon(coord):
                        if h.peut_se_colorier():
                            h.colorier(self.token)
                            return h.peut_se_colorier(), i, j
                        else:
                            return (False,)
        return (False,)
    
    def recherche_chemin(self, joueur, indice):
        #Recherche d'un chemin à partir des coordonnées d'un point
        i, j = indice[0], indice[1]
        if est_sommet(i, j):
            val_rech = -1*self.val_joueur(joueur) 
            trouver = False
            for ind in [(i+1, j), (i-1, j), (i, j+1), (i, j-1), (i+1, j+1), (i-1, j-1)]:
                if ind != indice:
                    trouver = trouver or rechercher(ind, indice, val_rech, joueur)
            return trouver
        else:
            return False

    def indice_sommet(self, indice):
        """
        Fonction qui evalu le type de sommet d'une case dans le tableau des cases
        haut : 1, bas : -1, gauche = 2, droite : -2  
        """
        i, j = indice[0], indice[1]
        if i==0 and j==0:
            return (1, 2)
        elif i==self.taille-1 and j==self.taille-1:
            return (-1, -2)
        elif i==0:
            return (1,)
        elif i==self.taille-1:
            return (-1,)
        elif j==0:
            return (2,)
        elif j==self.taille-1:
            return (-2,)
        else :
            return ()

    def est_sommet(self, indice):
        """
        Cette methode evalue si deux indices correspondent à celles d'un sommet
        """
        i, j = indice[0], indice[1]
        return i==0 or j==0 or i==self.taille-1 or j==self.taille-1

    def rechercher(self, id_courant, id_exclut, val_rech, joueur):
        """
        Cette methode recherche un chemin de facon recursif 
        """
        i, j = id_courant[0], id_courant[1]
        if self.est_sommet(i, j):
            if self.hexagones.correspond_joueur(joueur):
                if val_rech in indice_sommet(i, j):
                    return True
                else:
                    return False
            else:
                return False
        elif self.hexagones.correspond_joueur(joueur):
            trouver = False
            for indice in [(i+1, j), (i-1, j), (i, j+1), (i, j-1), (i+1, j+1), (i-1, j-1)]:
                if indice != id_exclut:
                    trouver = trouver or self.rechercher(indice, id_courant, val_rech, joueur)
            return trouver
        else:
            return False

    def val_joueur(self, joueur):
        #Attribut une valeur à un joueur 
        return joueur         






