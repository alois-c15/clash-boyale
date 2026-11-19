from pygame import Surface
from entite import Entite

import pygame

class Unite(Entite):
    def __init__(self, taille: int, vitesse: int) -> None:
        super().__init__(taille)
        self.vitesse = vitesse

        self.cible: Entite | None = None

    def update_ciblage(self, entites: list[Entite]) -> None:
        pass

    def update_attaque(self, t: float) -> None:
        pass

    def dessiner(self, surface: Surface) -> None:
        pygame.draw.circle(surface, "white", self.position, self.taille // 2)