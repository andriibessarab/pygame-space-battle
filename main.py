import pygame
import os

WIDTH, HEIGHT = 900, 500  # W & H of app
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Battle")

FPS = 60
VEL = 5

BACKGROUND_COLOR = (255, 255, 255)
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

SPACESHIP_YELLOW = pygame.transform.rotate(
    pygame.transform.scale(
        pygame.image.load(os.path.join("assets", "spaceship_yellow.png")),  # Path to IMG
        (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)  # Width & Height of img
    ),
    270  # Rotation angle
)
SPACESHIP_RED = pygame.transform.rotate(
    pygame.transform.scale(
        pygame.image.load(os.path.join("assets", "spaceship_red.png")),  # Path to IMG
        (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)  # Width & Height of img
    ),
    90  # Rotation angle
)


# Draw window
def draw_window(yellow, red):
    WIN.fill(BACKGROUND_COLOR)
    WIN.blit(SPACESHIP_YELLOW, (yellow.x, yellow.y))
    WIN.blit(SPACESHIP_RED, (red.x, red.y))
    pygame.display.update()


# Movement for left handle(yellow ship)
def movement_handle_left(keys_pressed, yellow):
    if keys_pressed[pygame.K_a]:  # Left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d]:  # Right
        yellow.x += VEL
    if keys_pressed[pygame.K_w]:  # Up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s]:  # Down
        yellow.y += VEL


# Movement for left handle(yellow ship)
def movement_handle_right(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT]:  # Left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT]:  # Right
        red.x += VEL
    if keys_pressed[pygame.K_UP]:  # Up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN]:  # Down
        red.y += VEL

# Main
def main():
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    clock = pygame.time.Clock()
    run = True  # When false, game terminates
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()

        # Handle movement
        movement_handle_left(keys_pressed, yellow)
        movement_handle_right(keys_pressed, red)

        draw_window(yellow, red)

    pygame.quit()


if __name__ == '__main__':
    main()
