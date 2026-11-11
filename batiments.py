from entite import Entite, EQUIPE_1, EQUIPE_2

from pygame import Vector2, Surface, Color
import pygame

class Batiment(Entite):
    def __init__(self, nom: str, taille: int, pv_max: int, equipe: int) -> None:
        super().__init__(nom, taille, pv_max, equipe)

    def dessiner(self, surface: Surface) -> None:
        rect = pygame.Rect(self.position.x - self.taille // 2, self.position.y - self.taille // 2, self.taille, self.taille)
        couleur = Color(255, 0, 0) if self.equipe == EQUIPE_1 else Color(0, 0, 255)

        pygame.draw.rect(surface, couleur, rect)
