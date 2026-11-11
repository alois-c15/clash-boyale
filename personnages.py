from entite import Entite

from pygame import Vector2, Surface
import pygame

import time

class Personnage(Entite):
    def __init__(self, nom: str) -> None:
        super().__init__(nom)

        self.cible: Entite | None = None

        self.debut_attaque = -1
        self.en_train_dattaquer = False

    def update_ia(self, entites: list[Entite], t: float) -> None:
        if not self.cible:
            self._chercher_cible(entites)
            return

        self._attaquer_cible(t)

    def _chercher_cible(self, entites: list[Entite]) -> None:
        cible_plus_proche = None
        distance_plus_proche = float("inf")

        for entite in entites:
            if entite == self: continue

            distance = self.position.distance_to(entite.position)

            if distance < distance_plus_proche:
                cible_plus_proche = entite
                distance_plus_proche = distance

        if cible_plus_proche:
            self.cible = cible_plus_proche

    def _attaquer_cible(self, t: float) -> None:
        if not self.cible: return

        direction = self.cible.position - self.position
        distance = direction.length()

        if distance > 30 + 5: # 15 + 15, self.taille + cible.taille + distance_attaque
            self.position += direction.normalize() * 75 * t
        else:
            if not self.en_train_dattaquer:
                self.en_train_dattaquer = True
                self.debut_attaque = time.time()
                return

            if time.time() - self.debut_attaque < 1:
                return

            print(self.nom, "attaque", self.cible.nom)

            self.en_train_dattaquer = False
            self.debut_attaque = -1

    def dessiner(self, surface: Surface) -> None:
        pygame.draw.circle(surface, "white", self.position, 15)
