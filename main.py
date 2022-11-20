import pygame
import os

# Window params
WIDTH, HEIGHT = 900, 500  # W & H of app
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Battle")

# Global Game Settings
FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 4

# Colors
BACKGROUND_COLOR = (255, 255, 255)
BORDER_COLOR = (0, 0, 0)
YELLOW_SIDE_COLOR = (255, 253, 84)
RED_SIDE_COLOR = (234, 51, 49)

# Images
IMG_SPACESHIP_YELLOW = pygame.image.load(os.path.join("assets", "spaceship_yellow.png"))
IMG_SPACESHIP_RED = pygame.image.load(os.path.join("assets", "spaceship_red.png"))
IMG_SPACE = pygame.image.load(os.path.join("assets", "background.png"))

# Custom events
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

# Objects
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)
BACKGROUND = pygame.transform.scale(
    IMG_SPACE,
    (WIDTH, HEIGHT)
)
SPACESHIP_YELLOW = pygame.transform.rotate(
    pygame.transform.scale(
       IMG_SPACESHIP_YELLOW,  # Path to IMG
        (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)  # Width & Height of img
    ),
    90  # Rotation angle
)
SPACESHIP_RED = pygame.transform.rotate(
    pygame.transform.scale(
        IMG_SPACESHIP_RED,  # Path to IMG
        (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)  # Width & Height of img
    ),
    270  # Rotation angle
)


# Draw window
def draw_window(yellow, red, yellow_bullets, red_bullets):
    WIN.blit(BACKGROUND, (0, 0))
    pygame.draw.rect(WIN, BORDER_COLOR, BORDER)
    WIN.blit(SPACESHIP_YELLOW, (yellow.x, yellow.y))
    WIN.blit(SPACESHIP_RED, (red.x, red.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW_SIDE_COLOR, bullet)

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED_SIDE_COLOR, bullet)

    pygame.display.update()


# Movement for left handle(yellow ship)
def movement_handle_left(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # Left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # Right
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # Up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - yellow.height / 2:  # Down
        yellow.y += VEL


# Movement for right handle(red ship)
def movement_handle_right(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # Left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # Right
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # Up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - red.height / 2:  # Down
        red.y += VEL


# Handle Bullets
def bullets_handle(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        if bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        if bullet.x < 0:
            red_bullets.remove(bullet)


# Main
def main():
    # Game objects
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red_bullets = []
    yellow_bullets = []

    clock = pygame.time.Clock()
    run = True  # When false, game terminates
    while run:
        clock.tick(FPS)  # Set FPS

        # Handle events
        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and MAX_BULLETS >= len(yellow_bullets):
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                if event.key == pygame.K_SLASH and MAX_BULLETS >= len(red_bullets):
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)

        keys_pressed = pygame.key.get_pressed()  # Get all pressed keys

        # Handle movement
        movement_handle_left(keys_pressed, yellow)
        movement_handle_right(keys_pressed, red)

        # Handle bullets
        bullets_handle(yellow_bullets, red_bullets, yellow, red)

        draw_window(yellow, red, yellow_bullets, red_bullets)  # Draw window

    pygame.quit()


if __name__ == '__main__':
    main()
