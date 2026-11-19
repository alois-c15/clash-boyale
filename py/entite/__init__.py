from pygame import Vector2, Surface

class Entite:
    def __init__(self, taille: int) -> None:
        self.position = Vector2(0, 0)
        self.taille = taille
    
    def on_entite_ajoutee(self, entite: "Entite") -> None: pass
    def on_entite_retiree(self, entite: "Entite") -> None: pass

    def dessiner(self, surface: Surface) -> None: pass
