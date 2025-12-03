import pygame
import random
import math
import sys

# Initialize pygame
pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Player
player_img = pygame.Surface((40, 20))
player_img.fill((0, 255, 0))
player_x = WIDTH // 2 - 20
player_y = HEIGHT - 60
player_speed = 5

# Enemy
enemy_img = pygame.Surface((40, 20))
enemy_img.fill((255, 0, 0))
num_enemies = 6
enemy_x = [random.randint(0, WIDTH - 40) for _ in range(num_enemies)]
enemy_y = [random.randint(50, 150) for _ in range(num_enemies)]
enemy_x_speed = [2 for _ in range(num_enemies)]
enemy_y_step = 40

# Bullet
bullet_img = pygame.Surface((5, 15))
bullet_img.fill((255, 255, 0))
bullet_x = 0
bullet_y = HEIGHT - 60
bullet_speed = 7
bullet_state = "ready"  # "ready" or "fire"

# Score
score = 0
font = pygame.font.SysFont(None, 36)

def show_score():
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 18, y))

def is_collision(ex, ey, bx, by):
    distance = math.sqrt((ex - bx)**2 + (ey - by)**2)
    return distance < 27

# Game loop
clock = pygame.time.Clock()

running = True
while running:
    screen.fill((0, 0, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - 40:
        player_x += player_speed
    if keys[pygame.K_SPACE] and bullet_state == "ready":
        bullet_x = player_x
        fire_bullet(bullet_x, bullet_y)

    # Enemy movement
    for i in range(num_enemies):
        enemy_x[i] += enemy_x_speed[i]

        if enemy_x[i] <= 0 or enemy_x[i] >= WIDTH - 40:
            enemy_x_speed[i] *= -1

        # Collision
        if is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y):
            bullet_y = HEIGHT - 60
            bullet_state = "ready"
            score += 1
            enemy_x[i] = random.randint(0, WIDTH - 40)
            enemy_y[i] = random.randint(50, 150)

        # Draw enemy
        screen.blit(enemy_img, (enemy_x[i], enemy_y[i]))

    # Bullet movement
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_speed

    if bullet_y <= 0:
        bullet_y = HEIGHT - 60
        bullet_state = "ready"

    # Draw player
    screen.blit(player_img, (player_x, player_y))

    show_score()
    pygame.display.update()
    clock.tick(60)