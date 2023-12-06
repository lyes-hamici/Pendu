import random
import unidecode
import pygame
import sys
from pygame.locals import *
from button import Button


pygame.init()

WIDTH = 1280

HEIGHT = 720

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

white = (255 , 255 , 255)

pygame.display.set_caption("Menu")

BG = pygame.image.load("images/Background.png")


def mot_aleatoire(fichier_mot):

    with open(fichier_mot, 'r') as fichier:

        lignes = fichier.readlines()

        mots = random.choice(lignes).strip().upper()
        
        mots = unidecode.unidecode(mots)

        return  mots



        


def get_font(size): 

    return pygame.font.Font("images/font.ttf", size)



def afficher_texte(texte, x, y, couleur=white):

    texte_affiche = get_font(20).render(texte, True, couleur)

    SCREEN.blit(texte_affiche, (x, y))


def ajout_mots(liste_mots):
    running = True
    ajout_mot = ""
    while running:
        SCREEN.blit(BG,(0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
                if event.key == pygame.K_RETURN:
                    # Enregistre le nouveau mot dans la liste des mots
                    with open(liste_mots, "a") as fichier:
                        fichier.write('\n' + ajout_mot.lower())
                    ajout_mot = ""  
                else:
                    lettre = chr(event.key)
                    ajout_mot += lettre

        afficher_texte("Appuyez sur Echap pour revenir sur l'ecran d'aceuill", 100, 600)
        afficher_texte("La touche 'Entrer' valide vôtre choix :", 100, 200)
        afficher_texte(f"Nouveau mot : {unidecode.unidecode(ajout_mot)}", 100, 150)  

        pygame.display.update()
    
def main_menu():

    while True:

        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")

        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("images/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        
        ADD_BUTTON = Button(image=pygame.image.load("images/Options Rect.png"), pos=(640, 400), 
                            text_input="Ajout", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        
        QUIT_BUTTON = Button(image=pygame.image.load("images/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON,ADD_BUTTON]:

            button.changeColor(MENU_MOUSE_POS)

            button.update(SCREEN)

        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()

                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):

                    main_game()

                if ADD_BUTTON.checkForInput(MENU_MOUSE_POS):
                    ajout_mots("liste_mots.txt")

                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):

                    pygame.quit()

                    sys.exit()


        pygame.display.update()



def main_game():
    global mot_initial, input_lettre , Mots_

    pygame.draw.rect(SCREEN, (150, 150, 150), (400, 200, 200, 50))

    mot_initial = mot_aleatoire("liste_mots.txt")

    print(mot_initial)

    print("------------------------")

    input_lettre = set()

    Mots_ = ["_" for _ in mot_initial]

    running = True

    nombre_vie = 1

    SCREEN.blit(BG, (0, 0))

    while running:

        if nombre_vie == 9:

            Perdu()

        elif ''.join(Mots_) == mot_initial :

            Victoire()

        # Charger l'image à chaque 'erreur' (perte de vie)

        image = pygame.image.load(f"images/pendu{nombre_vie}.png")

        image_width, image_height = image.get_rect().size

        # Position du pendu

        image_x = (WIDTH - image_width) // 2  

        image_y = 10 


        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    main_menu()

                if event.unicode.isalpha():

                    letter = event.unicode.upper()

                    input_lettre.add(letter) 

                    if letter in mot_initial:   

                        for i in range(len(mot_initial)):

                            if mot_initial[i] == letter:

                                Mots_[i] = letter

                    else:

                        nombre_vie += 1


        SCREEN.blit(image, (image_x, image_y))

        display_word = get_font(50).render(' '.join(Mots_), True, white)

        SCREEN.blit(display_word, (650 - display_word.get_width() // 2, 500))

        afficher_texte("Appuyez sur Echap pour revenir sur l'ecran d'aceuill", 100, 600)
        
        pygame.display.flip()



def Perdu():

    running = True

    while running:

        SCREEN.blit(BG, (0,0))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()

                quit()

            if event.type == pygame.KEYDOWN:

                main_menu()

        afficher_texte("Perdu : Appuiyez sur le du clavier pour revenir au menu", 110, 350)

        pygame.display.update()


def Victoire():

    running = True

    while running:

        SCREEN.blit(BG, (0,0))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()

                quit()


            if event.type == pygame.KEYDOWN:

                main_menu()

        afficher_texte("Victoire : Appuiyez sur le du clavier pour revenir au menu", 100, 350)

        pygame.display.update()





main_menu()





