from pygame import Vector2, Surface, Color
from entite import Equipe

import pygame

HAUT: int = 0
BAS: int = 1
GAUCHE: int = 2
DROITE: int = 3

def get_couleur(x: int, y: int) -> Color:
    if (x + y) % 2 == 0:
        return Color(0, 245, 0)
    return Color(0, 230, 0)


class Grille:
    LARGEUR: int = 32
    HAUTEUR: int = 18

    TAILLE_CASE: int = 40

    def __init__(self, equipe_1: Equipe, equipe_2: Equipe) -> None:
        self.case_active = Vector2(-1, -1)
        self.boutton_souris_actif = False

        self.equipe_1 = equipe_1
        self.equipe_2 = equipe_2

    def update(self) -> None:
        if not self.boutton_souris_actif: return

        souris = pygame.mouse.get_pos()

        self.case_active.x = souris[0] // self.TAILLE_CASE
        self.case_active.y = souris[1] // self.TAILLE_CASE

    def get_cote(self, x: int) -> int:
        if x < self.LARGEUR // 2:
            return -1
        return 1

    def dessiner(self, surface: Surface) -> None:
        overlay = Surface(surface.get_size(), pygame.SRCALPHA)

        for x in range(self.LARGEUR):
            for y in range(self.HAUTEUR):
                couleur = get_couleur(x, y)

                taille = self.TAILLE_CASE
                rect = pygame.Rect(x * taille, y * taille, taille, taille)
                pygame.draw.rect(surface, couleur, rect)

                if self.boutton_souris_actif:
                    cote = self.get_cote(x)

                    equipe = self.equipe_1 if cote == -1 else self.equipe_2
                    alpha = 170 if (x == self.case_active.x and y == self.case_active.y) else 100

                    pygame.draw.rect(overlay, Color(equipe.couleur.r, equipe.couleur.g, equipe.couleur.b, alpha), rect)

        surface.blit(overlay, (0, 0))
                    


TAILLE_PETIT: int = Grille.TAILLE_CASE * 1
TAILLE_MOYEN: int = Grille.TAILLE_CASE * 2
TAILLE_GRAND: int = Grille.TAILLE_CASE * 3