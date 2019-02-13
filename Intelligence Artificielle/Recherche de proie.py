# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 15:59:15 2019

@author: Loïc DENIS
"""

######    Algorithme de choix de proie pour deux proies    ######

##### Modules #####

import numpy as nu

##### Constantes #####

A_A = 20;           # Attaque Alien
A_D = 20;           # Defense (HP) Alien
A_PM = 16;           # Points de mouvement Alien
A_x = 5;            # Abscisse Alien
A_y = 5;            # Ordonnée Alien

H1_A = 8;           # Attaque Humain 1
H1_D = 22;          # Defense Humain 1
H1_PM = 4;          # Points de mouvement Humain 1
H1_x = 7;           # Abscisse Humain 1
H1_y = 7;           # Ordonnée Humain 1

H2_A = 12;          # Attaque Humain 2
H2_D = 18;          # Defense Humain 2
H2_PM = 4;          # Points de mouvement Humain 2
H2_x = 3;           # Abscisse Humain 2
H2_y = 7;           # Ordonnée Humain 2

HMap = nu.zeros((11,11));       # Carte des positions des humains
HMap[H1_x,H1_y] = 1;
HMap[H2_x,H2_y] = 1;

Prey = [];                  # Liste des proies
Pred = [];                  # Liste des prédateurs

# On pourra aussi créer un tableau des attaques et défenses des ennemis 
# mais je vais le faire à la main pour plus de lisibilté




##### Detection des proies #####

for i in range(-A_PM-1,A_PM+2):                         # Recherche selon x
    X_test = A_x+i;                                     # Plus ou moins un car on veut être au moins adjacent à la proie
    for j in range(abs(i)-A_PM-1, A_PM-abs(i)+2):       # Selon y
        Y_test = A_y+j;
        if X_test<len(HMap) and X_test >= 0 and Y_test<len(HMap) and Y_test >= 0 :      # Si on est toujours sur la map
            if HMap[X_test,Y_test] == 1:                    # On remplie la liste des positions des proies
                Prey.append([X_test,Y_test]);
            
            
            
            
            
            

##### Calcul des récompenses #####
            
Rec = nu.zeros(len(Prey))           # Liste des récompenses

# Pour la PROIE 1 :
if H1_D <= A_A:                     # S'il y a destruction
    Rec[0] = H1_D + H1_A;           # La récompense est la somme de l'attaque et de la defense de la proie
else:                               # Sinon
    Rec[0] = A_A + H1_A;            # Elle est la somme des dégats infligé et de l'attaque de la proie
                                    # J'ai choisi l'attaque plutôt que la défense arbitrairement (plus juste)
                                    
# Pour la PROIE 2:
if H2_D <= A_A:
    Rec[1] = H2_D + H2_A;
else :
    Rec[1] = A_A + H2_A;
                                  
    
    
    
    
    
  
##### Calcul des risques #####
    
Pos_Pos = []                        #Tableau des positions possibles
Ris = [];
Gain = [];          # Liste des gains, qui va nous servir à la fin
id = 0;                             # Index de la case observée (len(Prey)*4 cases en tout)




# Pour la PROIE 1 :

for i in range(-1,2):
    for j in range(-1+abs(i),1-abs(i)+1):                     # On regarde toutes les cases adjacentes à celle de la proie
        if i != 0 or j != 0:                                        # Si on est pas sur la proie
            if (abs((H1_x+i)-A_x) + abs((H1_y+j)-A_y)) <= A_PM:     # Si l'on est toujours à portée de cette case
                Pos_Pos.append([(H1_x+i),(H1_y+j)])
                Ris.append(0)                                       # On sait qu'on va calculer un gain et un risque, on fait de la place dans le tableau
                Gain.append(0)
                
# Detection des predateurs 
                for k in range(-10,10+1):                             # Recherche selon x
                    X_test = H2_x+i+k;
                    for l in range(abs(k)-10, 10-abs(k)+1):           # Selon y
                        Y_test = H2_y+j+l;
                        if X_test<len(HMap) and X_test >= 0 and Y_test<len(HMap) and Y_test >= 0 :      # Si on est toujours sur la map
                            if HMap[X_test,Y_test] == 1:                            # Si la case correspond à un predateur
                                if X_test == H1_x and Y_test == H1_y:               # Si la proie n'est pas celle que l'on detruit
                                    if A_A <= H1_D :                                # Si destruction
                                        Pred.append([X_test,Y_test]);               # Créer une liste des prédateurs à portée, ne sert pas pour la suite de l'algo mais utile sur Gamemaker
                                else:
                                    Pred.append([X_test,Y_test]);
                            
# Risque
                if A_D <= H2_A+H1_A:        # H2_A+H1_A est en fait l'attaque de TOUS les predateurs qui ont la portée
                    Ris[id] = A_D + A_A;    # Risque en cas de destruction
                else :
                    Ris[id] = H2_A;         # Non destruction
            
# Gain  
                                                    
                Gain[id] = Rec[0]-Ris[id]   # Significatif de la meilleure option ; Rec[0] car on est dans la partie du tableau qui correspond à la proie 1
                id += 1;
            
          
            
            
            
       
# Pour la PROIE 2 :

for i in range(-1,2):
    for j in range(-1+abs(i),1-abs(i)+1):                     # On regarde toutes les cases adjacentes à celle de la proie
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
                                if X_test == H2_x and Y_test == H2_y:               # Si la proie n'est pas celle que l'on detruit
                                    if A_A <= H2_D :                                # Si destruction
                                        Pred.append([X_test,Y_test]);               # Créer une liste des prédateurs à portée, ne sert pas pour la suite de l'algo mais utile sur Gamemaker
                                else:
                                    Pred.append([X_test,Y_test]);
# Risque
                if A_D <= H1_A:                     # H1_A est en fait l'attaque de TOUS les predateurs qui ont la portée
                    Ris[id] = A_D + A_A;            # Risque en cas de destruction
                else :
                    Ris[id] = H1_A;                 # Non destruction
            
# Gain  
                                                    
                Gain[id] = Rec[1]-Ris[id]           # Significatif de la meilleure option ; Rec[1] car on est dans la partie du tableau qui correspond à la proie 2
                id += 1;



##### Décision #####

print ('Position Alien = ', [A_x,A_y]);
print ('Position Humain1 = ', [H1_x,H1_y]);
print ('Position Humain2 = ', [H2_x,H2_y]);
print ('Option : ', Pos_Pos);
print ('Gain pour chaque option : ', Gain);

D = max(Gain);
print('Le gain maximal est de ',D);

if D >= 10 :       
    i = Gain.index(D);
    [A_x,A_y] = Pos_Pos[i];             # L'alien se déplace à la case qui correspond à un meilleur gain
    print("L'Alien se déplace sur : ", [A_x,A_y])
    # L'alien attaque
    
else :
    [A_x,A_y] = [A_x,A_y];              # Prévoir une solution de retrait si le gain est pas fou dans tout les cas (négatif par exemple)
    print("L'Alien n'attaque pas.")




'''
PROBLEMES :
    Je recherche les prédateurs selon les PM de l'alien et non les PM des enemis aux alentours
'''