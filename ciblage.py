from pygame import Vector2
from entite import Entite
import entite

def toutes_cibles_potentielles(origine: Entite) -> list[Entite]:
    cibles = []
    for e in entite.entites:
        if e != origine and e.equipe != origine.equipe and e.est_vivant():
            cibles.append(e)
    return cibles

def cible_plus_proche(cibles: list[Entite], position: Vector2) -> Entite | None:
    cible = None
    distance_cible = float("inf")

    for e in cibles:
        distance = position.distance_to(e.position)
        if distance < distance_cible:
            cible = e
            distance_cible = distance

    return cible

def cible_plus_loin(cibles: list[Entite], position: Vector2, distance_max: float = float("inf")) -> Entite | None:
    cible = None
    distance_cible = -1

    for e in cibles:
        distance = position.distance_to(e.position)
        if distance > distance_cible and distance <= distance_max:
            cible = e
            distance_cible = distance

    return cible

def cible_plus_grande(cibles: list[Entite]) -> Entite | None:
    pass

def cible_plus_petite(cibles: list[Entite]) -> Entite | None:
    pass
