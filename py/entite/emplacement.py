from entite import Entite, Equipe
from pygame import Surface

import pygame

class Emplacement(Entite):
    def __init__(self, equipe: Equipe, taille: int, pv_max: int) -> None:
        super().__init__(equipe, taille, pv_max)

    def dessiner(self, surface: Surface) -> None:
        self._dessiner_vie(surface)

        rect = pygame.Rect(self.position.x - self.taille // 2, self.position.y - self.taille // 2, self.taille, self.taille)
        pygame.draw.rect(surface, self.equipe.couleur, rect)