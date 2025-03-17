# jeu à 2 joueurs
# le but c'est de faire un score de 50
# chaque tour un joueur pour roll 1-6
# si le joueur fait un score différent de 1
# on augmente le score de son tour du montant qu'il a roll
# on lui demande si il veut risquer son score en continuant
# si il fait 1, son tour s'arrête et il ne gagne pas de point pour ce tour
# c'est ensuite le tour de l'autre joueur

import random
import sys

# On définit la variable qu'on nomme "scores"
# on lui donne comme valeur un tableau avec dedans 2 éléments qui valent tous les deux 0 et 0
# index d'un tableau commencent à 0
scores = [0,0]

# fonction qui renvoi un nombre random entre 1 et 6
def roll():
    return random.randint(1, 6)

# fonction qui renvoi l'index de la valeur la plus grande dans le tableau
def trouverGagnant(liste_joueur):
    return liste_joueur.index(max(liste_joueur))

print("Début de la partie\n")
# Boucle de jeu
# Tant que un des joueurs n'a pas encore atteint 50
while max(scores) < 50:
    # Début du nouveau tour
    print("********** Début d'un nouveau tour ! **********")
    # Chaque joueur joue leur tour joueur 1 puis joueur 2
    # for = pour
    # pour tous les joueurs
    # 2 joueurs -> score contient deux scores
    for joueur, score in enumerate(scores):
        # On ne continue pas si un joueur a gagné pendant son tour
        if max(scores) >= 50:
            break
        # Le tour passe à l'autre joueur
        print("C'est le tour du joueur", joueur+1, "avec un score actuel de", scores[joueur])

        # Premier roll du tour
        numero_de_roll = 1
        score_pour_le_tour = roll()
        if score_pour_le_tour == 1:
            print("Ho non c'est un 1 !! Le score pour le tour est de 0, fin du tour du joueur", joueur+1, file=sys.stderr, flush=True)
            score_pour_le_tour = 0
            break
        print("Roll N°", numero_de_roll , "\nRésultat :", score_pour_le_tour, "\nScore pour ce tour :", score_pour_le_tour)

        # Tant que c'est le tour du joueur on lui demande si il veut roll
        # On continue tant que le joueur veut ou qu'il roll un 1
        while True:
            # On demande au joueur si il veut continuer à roll
            voulez_vous_continuer = input("Voulez vous continuer ? Entrez oui ou non: ")
            # Si oui on roll encore
            if (voulez_vous_continuer.lower() == "oui"):
                roll_score = roll()
                print("Le joueur", joueur+1, "relance ! Et obtient un", roll_score)
                # Si le joueur roll un 1 c'est perdu et il n'a pas de points
                if roll_score == 1:
                    print("Ho non c'est un 1 !! Le score pour le tour est de 0, fin du tour du joueur", joueur+1, file=sys.stderr, flush=True)
                    score_pour_le_tour = 0
                    break
                # Si le joueur a obtenu un roll qui lui donne la victoire le tour s'arrête
                elif scores[joueur] + score_pour_le_tour + roll_score >= 50:
                    numero_de_roll += 1
                    score_pour_le_tour += roll_score
                    print("Roll N°", numero_de_roll , "\nRésultat :", roll_score, "\nScore pour ce tour :", score_pour_le_tour)
                    scores[joueur] += score_pour_le_tour
                    break
                # Sinon on ajoute son roll à son score pour le tour
                else:
                    numero_de_roll += 1
                    score_pour_le_tour += roll_score
                    print("Roll N°", numero_de_roll , "\nRésultat :", roll_score, "\nScore pour ce tour :", score_pour_le_tour)
            # Si il ne veut plus roll pour ce tour
            # On ajoute son score du tour à son score total et on met fin à son tour
            elif (voulez_vous_continuer.lower() == "non"):
                scores[joueur] += score_pour_le_tour
                print("Fin du tour du joueur", joueur+1)
                break

# Fin de la partie !!!
print("Fin de la partie, le joueur", trouverGagnant(scores)+1 ,"gagne !")