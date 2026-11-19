from pygame import Surface, Color

import pygame

def get_couleur(x: int, y: int) -> Color:
    if (x + y) % 2 == 0:
        return Color(0, 245, 0)
    return Color(0, 230, 0)

class Grille:
    LARGEUR: int = 32
    HAUTEUR: int = 18

    TAILLE_CASE: int = 40

    def __init__(self) -> None:
        pass

    def dessiner(self, surface: Surface) -> None:
        for x in range(self.LARGEUR):
            for y in range(self.HAUTEUR):
                couleur = get_couleur(x, y)

                taille = self.TAILLE_CASE
                rect = pygame.Rect(x * taille, y * taille, taille, taille)

                pygame.draw.rect(surface, couleur, rect)