import pygame
import os

WIDTH, HEIGHT = 900, 500  # W & H of app
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Battle")

FPS = 60

BACKGROUND_COLOR = (255, 255, 255)
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

SPACESHIP_YELLOW = pygame.transform.rotate(
    pygame.transform.scale(
        pygame.image.load(os.path.join("assets", "spaceship_yellow.png")),  # Path to IMG
        (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)  # Width & Height of img
    ),
    90  # Rotation angle
)
SPACESHIP_RED = pygame.transform.rotate(
    pygame.transform.scale(
        pygame.image.load(os.path.join("assets", "spaceship_red.png")),  # Path to IMG
        (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)  # Width & Height of img
    ),
    270  # Rotation angle
)


def draw_window():
    WIN.fill(BACKGROUND_COLOR)
    WIN.blit(SPACESHIP_YELLOW, (300, 100))
    WIN.blit(SPACESHIP_RED, (700, 100))
    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    run = True  # When false, game terminates
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                run = False

        draw_window()

    pygame.quit()


if __name__ == '__main__':
    main()
