from grille import Grille
from entite import Entite, EQUIPE_1, EQUIPE_2
from personnages import Personnage

from pygame import Surface, Color
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

        overlay = Surface(screen.get_size(), pygame.SRCALPHA)
        couleur = Color(255, 255, 255, 170)

        pygame.draw.circle(overlay, couleur, active, 15)
        screen.blit(overlay)

    grille.dessiner(screen)

    for entite in entites:
        if isinstance(entite, Personnage):
            entite.update_ia(entites, t)

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
        grille.bouton_souris_actif = True
    elif e.type == pygame.MOUSEBUTTONUP:
        grille.bouton_souris_actif = False

        active = grille.position_case_active()
        x = int(grille.convertir_position(active).x)

        equipe = EQUIPE_1 if grille.calculer_cote(int(grille.convertir_position(active).x)) == -1 else EQUIPE_2

        entite = Personnage(f"P{len(entites) + 1}", 15, 100, equipe, 75, 15, 5, 1)
        entite.position = active

        print(entite.nom, ":", equipe)

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
