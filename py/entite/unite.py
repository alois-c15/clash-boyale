from entite import Entite, Equipe
from pygame import Surface

import pygame
import time

class Unite(Entite):
    def __init__(self, equipe: Equipe, taille: int, pv_max: int, vitesse: int, degats: int, portee: int, duree_attaque: float) -> None:
        super().__init__(equipe, taille, pv_max)
        self.vitesse = vitesse

        self.degats = degats
        self.portee = portee
        self.duree_attaque = duree_attaque

        self.cible: Entite | None = None
        self.en_attaque = False
        self.debut_attaque = 0

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
            

    def update_attaque(self, t: float) -> None:
        if not self.cible: return

        distance = self.distance_to(self.cible)
        if distance > self.portee // 1.5:
            direction = self.cible.position - self.position
            self.position += direction.normalize() * self.vitesse * t
        else:
            now = time.time()
            if not self.en_attaque:
                self.en_attaque = True
                self.debut_attaque = now
                return

            if (now - self.debut_attaque < self.duree_attaque
                or not self.cible
                or self.distance_to(self.cible) > self.portee):
                return

            self.cible.prendre_degats(self.degats)
            self.en_attaque = False

    def dessiner(self, surface: Surface) -> None:
        self._dessiner_vie(surface)
        pygame.draw.circle(surface, self.equipe.couleur, self.position, self.taille // 2)

