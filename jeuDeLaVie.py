# -*- coding: utf-8 -*-

##    This program is a simple implement of the game of life.
##    Copyright (C) 2014  Frédéric Micout - gameoflife@sujets-libres.fr
##
##    This program is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from tkinter import *
from math import *
from random import randrange	   # générateur de nombres aléatoires
import time

# =============== Fonctions ===============

# Dessine un cercle
def cercle(x, y, r, coul):
    can1.create_oval(x-r, y-r, x+r, y+r, fill=coul)
    can1.pack()

# Initialiser le tableau
def initTableau():
    global tab
    tab = [['0'] * nbColonnes for _ in range(nbLignes)]

# Ajoute des pions de manière aléatoire
def ajouter_pion_aleatoire():
    # tirer au hasard les coordonnées des pions :
    for i in range (nbPionsAleatoires):        
        x = c/2 + randrange(nbColonnes) * c
        y = c/2 + randrange(nbLignes) * c
        tab[int(y/c)][int(x/c)] = '1'

# Pause de l'animation
def pauseAction():
    global pause
    pause = not pause

# Démarre le traitement
def demarrer():
    global jeuEnCours, fin  
    jeuEnCours = not jeuEnCours

    if jeuEnCours:        
        b1.config(text = u'Arrêter')
        ajouter_pion_aleatoire()
        while not fin:        
            time.sleep(1/(2*sqrt(compteDisque())))
            
            #if chercheBlocage() == 0:        # Permet de relancer la vie s'il n'y en a plus de nouvelle à naitre (Décommentez les deux lignes si besoin)
            #    ajouter_pion_aleatoire()
            
            if not pause:
                # Génération tableau suivant
                majTableau()
                affichage()
            can1.update()
    else:        
        b1.config(text = u'Démarrer')
        initTableau()
        can1.update()
            

# Affiche le tableau
def affichage():       
    can1.delete("all")
    for j in range(nbLignes):
        res = ""
        for i in range(nbColonnes):
            res += tab[j][i]
            if tab[j][i] == '1': # disque naissant
                cercle(i*c + c/2 + 1, j*c + c/2 + 1, c/2, '#ff9900')
            elif tab[j][i] == '2': # disque ancien
                cercle(i*c + c/2 + 1, j*c + c/2 + 1, c/2, '#ffdd00')  
            elif tab[j][i] == '3': # disque ancien
                cercle(i*c + c/2 + 1, j*c + c/2 + 1, c/2, '#ffff99')    

# Génére le tableau suivant
def majTableau():
    
    tabTmp = [[0] * nbColonnes for _ in range(nbLignes)]

    # Analyse du tableau précédent
    for j in range(nbLignes):
        for i in range(nbColonnes):
            nbCellulesVivantesAdjacentes = 0
        
            # Ligne du haut, colonne à gauche
            if tab[(j-1)%nbLignes][(i-1)%nbColonnes] != '0':
                nbCellulesVivantesAdjacentes += 1
                
            # Ligne du haut, colonne au centre     
            if tab[(j-1)%nbLignes][i] != '0':
                nbCellulesVivantesAdjacentes += 1
               
            # Ligne du haut, colonne à droite
            if tab[(j-1)%nbLignes][(i+1)%nbColonnes] != '0':
                nbCellulesVivantesAdjacentes += 1
                
            # Ligne au centre, colonne à gauche
            if tab[j][(i-1)%nbColonnes] != '0':
                nbCellulesVivantesAdjacentes += 1
                
            # Ligne au centre, colonne à droite
            if tab[j][(i+1)%nbColonnes] != '0':
                nbCellulesVivantesAdjacentes += 1
                
            # Ligne du bas, colonne à gauche  
            if tab[(j+1)%nbLignes][(i-1)%nbColonnes] != '0':
                nbCellulesVivantesAdjacentes += 1
               
            # Ligne du bas, colonne au centre 
            if tab[(j+1)%nbLignes][i] != '0':
                nbCellulesVivantesAdjacentes += 1
               
            # Ligne du bas, colonne à droite 
            if tab[(j+1)%nbLignes][(i+1)%nbColonnes] != '0':
                nbCellulesVivantesAdjacentes += 1
                
            tabTmp[j][i] = nbCellulesVivantesAdjacentes

    # Mise à jour du nouveau tableau
    for j in range(nbLignes):
        for i in range(nbColonnes):
            
            # Si la cellule était naissante au tour précédent, elle ne le sera de toute manière plus à cet instant
            if tab[j][i] == '2':
                tab[j][i] = '3'
                
            if tab[j][i] == '1':
                tab[j][i] = '2'

            # Vie et mourt des cellules
            if tabTmp[j][i] == 3 and tab[j][i] == '0': # Devient vivante
                tab[j][i] = '1'
            elif tabTmp[j][i] < 2 or tabTmp[j][i] > 3: # Meurt
                tab[j][i] = '0'
                

# Compte le nombre de disques à afficher
def compteDisque():
    nbDisquesAAfficher = 1
    for j in range(nbLignes):
        nbDisquesAAfficher += tab[j].count('1') + tab[j].count('2') + tab[j].count('3')
    return nbDisquesAAfficher

# Détermine si on a atteint une position de bloquage (plus de cellule dont la durée de vie = 2)
def chercheBlocage():
    nbDisquesVieDureeDeux = 0
    for j in range(nbLignes):
        nbDisquesVieDureeDeux += tab[j].count('2')
    return nbDisquesVieDureeDeux

# Sortie de l'application
def quitter():
    global pause, fin
    pause = False
    fin = True
    fen1.quit()


# Gestion des événements liés à l'appui des touches
# Effet touche "return"
def toucheReturn(event):
    ajouter_pion_aleatoire()

# Effet touche "p"
def toucheP(event):
    pauseAction()

# Effet touche "d"
def toucheD(event):
    demarrer()

# Effet touche "q"
def toucheQ(event):
    quitter()
    

# ========== Programme principal ==========

# Variables globales
c = 14		  # taille des carrés
nbLignes = 30     # Nombre de lignes dans le tableau (60)
nbColonnes = 60   # Nombre de colonnes dans le tableau (119)
pause = False     # Indique si le jeu doit etre mis en pause
jeuEnCours = False  # Indique qu'un jeu est en cours (en pause ou non)
fin = False       # L'application est toujours utilisable
nbPionsAleatoires = int(nbColonnes*nbLignes/7) # Le nombre de pions à positionner aléatoirement est fonction de la taille de la zone

# Initialisation du tableau
initTableau()

# Widget principal
fen1 = Tk()
fen1.title(u"Jeu de la vie - %s x %s" % (nbColonnes,nbLignes))

# Widgets enfants
can1 = Canvas(fen1,bg='grey',height=c*nbLignes+2, width=c*nbColonnes+2)
can1.pack(side =TOP, padx =5, pady =5)

b1 = Button(fen1, width=10, text = u'Démarrer', command=demarrer)
b1.pack(side =LEFT, padx =3, pady =3)

b2 = Button(fen1, text =u'Pause', command=pauseAction)
b2.pack(side =LEFT, padx =3, pady =3)

b3 = Button(fen1, text =u'Ajouter %s pions aléatoirement' % (nbPionsAleatoires), command=ajouter_pion_aleatoire)
b3.pack(side =LEFT, padx =3, pady =3)

b4 = Button(fen1, text =u'Quitter', command=quitter)
b4.pack(side =RIGHT, padx =3, pady =3)

# Gestion du clavier
fen1.bind("<Return>", toucheReturn) # Ajout pions aléatoirement
fen1.bind("<p>", toucheP) # Pause
fen1.bind("<d>", toucheD) # Démarrer / Arrêter
fen1.bind("<q>", toucheQ) # Quitter l'application

# Démarrage du réceptionnaire d'événements
fen1.mainloop()

# Destruction de la fenetre
fen1.destroy()
