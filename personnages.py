from entite import Entite, EQUIPE_1, EQUIPE_2

from pygame import Surface, Color, Vector2
import pygame

import time

import entite

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
        self._deplacement(entites, t)

    def _deplacement(self, entites: list[Entite], t: float) -> None:
        if not self.cible or self.en_train_dattaquer: return

        direction = self.cible.position - self.position
        distance = direction.length()

        mouvement = Vector2()

        if distance > self.taille // 2 + self.cible.taille // 2 + self.portee:
            mouvement += direction.normalize()

        separation = self._calculer_separation(entites)
        deplacement = direction.normalize() + separation * 2

        if deplacement.length() > 0:
            self.position += deplacement.normalize() * self.vitesse * t

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

        if distance <= self.taille // 2 + self.cible.taille // 2 + self.portee:
            if not self.en_train_dattaquer:
                self.en_train_dattaquer = True
                self.debut_attaque = time.time()

        if not self.en_train_dattaquer: return

        if time.time() - self.debut_attaque < self.duree_attaque:
            return

        distance = self.position.distance_to(self.cible.position)
        if distance > self.taille // 2 + self.cible.taille // 2 + self.portee:
            self.en_train_dattaquer = False
            return

        if not self.cible.est_vivant():
            self.cible = None
            self.en_train_dattaquer = False
            return

        self.cible.prendre_degats(self, self.degats)
        print(f"pv {self.cible.nom}: {self.cible.pv}/{self.cible.pv_max}")

        if not self.cible.est_vivant():
            self.cible = None

        self.en_train_dattaquer = False
        self.debut_attaque = -1

    def _calculer_separation(self, entites: list[Entite]) -> Vector2:
        force = Vector2()
        voisins = 0

        for entite in entites:
            if entite == self: continue
            distance_min = ((self.taille + entite.taille) / 2 + self.portee) * 2

            direction = self.position - entite.position
            distance = direction.length()

            if distance == 0 or distance >= distance_min: continue

            force += direction.normalize() / distance
            voisins += 1

        if voisins > 0:
            force /= voisins

        return force


    def prendre_degats(self, origine: "Entite", degats: int) -> None:
        super().prendre_degats(origine, degats)

        if not self.cible:
            self.cible = origine

        if self.cible == origine: return

        distance_origine = self.position.distance_to(origine.position)
        distance_cible = self.position.distance_to(self.cible.position)

        if distance_origine <= distance_cible and not self.cible.taille > origine.taille:
            self.cible = origine

    def dessiner(self, surface: Surface) -> None:
        couleur = Color(255, 0, 0) if self.equipe == EQUIPE_1 else Color(0, 0, 255)
        pygame.draw.circle(surface, couleur, self.position, self.taille // 2)
