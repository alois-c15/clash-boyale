from entite import Entite, EQUIPE_1, EQUIPE_2
import entite

from pygame import Surface, Color, Vector2
import pygame

import ciblage
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

    def update_ia(self, t: float) -> None:
        if not self.cible:
            self._chercher_cible()
            return

        self._attaquer_cible(t)
        self._deplacement(t)

    def on_entite_ajoutee(self, entite: Entite) -> None:
        if not self.cible or entite == self.cible or entite.equipe == self.equipe: return

        distance_cible = self.position.distance_to(self.cible.position)
        distance_entite = self.position.distance_to(entite.position)

        if distance_entite < distance_cible and entite.taille >= self.cible.taille:
            self.cible = entite

    def _deplacement(self, t: float) -> None:
        if not self.cible or self.en_train_dattaquer: return

        direction = self.cible.position - self.position
        distance = direction.length()

        mouvement = Vector2()

        if distance > self.taille // 2 + self.cible.taille // 2 + self.portee // 2:
            mouvement += direction.normalize()

        separation = self._calculer_separation(entite.entites)
        deplacement = direction.normalize() + separation * 2

        if deplacement.length() > 0:
            self.position += deplacement.normalize() * self.vitesse * t

    def _chercher_cible(self) -> None:
        cibles = ciblage.toutes_cibles_potentielles(self)
        self.cible = ciblage.cible_plus_proche(cibles, self.position)

    def _attaquer_cible(self, t: float) -> None:
        if not self.cible:
            self.en_train_dattaquer = False
            return

        distance = self.position.distance_to(self.cible.position)
        portee = self.taille // 2 + self.cible.taille // 2 + self.portee

        if distance > portee:
            self.en_train_dattaquer = False
            self.debut_attaque = -1
            return

        if not self.en_train_dattaquer:
            self.en_train_dattaquer = True
            self.debut_attaque = time.time()
            return

        if time.time() - self.debut_attaque < self.duree_attaque:
            return

        if not self.cible.est_vivant():
            self.cible = None
            self.en_train_dattaquer = False
            self.debut_attaque = -1
            return

        if distance > portee:
            self.en_train_dattaquer = False
            return

        self.cible.prendre_degats(self, self.degats)
        print(f"pv {self.cible.nom}: {self.cible.pv}/{self.cible.pv_max}")

        if not self.cible.est_vivant():
            self.cible = None

        self.debut_attaque = time.time()

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
            return

        if self.cible == origine: return

        distance_origine = self.position.distance_to(origine.position) - origine.taille
        distance_cible = self.position.distance_to(self.cible.position) - self.cible.taille

        if origine.taille > self.cible.taille:
            if distance_origine <= self.portee:
                self.cible = origine
                return

        if distance_cible >= distance_origine and origine.taille <= self.cible.taille:
            self.cible = origine

    def dessiner(self, surface: Surface) -> None:
        super().dessiner(surface)

        couleur = Color(255, 0, 0) if self.equipe == EQUIPE_1 else Color(0, 0, 255)
        pygame.draw.circle(surface, couleur, self.position, self.taille // 2)
