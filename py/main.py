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
    unite = Unite(EQUIPE_1, 35, 45)
    unite.position = pygame.Vector2(273, 173)

    entites.append(unite)


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