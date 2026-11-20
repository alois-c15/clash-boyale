from pygame import Vector2, Surface, Color
from dataclasses import dataclass

import pygame

@dataclass(frozen=True)
class Equipe:
    nom: str
    couleur: Color

    def __hash__(self) -> int:
        return hash((self.nom, tuple(self.couleur)))


class Entite:
    OFFSET_VIE: int = 15

    def __init__(self, equipe: Equipe, taille: int, pv_max: int) -> None:
        self.position = Vector2(0, 0)
        self.taille = taille
        self.equipe = equipe

        self.pv_max = pv_max
        self._pv = pv_max

    @property
    def pv(self) -> int:
        return self._pv

    @pv.setter
    def pv(self, valeur: int) -> None:
        self._pv = max(0, min(valeur, self.pv_max))

    def prendre_degats(self, degats: int, origine: "Entite") -> None:
        self.pv -= degats

    def est_vivant(self) -> bool:
        return self.pv > 0

    def distance_to(self, entite: "Entite") -> int:
        distance = self.position.distance_to(entite.position)
        return int(distance - (self.taille // 2 + entite.taille // 2))
    
    def on_entite_ajoutee(self, entite: "Entite") -> None: pass
    def on_entite_retiree(self, entite: "Entite") -> None: pass

    def dessiner(self, surface: Surface) -> None: pass
    def _dessiner_vie(self, surface: Surface) -> None:
        position = self.position + Vector2(0, self.taille // 2 + self.OFFSET_VIE)
        taille_pv = (self.pv / self.pv_max) * self.taille * 2

        bg = pygame.Rect(position.x - self.taille, position.y, self.taille * 2, 5)
        fill = pygame.Rect(bg.left, bg.top, taille_pv, bg.height)

        pygame.draw.rect(surface, "black", bg)
        pygame.draw.rect(surface, self.equipe.couleur, fill)

