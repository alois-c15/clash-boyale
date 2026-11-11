from pygame import Vector2, Surface, Color
import pygame

class Grille:
    def __init__(self, largeur: int, hauteur: int, taille_case: int) -> None:
        self.largeur = largeur
        self.hauteur = hauteur

        self.taille_case = taille_case

        self.bouton_souris_actif = False
        self.case_active = Vector2(-1, -1)

    def update(self) -> None:
        if not self.bouton_souris_actif: return

        pos_souris = pygame.mouse.get_pos()

        self.case_active.x = pos_souris[0] // self.taille_case
        self.case_active.y = pos_souris[1] // self.taille_case

    def dessiner(self, surface: Surface) -> None:
        if not self.bouton_souris_actif: return

        overlay = Surface(surface.get_size(), pygame.SRCALPHA)

        for x in range(self.largeur):
            for y in range(self.hauteur):
                alpha = 65 if x == self.case_active.x and y == self.case_active.y else 20 if (x + y) % 2 == 0 else 15
                couleur = Color(255, 255, 255,  alpha)

                rect = pygame.Rect(x * self.taille_case, y * self.taille_case, self.taille_case, self.taille_case)
                pygame.draw.rect(overlay, couleur, rect)

        surface.blit(overlay)
