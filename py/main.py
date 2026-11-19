import pygame

pygame.init()
pygame.display.set_caption("Clash Boyale")

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
is_running = True


def start():
    pass

def update(t: float):
    pass

def on_event(e: pygame.event.Event):
    global is_running

    if e.type == pygame.QUIT:
        is_running = False

while is_running:
    for e in pygame.event.get():
        on_event(e)

    t = clock.tick(60) / 1000
    screen.fill("black")

    update(t)
    pygame.display.flip()

pygame.quit()