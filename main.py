import pygame
import os
import random

pygame.font.init()
pygame.mixer.init()

# Window params
WIDTH, HEIGHT = 1280, 1024  # W & H of app
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Battle")

# Global Game Settings
FPS = 60
VEL = 7
BULLET_VEL = 12
MAX_BULLETS = 4

# Sounds
SOUND_BG_GAME = pygame.mixer.Sound(os.path.join("assets", "game_bg_soundtrack.mp3"))
SOUND_BULLET_HIT = pygame.mixer.Sound(os.path.join("assets", "bullet_fire_sound.mp3"))
SOUND_BULLET_FIRE = pygame.mixer.Sound(os.path.join("assets", "bullet_hit_sound.mp3"))

# Sounds volume
SOUND_BG_GAME.set_volume(0.1)
SOUND_BULLET_HIT.set_volume(0.2)
SOUND_BULLET_FIRE.set_volume(0.2)

# Fonts
FONT_HEALTH = pygame.font.SysFont("comicsans", 25)
FONT_WINNER = pygame.font.SysFont("comicsans", 100)

# Colors
BACKGROUND_COLOR = (255, 255, 255)
BORDER_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
YELLOW_SIDE_COLOR = (255, 253, 84)
RED_SIDE_COLOR = (234, 51, 49)

# Images
IMG_SPACESHIP_YELLOW = pygame.image.load(os.path.join("assets", "spaceship_yellow.png"))
IMG_SPACESHIP_RED = pygame.image.load(os.path.join("assets", "spaceship_red.png"))
IMG_SPACE = pygame.image.load(os.path.join("assets", "bg_frames", "f0.png"))
IMG_BULLET_POWERUP = pygame.image.load(os.path.join("assets", "bullet_powerup.png"))

# Custom events
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 150, 100
BULLET_WIDTH, BULLET_HEIGHT = 20, 12

# Objects
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)
BACKGROUND = pygame.transform.scale(
    IMG_SPACE,
    (WIDTH, HEIGHT)
)
BULLET_POWERUP = pygame.transform.scale(
    IMG_BULLET_POWERUP,  # Path to IMG
    (WIDTH * 0.05, HEIGHT * 0.05)  # Width & Height of img
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
def draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health):
    # Draw layout
    WIN.blit(BACKGROUND, (0, 0))
    pygame.draw.rect(WIN, BORDER_COLOR, BORDER)

    # Draw scores
    yellow_health_text = FONT_HEALTH.render(f"HP: {yellow_health}", True, WHITE_COLOR)
    red_health_text = FONT_HEALTH.render(f"HP: {red_health}", True, WHITE_COLOR)
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))

    # Draw spaceships
    WIN.blit(SPACESHIP_YELLOW, (yellow.x, yellow.y))
    WIN.blit(SPACESHIP_RED, (red.x, red.y))

    # Draw bullets
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW_SIDE_COLOR, bullet)

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED_SIDE_COLOR, bullet)

    pygame.display.update()


# Draw winner screen
def draw_winner(text):
    winner_text = FONT_WINNER.render(text, True, WHITE_COLOR)
    WIN.blit(winner_text, (WIDTH//2 - winner_text.get_width()//2, HEIGHT//2 - winner_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(2000)  # Restart game after 2 sec


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

    red_health = 10
    yellow_health = 10

    bullet_powerups = []

    clock = pygame.time.Clock()
    run = True  # When false, game terminates
    while run:
        clock.tick(FPS)  # Set FPS

        # Handle events
        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and MAX_BULLETS >= len(yellow_bullets):
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, BULLET_WIDTH, BULLET_HEIGHT)
                    yellow_bullets.append(bullet)
                    pygame.mixer.Channel(1).play(SOUND_BULLET_FIRE)
                if event.key == pygame.K_SLASH and MAX_BULLETS >= len(red_bullets):
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, BULLET_WIDTH, BULLET_HEIGHT)
                    red_bullets.append(bullet)
                    pygame.mixer.Channel(2).play(SOUND_BULLET_FIRE)
            if event.type == RED_HIT:
                red_health -= 1
                pygame.mixer.Channel(2).play(SOUND_BULLET_HIT)
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                pygame.mixer.Channel(1).play(SOUND_BULLET_HIT)

        # Always have bg music
        if not pygame.mixer.Channel(0).get_busy():
            pygame.mixer.Channel(0).play(SOUND_BG_GAME)

        # Check if either side lost/won
        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins"
        elif yellow_health <= 0:
            winner_text = "Yellow Wins"
        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()  # Get all pressed keys

        # Handle movement
        movement_handle_left(keys_pressed, yellow)
        movement_handle_right(keys_pressed, red)

        # Handle bullets
        bullets_handle(yellow_bullets, red_bullets, yellow, red)

        # Generate bullet powerup every few seconds
        #if random.randint(0, 200) == 1:
        #   bullet_powerup = pygame.(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)

        draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health,  red_health)  # Draw window

    main()


if __name__ == '__main__':
    main()
