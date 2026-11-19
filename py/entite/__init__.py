from pygame import Vector2, Surface, Color
from dataclasses import dataclass

@dataclass
class Equipe:
    nom: str
    couleur: Color


class Entite:
    def __init__(self, equipe: Equipe, taille: int, pv_max: int) -> None:
        self.position = Vector2(0, 0)
        self.taille = taille
        self.equipe = equipe

    def distance_to(self, entite: "Entite") -> int:
        distance = self.position.distance_to(entite.position)
        return int(distance - (self.taille // 2 + entite.taille // 2))
    
    def on_entite_ajoutee(self, entite: "Entite") -> None: pass
    def on_entite_retiree(self, entite: "Entite") -> None: pass

    def dessiner(self, surface: Surface) -> None: pass
