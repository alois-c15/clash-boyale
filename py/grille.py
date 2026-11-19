from pygame import Vector2, Surface, Color
from entite import Equipe

import pygame

HAUT: int = 0
BAS: int = 1
GAUCHE: int = 2
DROITE: int = 3

def get_couleur(x: int, y: int) -> Color:
    if (x + y) % 2 == 0:
        return Color(0, 245, 0)
    return Color(0, 230, 0)


class Curseur:
    def __init__(self, equipe: Equipe, cote: int) -> None:
        self.equipe = equipe
        self.cote = cote

        self._position = Vector2(0, 0)

    @property
    def position(self) -> Vector2:
        return self._position

    @position.setter
    def position(self, nouveau: Vector2) -> None:
        self._position.x = int(nouveau.x)
        self._position.y = int(nouveau.y)


class Grille:
    LARGEUR: int = 32
    HAUTEUR: int = 18

    TAILLE_CASE: int = 40

    def __init__(self) -> None:
        self._curseurs: dict[Equipe, Curseur] = {}

    def creer_curseur(self, equipe: Equipe, cote: int, position: Vector2 | None = None):
        if equipe in self._curseurs: return

        curseur = Curseur(equipe, cote)
        if position:
            curseur.position = position

        self._curseurs[equipe] = curseur

    def deplacer_curseur(self, equipe: Equipe, direction: int) -> None:
        curseur = self._curseurs.get(equipe)
        if not curseur: return

        if direction == HAUT:
            curseur.position.y -= 1
            if curseur.position.y < 0:
                curseur.position.y = 0
        elif direction == BAS:
            curseur.position.y += 1
            if curseur.position.y > self.HAUTEUR - 1:
                curseur.position.y = self.HAUTEUR - 1
        elif direction == GAUCHE:
            curseur.position.x -= 1
            if curseur.cote == GAUCHE:
                if curseur.position.x < 0:
                    curseur.position.x = 0
            else:
                if curseur.position.x < self.LARGEUR // 2:
                    curseur.position.x = self.LARGEUR // 2
        elif direction == DROITE:
            curseur.position.x += 1
            if curseur.cote == GAUCHE:
                if curseur.position.x > self.LARGEUR // 2 - 1:
                    curseur.position.x = self.LARGEUR // 2 - 1
            else:
                if curseur.position.x > self.LARGEUR - 1:
                    curseur.position.x = self.LARGEUR - 1


    def grille_to_global(self, position_grille: Vector2) -> Vector2:
        position_globale = Vector2()
        position_globale.x = position_grille.x * self.TAILLE_CASE + self.TAILLE_CASE // 2
        position_globale.y = position_grille.y * self.TAILLE_CASE + self.TAILLE_CASE // 2

        return position_globale

    def dessiner(self, surface: Surface) -> None:
        for x in range(self.LARGEUR):
            for y in range(self.HAUTEUR):
                couleur = get_couleur(x, y)

                taille = self.TAILLE_CASE
                rect = pygame.Rect(x * taille, y * taille, taille, taille)

                pygame.draw.rect(surface, couleur, rect)

        overlay = Surface(surface.get_size(), pygame.SRCALPHA)
        for curseur in self._curseurs.values():
            position = self.grille_to_global(curseur.position)
            rect = pygame.Rect(position.x - self.TAILLE_CASE // 2, position.y - self.TAILLE_CASE // 2, self.TAILLE_CASE, self.TAILLE_CASE)

            c = curseur.equipe.couleur
            couleur = Color(min(c.r + 75, 255), min(c.g + 75, 255), min(c.b + 75, 255), 170)

            pygame.draw.rect(overlay, couleur, rect)

        surface.blit(overlay, (0, 0))
