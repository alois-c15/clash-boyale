from grille import Grille, HAUT, BAS, GAUCHE, DROITE, TAILLE_PETIT, TAILLE_GRAND
from entite import Entite, Equipe
from entite.emplacement import Emplacement
from entite.unite import Unite

import pygame

pygame.init()
pygame.display.set_caption("Clash Boyale")

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
is_running = True

EQUIPE_1 = Equipe("Equipe 1", pygame.Color(255, 0, 0))
EQUIPE_2 = Equipe("Equipe 2", pygame.Color(0, 0, 255))

grille = Grille()
entites: list[Entite] = []

tour_equipe_1: Emplacement | None = None
tour_equipe_2: Emplacement | None = None

def ajouter_entite(entite: Entite):
    global entites

    for e in entites:
        e.on_entite_ajoutee(entite)

    entites.append(entite)

def retirer_entite(entite: Entite):
    global entites

    entites.remove(entite)
    for e in entites:
        e.on_entite_retiree(entite)

def start():
    global tour_equipe_1, tour_equipe_2

    tour_equipe_1 = Emplacement(equipe=EQUIPE_1, taille=TAILLE_GRAND + 5, pv_max=700)
    tour_equipe_1.position = pygame.Vector2(80 + TAILLE_GRAND // 2, 360)

    tour_equipe_2 = Emplacement(equipe=EQUIPE_2, taille=TAILLE_GRAND + 5, pv_max=700)
    tour_equipe_2.position = pygame.Vector2(1200 - TAILLE_GRAND // 2, 360)

    ajouter_entite(tour_equipe_1)
    ajouter_entite(tour_equipe_2)

    unite_1 = Unite(equipe=EQUIPE_1, taille=TAILLE_PETIT, pv_max=100, vitesse=85, degats=25, portee=15, duree_attaque=1.35)
    unite_1.position = pygame.Vector2(400, 360)

    unite_2 = Unite(equipe=EQUIPE_2, taille=TAILLE_PETIT, pv_max=100, vitesse=85, degats=25, portee=15, duree_attaque=1.35)
    unite_2.position = pygame.Vector2(880, 360)

    ajouter_entite(unite_1)
    ajouter_entite(unite_2)


def update(t: float):
    grille.dessiner(screen)
    for entite in entites:
        if not entite.est_vivant():
            retirer_entite(entite)
            
            del entite
            continue

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