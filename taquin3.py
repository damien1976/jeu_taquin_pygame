import matplotlib.image as img
from numpy import multiply, ones, array
from random import shuffle
import pygame as pg
#import sys

# Couleurs
BLACK=(0,0,0)
WHITE=(255, 255, 255)

# Jeu du taquin
filename = 'poisson.jpg'

# Ouverture
image = img.imread(filename)
image=image.transpose((1,0,2))

# Dimensions de l'image
l_x, l_y, _ = image.shape

# Caractéristiques du découpage de l'image
nb_x = 4
nb_y = 3

taille_x=l_x//nb_x 
taille_y=l_y//nb_y

# Dimensions de la fenêtre
WINDOW_HEIGHT=taille_x*nb_x
WINDOW_WIDTH=taille_y*nb_y


# Découpage de l'image, tranformation des vignettes en surfaces pygame et mise dans un tableau 2D
tab=[]

for i in range(nb_x):
    l=[]
    for j in range(nb_y):
        #On grise la case en bas à droite
        if i==nb_x-1 and j==nb_y-1:
            image[taille_x*i:taille_x*(i+1),taille_y*j:taille_y*(j+1),:]=multiply(ones((taille_x, taille_y,3), dtype='int'), 127)
        # On convertit les vignettes en surface pygame
        l.append(pg.pixelcopy.make_surface(image[taille_x*i:taille_x*(i+1),taille_y*j:taille_y*(j+1),:]))
    tab.append(l)

# Mise sous forme d'une liste
tab2=array(tab).reshape(1,nb_x*nb_y)[0] # liste des numéros des vignettes

# Mélange des vignettes
L=[x for x in range(nb_x*nb_y)]
shuffle(L) 
L=array(L).reshape(nb_y, nb_x) # La vignette i,j dans l'image de départ se trouve à l'emplacement L[i][j]

# Tester si une vignette k, l se trouve dans la grille
def est_dans_grille(k, l):
    if k>=0 and l>=0 and l<nb_x and k<nb_y:
        return True
    else:
        return False

# Tester si une vignette k,l est voisine de la vignette grise (nb_x, nb_y)
def voisine(k, l):
    if est_dans_grille(k+1, l):
        if L[k+1][l]==nb_x*nb_y-1:
            return k+1, l, True
    if est_dans_grille(k-1,l):
        if L[k-1][l]==nb_x*nb_y-1:
            return k-1, l, True
    if est_dans_grille(k,l-1):
        if L[k][l-1]==nb_x*nb_y-1:
            return k, l-1, True
    if est_dans_grille(k,l+1):
        if L[k][l+1]==nb_x*nb_y-1:
            return k, l+1, True
    return  -1, -1, False

# Tester si le puzzle est reconstitué
def gagne(L):
    for j in range(nb_y):
        for i in range(nb_x):
            if L[j][i]!=j*nb_x+i:
                return False
    return True

# Classe Bouton
class Bouton(pg.sprite.Sprite):
    def __init__(self, i, j):
        super().__init__()
        self.i=i
        self.j=j
        self.image=pg.Surface([taille_x, taille_y])
        pg.draw.rect(self.image, WHITE, [i*taille_x, j*taille_y, taille_x, taille_y])
        self.rect = self.image.get_rect()

#This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pg.sprite.Group()

def drawgrid():
    for i in range(nb_x):
        for j in range(nb_y):
            bouton = Bouton(i,j)
            bouton.rect.x=i*taille_x
            bouton.rect.y=j*taille_y
            bouton.image=tab2[L[j][i]]
            all_sprites_list.add(bouton)
            
        

pg.init()
screen = pg.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
pg.display.set_caption('Jeu du taquin')

#Allowing the user to close the window...
carryOn = True
#clock=pg.time.Clock()

drawgrid()
 
while carryOn:
        for event in pg.event.get():
            if event.type==pg.QUIT:
                carryOn=False
            
            # handle MOUSEBUTTONUP
            if event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()

                for s in all_sprites_list:
                    if s.rect.collidepoint(pos):
                        # On récupère les positions de la case courante
                        i1,j1=s.i, s.j
                        # On récupère les positions de la case grise
                        k0,l0, voisin=voisine(s.j,s.i)

                        # Mise à jour de l'image qui devient case grise 
                        if voisin:
                            s.image=tab2[L[k0][l0]]
                        break
                    
                # Recherche puis mise à jour de la case grise qui devient image          
                for s in all_sprites_list:
                    if voisin and s.i==l0 and s.j==k0:
                        s.image=tab2[L[j1][i1]]
                        break

                # Mise à jour de la table L dans le cas où une permutation est possible
                if voisin:
                    nb=L[j1][i1]
                    L[j1][i1]=nb_x*nb_y-1
                    L[k0][l0]=nb

                i1, j1, k0, l0, voisin = -1, -1, -1, -1, False
                          
        #Game Logic
        all_sprites_list.update()
 
        #Now let's draw all the sprites in one go. (For now we only have 1 sprite!)
        all_sprites_list.draw(screen)
 
        #Refresh Screen
        pg.display.flip()
 
        #Number of frames per secong e.g. 60
        #clock.tick(60)
 
pg.quit()
