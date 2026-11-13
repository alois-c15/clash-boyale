from grille import Grille
from entite import Entite, EQUIPE_1, EQUIPE_2, TAILLE_PETIT, TAILLE_GRAND, entites
from personnages import Personnage
from batiments import Batiment

from pygame import Surface, Color, Vector2
import pygame

import personnages

pygame.init()
pygame.display.set_caption("Clash Boyale")

screen = pygame.display.set_mode((1280, 720))
clock = pygame.Clock()
is_running = True

font = pygame.font.SysFont(None, 26)

grille = Grille(32, 18, 40)
perso_select = 0

def selection_personnage_up():
    global perso_select

    perso_select += 1
    if perso_select > len(personnages.LISTE) - 1:
        perso_select = 0

    print(personnages.LISTE[perso_select][0])

def selection_personnage_down():
    global perso_select

    perso_select -= 1
    if perso_select < 0:
        perso_select = len(personnages.LISTE) - 1

    print(personnages.LISTE[perso_select][0])

def start():
    tour_equipe_1 = Batiment("TourEquipe1", TAILLE_GRAND, 700, EQUIPE_1)
    tour_equipe_1.position = Vector2(120, 360)

    tour_equipe_2 = Batiment("TourEquipe2", TAILLE_GRAND, 700, EQUIPE_2)
    tour_equipe_2.position = Vector2(1160, 360)

    entites.append(tour_equipe_1)
    entites.append(tour_equipe_2)

def update(t: float):
    grille.update()
    grille.dessiner_sol(screen)

    if grille.bouton_souris_actif:
        active = grille.position_case_active()

        overlay = Surface(screen.get_size(), pygame.SRCALPHA)
        couleur = Color(255, 255, 255, 170)

        select = personnages.LISTE[perso_select]
        if not select: return

        pygame.draw.circle(overlay, couleur, active, select[1] // 2)
        screen.blit(overlay)

    grille.dessiner_overlay(screen)

    for entite in entites:
        if isinstance(entite, Personnage):
            entite.update_ia(t)

        entite.dessiner(screen)

    for entite in entites:
        if not entite.est_vivant():
            print(entite.nom, "est mort")

            entites.remove(entite)
            del entite

    pos = pygame.mouse.get_pos()

    perso_texte = font.render(str(personnages.LISTE[perso_select][0]), True, Color(255, 255, 255))
    screen.blit(perso_texte, (pos[0] + 5, pos[1] + 15))

def on_event(e: pygame.Event):
    global is_running

    if e.type == pygame.QUIT:
        is_running = False
    elif e.type == pygame.MOUSEBUTTONDOWN:
        if not e.button == 1: return
        grille.bouton_souris_actif = True
    elif e.type == pygame.KEYDOWN:
        if e.key == pygame.K_e:
            selection_personnage_up()
        elif e.key == pygame.K_a:
            selection_personnage_down()
    elif e.type == pygame.MOUSEBUTTONUP:
        if not e.button == 1: return
        grille.bouton_souris_actif = False

        active = grille.position_case_active()
        equipe = EQUIPE_1 if grille.calculer_cote(int(grille.convertir_position(active).x)) == -1 else EQUIPE_2

        stats = personnages.LISTE[perso_select]
        print(stats)

        entite = Personnage(f"{equipe}_{stats[0]}{len(entites) + 1}", stats[1], stats[2], equipe, stats[3], stats[4], stats[5], stats[6])
        entite.position = active

        for entite_l in entites:
            entite_l.on_entite_ajoutee(entite)

        entites.append(entite)

start()
while is_running:
    for e in pygame.event.get():
        on_event(e)

    t = clock.tick(60) / 1000

    screen.fill("black")
    update(t)

    pygame.display.flip()

pygame.quit()
