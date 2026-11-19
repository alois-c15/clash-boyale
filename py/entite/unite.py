from entite import Entite, Equipe
from pygame import Surface

import pygame

class Unite(Entite):
    def __init__(self, equipe: Equipe, taille: int, pv_max: int, vitesse: int, degats: int, portee: int, duree_attaque: float) -> None:
        super().__init__(equipe, taille, pv_max)
        self.vitesse = vitesse

        self.degats = degats
        self.portee = portee
        self.duree_attaque = duree_attaque

        self.cible: Entite | None = None

    def update_ciblage(self, entites: list[Entite]) -> None:
        cible_min = None
        distance_min = float("inf")

        for entite in entites:
            if entite == self or entite.equipe == self.equipe:
                continue

            distance = self.distance_to(entite)
            if distance < distance_min:
                cible_min = entite
                distance_min = distance

        if cible_min:
            self.cible = cible_min
            print(self.cible)
            

    def update_attaque(self, t: float) -> None:
        if not self.cible: return

        distance = self.distance_to(self.cible)
        if distance > self.portee // 1.5:
            direction = self.cible.position - self.position
            self.position += direction.normalize() * self.vitesse * t
        else:
            pass

    def dessiner(self, surface: Surface) -> None:
        pygame.draw.circle(surface, self.equipe.couleur, self.position, self.taille // 2)