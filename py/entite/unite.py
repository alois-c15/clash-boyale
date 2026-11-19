from entite import Entite, Equipe
from pygame import Surface

import pygame

class Unite(Entite):
    def __init__(self, equipe: Equipe, taille: int, vitesse: int) -> None:
        super().__init__(equipe, taille)
        self.vitesse = vitesse

        self.cible: Entite | None = None

    def update_ciblage(self, entites: list[Entite]) -> None:
        pass

    def update_attaque(self, t: float) -> None:
        pass

    def dessiner(self, surface: Surface) -> None:
        pygame.draw.circle(surface, self.equipe.couleur, self.position, self.taille // 2)