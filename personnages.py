from entite import Entite, EQUIPE_1, EQUIPE_2

from pygame import Vector2, Surface, Color
import pygame

import time

class Personnage(Entite):
    def __init__(self, nom: str, taille: int, pv_max: int, equipe: int, vitesse: int, degats: int, portee: int, duree_attaque: float) -> None:
        super().__init__(nom, taille, pv_max, equipe)

        self.vitesse = vitesse

        self.degats = degats
        self.portee = portee
        self.duree_attaque = duree_attaque

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
            if entite == self or entite.equipe == self.equipe: continue

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

        if distance > self.taille + self.cible.taille + self.portee:
            self.position += direction.normalize() * self.vitesse * t
        else:
            if not self.en_train_dattaquer:
                self.en_train_dattaquer = True
                self.debut_attaque = time.time()
                return

            if time.time() - self.debut_attaque < self.duree_attaque:
                return

            self.cible.pv -= self.degats
            print(f"pv {self.cible.nom}: {self.cible.pv}/{self.cible.pv_max}")

            if not self.cible.est_vivant():
                self.cible = None

            self.en_train_dattaquer = False
            self.debut_attaque = -1

    def dessiner(self, surface: Surface) -> None:
        couleur = Color(255, 0, 0) if self.equipe == EQUIPE_1 else Color(0, 0, 255)
        pygame.draw.circle(surface, couleur, self.position, self.taille)
