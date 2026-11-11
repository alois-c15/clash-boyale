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

    def position_case_active(self) -> Vector2:
        x = self.case_active.x * self.taille_case + self.taille_case // 2
        y = self.case_active.y * self.taille_case + self.taille_case // 2

        return Vector2(x, y)

    def convertir_position(self, position: Vector2) -> Vector2:
        x = position.x // self.taille_case
        y = position.y // self.taille_case

        return Vector2(x, y)

    def calculer_cote(self, x: int) -> int:
        """Retourne -1 si a droite, 0 si au milieu, 1 si a gauche"""
        return (x > (self.largeur - 1) / 2) - (x < (self.largeur - 1) / 2)

    def dessiner(self, surface: Surface) -> None:
        if not self.bouton_souris_actif: return

        overlay = Surface(surface.get_size(), pygame.SRCALPHA)

        for x in range(self.largeur):
            for y in range(self.hauteur):
                cote = self.calculer_cote(x)

                alpha = 75 if x == self.case_active.x and y == self.case_active.y else 25 if (x + y) % 2 == 0 else 20
                couleur = Color(255, 0, 0, alpha) if cote == -1 else Color(255, 255, 255, alpha) if cote == 0 else Color(0, 0, 255, alpha)

                rect = pygame.Rect(x * self.taille_case, y * self.taille_case, self.taille_case, self.taille_case)
                pygame.draw.rect(overlay, couleur, rect)

        surface.blit(overlay)
