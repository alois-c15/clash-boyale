from grille import Grille
from entite import Entite
from personnages import Personnage

import pygame

pygame.init()
pygame.display.set_caption("Clash Boyale")

screen = pygame.display.set_mode((1280, 720))
clock = pygame.Clock()
is_running = True

grille = Grille(32, 18, 40)
entites: list[Entite] = []

def start():
    pass

def update(t: float):
    grille.update()

    if grille.bouton_souris_actif:
        active = grille.position_case_active()
        pygame.draw.circle(screen, "grey", active, 15)

    grille.dessiner(screen)

    for entite in entites:
        entite.dessiner(screen)

def on_event(e: pygame.Event):
    global is_running

    if e.type == pygame.QUIT:
        is_running = False
    elif e.type == pygame.MOUSEBUTTONDOWN:
        grille.bouton_souris_actif = True
    elif e.type == pygame.MOUSEBUTTONUP:
        grille.bouton_souris_actif = False

        active = grille.position_case_active()

        entite = Personnage("Test")
        entite.position = active

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
