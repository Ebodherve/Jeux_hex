
class HexagonesBoard:

    def __init__(self, etat_couleur=None, taille_grille=14, rayon=30, centre=(100, 100), indice=(0,0)):
        self.etat_couleur = etat_couleur
        self.taille = taille_grille
        self.rayon = rayon
        self.centre = centre
        self.indice = indice
        self.sommet = self.suis_je_sommet()
        self.indices_frere_ignores = []

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

    def suis_je_sommet(self, taille=None):
        """
        Cette methode evalue si deux indices correspondent à celles d'un sommet
        """
        taille = taille if taille else self.taille
        i, j = self.indice[0], self.indice[1]
        if i==0 and j==0:
            return True, 1, 2
        elif i==taille-1 and j==taille-1:
            return True, -1, -2
        elif i==0 and j==taille-1:
            return True, 1, -2
        elif i==taille-1 and j==0:
            return True, -1, 2
        elif i==0:
            return True, 1
        elif i==taille-1:
            return True, -1
        elif j==0:
            return True, 2
        elif j==taille-1:
            return True, -2
        else:
            return (False,)

    def est_sommet(self):
        return self.sommet[0]

    def est_sommet_joueur(self, joueur):
        return self.sommet[0] and abs(self.couleur_sommet())==self.etat_couleur

    def couleur_sommet(self, taille=None):
        i,j = self.indice
        taille = taille if taille else self.taille
        if i==0 and j==0:
            if self.etat_couleur==1:
                return self.sommet[1]
            else:
                return self.sommet[2]
        elif i==taille-1 and j==taille-1:
            if self.etat_couleur==1:
                return self.sommet[1]
            else:
                return self.sommet[2]
        elif i==0 and j==taille-1:
            if self.etat_couleur==1:
                return self.sommet[1]
            else:
                return self.sommet[2]
        elif i==taille-1 and j==0:
            if self.etat_couleur==1:
                return self.sommet[1]
            else:
                return self.sommet[2]
        else:
            try:
                return self.sommet[1]
            except:
                pass

    def supprime_frere(self, ind):
        """
        Cette methode indique les indices d'hexagones à ne pas prendre comme frere
        """
        self.indices_frere_ignores.append(ind)

    def freres(self):
        """
        Cette methode retourne la liste des indices des hexagones consideres comme freres
        """
        freres = []
        i, j = self.indice
        for ind in [(i+1, j), (i-1, j), (i, j+1), (i, j-1), (i+1, j-1), (i-1, j+1)]:
            if not ind in self.indices_frere_ignores:
                freres.append(ind)
        return freres

    def reinit_frerres(self):
        self.indices_frere_ignores = []

    def indice_self(self):
        return self.indice


class HexBoard:

    def __init__(self, hexview=None, taille=14, rayon_hex=30, token=1, etat=1):
        self.rayon_sommet = rayon_hex
        self.taille = taille
        #deux etats -> 1 : encour, 0: fin 
        self.etat = etat
        self.token = token
        self.hexagones = [[] for i in range(taille)]
        self.joueur1 = 1
        self.joueur2 = 2
        self.joueur_arriere = None
        self.dernier_coup = None
        self.hexview = hexview

    def setjoueurs(self, joueur1, joueur2):
        self.joueur1 = joueur1
        self.joueur2 = joueur2

    def ajout_joueur_arriere(self, joueur):
        self.joueur_arriere = joueur
        self.joueur_arriere.ajouthexboard(self)

    def set_hexview(self, hexview):
        self.hexview = hexview

    def construire_tableau(self):
        sommet = 2*self.rayon_sommet, 2*self.rayon_sommet
        hexagones = [[] for i in range(self.taille)]
        self.hexagones = [[] for i in range(self.taille)]
        for i in range(self.taille):
            hexagones[i].append(sommet)
            self.hexagones[i].append(HexagonesBoard(rayon=self.rayon_sommet, taille_grille=self.taille, centre=sommet, indice=(i,0)))
            for j in range(1,self.taille):
                h = hexagones[i][-1]
                h = h[0]+ 2*self.rayon_sommet, h[1]
                hexagones[i].append(h)
                self.hexagones[i].append(HexagonesBoard(rayon=self.rayon_sommet, taille_grille=self.taille, centre=h, indice=(i,j)))
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
                            self.dernier_coup = (i,j)
                            rep_coloriage = h.colorier(self.token)
                            self.changer_token()
                            return rep_coloriage, i, j
                        else:
                            return (False,)
        return (False,)
    
    def trouver_chemin(self, joueur, indice):
        #Recherche d'un chemin à partir des coordonnées d'un point
        liste_s = self.recherche_sommets(indice, joueur)
        if len(liste_s)==2:
            self.etat = 0
            return True
        return False

    def sommet_joueur(self, indice, joueur):
        """
        Cette methode retourne le type de sommet correspondant à un joueur
        """
        t_sommet = self.indice_sommet(indice)
        if joueur in t_sommet:
            return joueur
        if -1*joueur in t_sommet:
            return -1*joueur    

    def changer_token(self):
        """
        Cette methode permet de modifier le token apres qu'un joueur ait joué
        """
        if self.token == self.joueur1:
            self.token = self.joueur2
        else:
            self.token = self.joueur1 

    def recherche_sommets(self, id_courant, joueur):
        """
        Cette methode recherche les sommets à partir d'une position de facon 
        recursive dans la grille d'hexagone les sommets potentielle sont : 1, -1, 2, -2
        """
        i, j = id_courant[0], id_courant[1]
        liste_hex = [self.hexagones[i][j]]
        liste_sommet = []
        liste_reinit = []
        while len(liste_hex)>0 and len(liste_sommet)<2:
            h = liste_hex[0]
            if h.est_sommet_joueur(joueur):
                sommet = h.couleur_sommet()
                if not sommet in liste_sommet:
                    liste_sommet.append(sommet)
            liste_hex = liste_hex[1:]
            for frere in h.freres():
                if self.indice_valide(frere):
                    i,j = frere
                    ind = h.indice_self()
                    h_frere = self.hexagones[i][j]
                    if h_frere.couleur()==h.couleur():
                        h_frere.supprime_frere(ind)
                        liste_hex.append(h_frere)
            liste_reinit.append(h)
        for h in liste_reinit:
            h.reinit_frerres()
        return liste_sommet

    def val_joueur(self, joueur):
        #Attribut une valeur à un joueur 
        return joueur

    def indice_valide(self, ind):
        """
        Cette methode teste si les indices d'un pion sont valides
        """
        valide = True
        for i in ind:
            valide = valide and i>=0 and i<self.taille
        return valide

    def dernier_coup_jouer(self):
        #cette methode permet d'acceder au dernier coup joué par le joueur
        return self.dernier_coup

    def colorier_hex_arriere(self, ind, couleur, nom):
        """
        Interface de jeu pour le joueur arriere plan : Random ou Ia 
        """
        i, j = ind
        if self.hexagones[i][j].peut_se_colorier() and self.etat and couleur==self.token:
            self.hexagones[i][j].colorier(couleur)
            self.hexview.colorier_hex(ind, couleur)
            trouver = self.trouver_chemin(couleur, ind)
            self.changer_token()
            if trouver:
                self.hexview.victoire(nom)

