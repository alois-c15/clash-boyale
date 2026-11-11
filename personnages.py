from entite import Entite

from pygame import Vector2, Surface
import pygame

class Personnage(Entite):
    def __init__(self, nom: str) -> None:
        super().__init__(nom)

    def dessiner(self, surface: Surface) -> None:
        pygame.draw.circle(surface, "white", self.position, 35)
