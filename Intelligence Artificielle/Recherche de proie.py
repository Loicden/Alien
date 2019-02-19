# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 15:59:15 2019

@author: Loïc DENIS
"""

######    Algorithme de choix de proie pour deux proies    ######

# A l'attention du lecteur : 
# Dans tout le code, je recherche la portée en calculant le nombre de cases entre les unités : je ne tiens compte ni des terrains différents, ni des ennemis qui pourraient bloquer la voie.
# De plus, je n'ai pas créé de classe ennemi, il faudra le faire directement sur GM et calculer les risques et récompenses à partir de la liste des ennemis.

##### Modules #####

import numpy as nu

##### Constantes #####

A_A = 20;           # Attaque Alien
A_D = 20;           # Defense (HP) Alien
A_PM = 4;           # Points de mouvement Alien
A_x = 5;            # Abscisse Alien
A_y = 5;            # Ordonnée Alien

H1_A = 8;           # Attaque Humain 1
H1_D = 22;          # Defense Humain 1
H1_PM = 3;          # Points de mouvement Humain 1
H1_x = 7;           # Abscisse Humain 1
H1_y = 7;           # Ordonnée Humain 1

H2_A = 12;          # Attaque Humain 2
H2_D = 18;          # Defense Humain 2
H2_PM = 3;          # Points de mouvement Humain 2
H2_x = 3;           # Abscisse Humain 2
H2_y = 7;           # Ordonnée Humain 2

HMap = nu.zeros((11,11));       # Carte des positions des humains
HMap[H1_x,H1_y] = 1;
HMap[H2_x,H2_y] = 1;

Prey = [];                  # Liste des proies
Pred = [];                  # Liste des prédateurs
Pred2 = [];                 # Liste des prédateurs en cas de retraite

# On pourra aussi créer un tableau des attaques et défenses des ennemis 
# mais je vais le faire à la main pour plus de lisibilté




##### Detection des proies #####

for i in range(-A_PM-1,A_PM+2):                         # Recherche selon x
    X_test = A_x+i;                                     # Plus ou moins un car on veut être au moins adjacent à la proie
    for j in range(abs(i)-A_PM-1, A_PM-abs(i)+2):       # Selon y
        Y_test = A_y+j;
        if X_test<len(HMap) and X_test >= 0 and Y_test<len(HMap) and Y_test >= 0 :      # Si on est toujours sur la map
            if HMap[X_test,Y_test] == 1:                
                Prey.append([X_test,Y_test]);           # On remplie la liste des positions des proies
            
            
            
            
            
            

##### Calcul des récompenses #####

Bella = False                           # Variable de décision 

if len(Prey) != 0:                      # S'il y a des ennemis à portée
        
    Rec = nu.zeros(len(Prey))           # Liste des récompenses
    
    # Pour la PROIE 1 :
    if H1_D <= A_A:                     # S'il y a destruction
        Rec[0] = H1_D + H1_A;           # La récompense est la somme de l'attaque et de la defense de la proie
    else:                               # Sinon
        Rec[0] = A_A;                   # Elle est la somme des dégats infligé
                                        
    # Pour la PROIE 2:
    if H2_D <= A_A:
        Rec[1] = H2_D + H2_A;
    else :
        Rec[1] = A_A;
                                      
        
        
        
        
        
      
    ##### Calcul des risques #####
        
    Pos_Pos = []                        # Tableau des positions possibles
    Ris = [];
    Gain = [];                          # Liste des gains, qui va nous servir à la fin
    id = 0;                             # Index de la case observée (len(Prey)*4 cases en tout)
    
    
    
    
    # Pour la PROIE 1 :
    
    for i in range(-1,2):
        for j in range(-1+abs(i),1-abs(i)+1):                           # On regarde toutes les cases adjacentes à celle de la proie
            if i != 0 or j != 0:                                        # Si on est pas sur la proie
                if (abs((H1_x+i)-A_x) + abs((H1_y+j)-A_y)) <= A_PM:     # Si l'on est toujours à portée de cette case
                    Pos_Pos.append([(H1_x+i),(H1_y+j)])
                    Ris.append(0)                                       # On sait qu'on va calculer un gain et un risque, on fait de la place dans le tableau
                    Gain.append(0)
                    
    # Detection des predateurs 
                    for k in range(-10,10+1):                           # Recherche selon x
                        X_test = H2_x+i+k;
                        for l in range(abs(k)-10, 10-abs(k)+1):         # Selon y
                            Y_test = H2_y+j+l;
                            if X_test<len(HMap) and X_test >= 0 and Y_test<len(HMap) and Y_test >= 0 :      # Si on est toujours sur la map
                                if HMap[X_test,Y_test] == 1:                            # Si la case correspond à un predateur
                                    if X_test == H1_x and Y_test == H1_y:               # Si la proie est celle que l'on attaque
                                        if A_A < H1_D :                                 # Si pas de destruction
                                            Pred.append([X_test,Y_test]);               # Créer une liste des prédateurs à portée, ne sert pas pour la suite de l'algo mais utile sur Gamemaker
                                    else:
                                        if (abs((H1_x+i)-X_test) + abs((H1_y+j)-Y_test)) <= H2_PM+1 :     # On regarde si le prédateur est à portée (Si c'est la cible qu'on attaque, elle est forcement à portée) 
                                            Pred.append([X_test,Y_test]);
                                
    # Risque
                    if A_D <= H2_A+H1_A:        # H2_A+H1_A est en fait l'attaque de TOUS les predateurs dans la liste
                        Ris[id] = A_D + A_A;    # Risque en cas de destruction de l'alien
                    else :
                        Ris[id] = H2_A;         # Non destruction
                
    # Gain  
                                                        
                    Gain[id] = Rec[0]-Ris[id]   # Significatif de la meilleure option ; Rec[0] car on est dans la partie du tableau qui correspond à la proie 1
                    id += 1;
                
              
                
                
                
           
    # Pour la PROIE 2 :
    
    for i in range(-1,2):
        for j in range(-1+abs(i),1-abs(i)+1):                           # On regarde toutes les cases adjacentes à celle de la proie
            if i != 0 or j != 0:                                        # Si on est pas sur la proie
                if (abs((H2_x+i)-A_x) + abs((H2_y+j)-A_y)) <= A_PM:     # Si l'on est toujours à portée de cette case
                    Pos_Pos.append([(H2_x+i),(H2_y+j)])
                    Ris.append(0)                                       # On sait qu'on va calculer un gain et un risque, on fait de la place dans le tableau 
                    Gain.append(0)
                    
    # Detection des predateurs 
                    for k in range(-10,10+1):                           # Recherche selon x, le 10 est arbitraire
                        X_test = H2_x+i+k;                              # On regarde les cases depuis la position considérée
                        for l in range(abs(k)-10, 10-abs(k)+1):         # Selon y
                            Y_test = H2_y+j+l;
                            if X_test<len(HMap) and X_test >= 0 and Y_test<len(HMap) and Y_test >= 0 :      # Si on est toujours sur la map
                                if HMap[X_test,Y_test] == 1:                            # Si la case correspond à un predateur
                                    if X_test == H2_x and Y_test == H2_y:               # Si la proie est celle que l'on attaque
                                        if A_A < H2_D :                                 # Si pas de destruction
                                            Pred.append([X_test,Y_test]);               # Créer une liste des prédateurs à portée, ne sert pas pour la suite de l'algo mais utile sur Gamemaker
                                    else:
                                        if (abs((H2_x+i)-X_test) + abs((H2_y+j)-Y_test)) <= H1_PM+1 :     # On regarde si le prédateur est à portée (Si c'est la cible qu'on attaque, elle est forcement à portée)
                                            Pred.append([X_test,Y_test]);
    # Risque
                    if A_D <= H1_A:                     # H1_A est en fait l'attaque de TOUS les predateurs de la liste
                        Ris[id] = A_D + A_A;            # Risque en cas de destruction
                    else :
                        Ris[id] = H1_A;                 # Non destruction
                
    # Gain  
                                                        
                    Gain[id] = Rec[1]-Ris[id]           # Significatif de la meilleure option ; Rec[1] car on est dans la partie du tableau qui correspond à la proie 2
                    id += 1;
    
    ## Lors du calcul de risque, l'IA prend en compte les ennemis que j'ai rentré à la main, et pas ceux qu'elle a détecté juste avant.
    ## Il faudra le faire directement sur GM avec la fonction qui donne les attributs d'une case et de l'unité sur celle-ci.
    
    ##### Décision #####
    
    print ('Position Alien = ', [A_x,A_y]);
    print ('Position Humain1 = ', [H1_x,H1_y]);
    print ('Position Humain2 = ', [H2_x,H2_y]);
    print ('Prey : ', Prey)
    print ('Pred : ', Pred)
    print ('Option : ', Pos_Pos);
    print ('Gain pour chaque option : ', Gain);
    
    D = max(Gain);
    print('Le gain maximal est de ',D);
    
    if D >= 10 :                            # C'est peut-être intelligent de mettre zéro   
        Bella = True
        i = Gain.index(D);
        [A_x,A_y] = Pos_Pos[i];             # L'alien se déplace à la case qui correspond à un meilleur gain
        print("L'Alien se déplace sur : ", [A_x,A_y])
        # L'alien attaque
        
    else :
        pass                                # Si le gain est pas fou dans tout les cas, on choisira une autre option
        print("L'Alien n'attaque pas.")

else :
    pass            # Refaire TOUT l'algo depuis détection des proies, mais cette fois en doublant la zone de recherche (On regarde deux tours à l'avance)

##### En cas de retraite #####

if Bella == False :                         # S'il n'y a pas d'ennemi à portée, ou si les gains ne sont pas fous.
    
    ##### Calcul des risques #####          # Même algo qu'avant mais avec TOUTES les cases à portée.
        
    Pos_Pos2 = []                           # Tableau des positions possibles
    Ris2 = [];
    id = 0;
    
    for i in range(-A_PM , A_PM+1):                     # Recherche selon x
        X_test = A_x+i;
        for j in range(abs(i)-A_PM-1, A_PM-abs(i)+2):       # Selon y
            Y_test = A_y+j;
            if X_test<len(HMap) and X_test >= 0 and Y_test<len(HMap) and Y_test >= 0 :      # Si on est toujours sur la map
                if HMap[X_test,Y_test] != 1:                # Si la case n'est pas sur un ennemi
                    Pos_Pos2.append([(H1_x+i),(H1_y+j)])
                    Ris2.append(0)                           # On sait qu'on va calculer un risque, on fait de la place dans le tableau
                    
    # Detection des predateurs 
                    for k in range(-10,10+1):                           # Recherche selon x
                        X_test = H2_x+i+k;
                        for l in range(abs(k)-10, 10-abs(k)+1):         # Selon y
                            Y_test = H2_y+j+l;
                            if X_test<len(HMap) and X_test >= 0 and Y_test<len(HMap) and Y_test >= 0 :      # Si on est toujours sur la map
                                if HMap[X_test,Y_test] == 1:                            # Si la case correspond à un predateur
                                    if (abs((H1_x+i)-X_test) + abs((H1_y+j)-Y_test)) <= H2_PM+1 :     # On regarde si le prédateur est à portée (Si c'est la cible qu'on attaque, elle est forcement à portée) 
                                        Pred2.append([X_test,Y_test]);
                                
    # Risque
                    if A_D <= H2_A+H1_A:            # H2_A+H1_A est en fait l'attaque de TOUS les predateurs dans la liste
                        Ris2[id] = A_D + A_A;       # Risque en cas de destruction de l'alien
                    else :
                        Ris2[id] = H2_A;            # Non destruction
                    id += 1;
                
    R = min(Ris2);
    print ('Le risque minimum est de ', R)
    i = Ris2.index(R);
    [A_x,A_y] = Pos_Pos[i];             # L'alien se déplace à la case qui correspond au risque minimum
    print("L'Alien se déplace sur : ", [A_x,A_y])
    