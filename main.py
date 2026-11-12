from grille import Grille
from entite import Entite, EQUIPE_1, EQUIPE_2, TAILLE_PETIT, TAILLE_GRAND, entites
from personnages import Personnage
from batiments import Batiment

from pygame import Surface, Color, Vector2
import pygame

pygame.init()
pygame.display.set_caption("Clash Boyale")

screen = pygame.display.set_mode((1280, 720))
clock = pygame.Clock()
is_running = True

grille = Grille(32, 18, 40)

def start():
    tour_equipe_1 = Batiment("TourEquipe1", TAILLE_GRAND, 500, EQUIPE_1)
    tour_equipe_1.position = Vector2(120, 360)

    tour_equipe_2 = Batiment("TourEquipe2", TAILLE_GRAND, 500, EQUIPE_2)
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

        pygame.draw.circle(overlay, couleur, active, TAILLE_PETIT // 2)
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

def on_event(e: pygame.Event):
    global is_running

    if e.type == pygame.QUIT:
        is_running = False
    elif e.type == pygame.MOUSEBUTTONDOWN:
        if not e.button == 1: return
        grille.bouton_souris_actif = True
    elif e.type == pygame.MOUSEBUTTONUP:
        if not e.button == 1: return
        grille.bouton_souris_actif = False

        active = grille.position_case_active()
        equipe = EQUIPE_1 if grille.calculer_cote(int(grille.convertir_position(active).x)) == -1 else EQUIPE_2

        entite = Personnage(f"{equipe}_P{len(entites) + 1}", TAILLE_PETIT, 100, equipe, 75, 15, 15, 1)
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
