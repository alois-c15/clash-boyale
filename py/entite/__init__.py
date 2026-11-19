from pygame import Vector2, Surface, Color
from dataclasses import dataclass

@dataclass
class Equipe:
    nom: str
    couleur: Color


class Entite:
    def __init__(self, equipe: Equipe, taille: int) -> None:
        self.position = Vector2(0, 0)
        self.taille = taille
        self.equipe = equipe
    
    def on_entite_ajoutee(self, entite: "Entite") -> None: pass
    def on_entite_retiree(self, entite: "Entite") -> None: pass

    def dessiner(self, surface: Surface) -> None: pass
