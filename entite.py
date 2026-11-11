from pygame import Vector2, Surface
import pygame

class Entite:
    position: Vector2

    def __init__(self, nom: str) -> None:
        self.nom = nom
        self.position = Vector2()

    def dessiner(self, surface: Surface) -> None:
        pass
