from pygame import Vector2, Surface

EQUIPE_1: int = 1
EQUIPE_2: int = 2

class Entite:
    position: Vector2

    def __init__(self, nom: str, taille: int, pv_max: int, equipe: int) -> None:
        self.nom = nom
        self.taille = taille

        self.equipe = equipe

        self.position = Vector2()

        self._pv = pv_max
        self._pv_max = pv_max

    @property
    def pv_max(self) -> int:
        return self._pv_max

    @property
    def pv(self) -> int:
        return self._pv

    @pv.setter
    def pv(self, valeur: int) -> None:
        self._pv = max(0, min(valeur, self.pv_max))

    def est_vivant(self) -> bool:
        return self.pv > 0

    def dessiner(self, surface: Surface) -> None:
        pass
