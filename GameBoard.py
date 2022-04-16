
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
        return True

    def couleur(self):
        #retourne la couleur de l'hexagone
        return self.etat_couleur

    def correspond_joueur(self, joueur):
        #Teste si le joueur à poser un pion sur cette case
        if self.etat_couleur==joueur:
            return True
        return False


class HexBoard:

    def __init__(self, taille=14, rayon_hex=30, token=1, etat=1):
        self.rayon_sommet = rayon_hex
        self.taille = taille
        #deux etats -> 1 : encour, 0: fin 
        self.etat = etat
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
        if self.token == joueur and self.etat:
            for i in range(self.taille):
                for j in range(self.taille) :
                    h = self.hexagones[i][j]
                    if h.est_dans_rayon(coord):
                        if h.peut_se_colorier():
                            return h.colorier(self.token), i, j
                        else:
                            return (False,)
        return (False,)
    
    def trouver_chemin(self, joueur, indice):
        #Recherche d'un chemin à partir des coordonnées d'un point
        liste_s = set()
        liste_s = self.recherche_sommets(indice, joueur, liste_s, None)
        if len(liste_s)==2:
            self.etat = 0
            return True
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

    def est_sommet_de(self, indice, joueur):
        """
        Cette methode évalu si un sommet est celui d'un 
        joueur et retourne l'indice du cote à rechercher
        """
        i, j = indice[0], indice[1]
        if i==0 :
            if joueur==1:
                return True, 1
        if i==self.taille-1 :
            if joueur==1:
                return True, -1
        if j==0 :
            if joueur==2:
                return True, 2
        if j==self.taille-1:
            if joueur==2:
                return True, -2
        return (False,)

    def sommet_joueur(self, indice, joueur):
        """
        Cette methode retourne le type de sommet correspondant à un joueur
        """
        t_sommet = self.indice_sommet(indice)
        if joueur in t_sommet:
            return joueur
        if -1*joueur in t_sommet:
            return -1*joueur    

    def est_sommet(self, indice):
        """
        Cette methode evalue si deux indices correspondent à celles d'un sommet
        """
        i, j = indice[0], indice[1]
        return i==0 or j==0 or i==self.taille-1 or j==self.taille-1

    def recherche_sommets(self, id_courant, joueur, liste_sommet, id_exclut):
        """
        Cette methode recherche les sommets à partir d'une position de facon recursive
        """
        i, j = id_courant[0], id_courant[1]
        if self.hexagones[i][j].couleur()==joueur:
            sommet = self.est_sommet_de(id_courant, joueur)
            if sommet[0] :
                sommet = sommet[1]
                if not (sommet in liste_sommet):
                    print(sommet)
                    liste_sommet.add(sommet)
                    if len(liste_sommet)==2:
                        return liste_sommet
            for indice in [(i+1, j), (i-1, j), (i, j+1), (i, j-1), (i+1, j+1), (i-1, j-1)]:
                if indice != id_exclut and self.indice_valide(indice):
                    if self.hexagones[indice[0]][indice[1]].couleur()==joueur:
                        liste_s = self.recherche_sommets(indice, joueur, liste_sommet, id_courant)
                        print("Recursion----------")
                        if len(liste_sommet) < len(liste_s):
                            liste_sommet = liste_s
            return liste_sommet
        return liste_sommet

    def val_joueur(self, joueur):
        #Attribut une valeur à un joueur 
        return joueur

    def indice_valide(self, ind):
        valide = True
        for i in ind:
            valide = valide and i>=0 and i<self.taille
        return valide






