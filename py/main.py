from entite import Entite, Equipe
from entite.unite import Unite

import pygame

pygame.init()
pygame.display.set_caption("Clash Boyale")

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
is_running = True

EQUIPE_1 = Equipe("Equipe 1", pygame.Color(255, 0, 0))
EQUIPE_2 = Equipe("Equipe 2", pygame.Color(0, 0, 255))

entites: list[Entite] = []


def start():
    unite_1 = Unite(equipe=EQUIPE_1, taille=35, pv_max=100, vitesse=85, degats=25, portee=15, duree_attaque=1.35)
    unite_1.position = pygame.Vector2(400, 360)

    unite_2 = Unite(equipe=EQUIPE_2, taille=35, pv_max=100, vitesse=85, degats=25, portee=15, duree_attaque=1.35)
    unite_2.position = pygame.Vector2(880, 360)

    entites.append(unite_1)
    entites.append(unite_2)


def update(t: float):
    for entite in entites:
        if isinstance(entite, Unite):
            update_unite(entite, t)

        entite.dessiner(screen)


def update_unite(unite: Unite, t: float):
    if not unite.cible:
        unite.update_ciblage(entites)
        return
    unite.update_attaque(t)


def on_event(e: pygame.event.Event):
    global is_running

    if e.type == pygame.QUIT:
        is_running = False

start()
while is_running:
    for e in pygame.event.get():
        on_event(e)

    t = clock.tick(60) / 1000
    screen.fill("black")

    update(t)
    pygame.display.flip()

pygame.quit()