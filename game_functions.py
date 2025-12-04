import sys
import pygame
from time import sleep
from pygame.sprite import Sprite
import random
import pygame.font

# save game settings
class Settings(object):

    def __init__(self):
        self.screen_height = 600
        self.screen_width = 1200
        self.bg_color = (230, 230, 230)

        # alien setting
        self.fleet_direction = 1
        # ships
        self.ships_limit = 3

        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.alien_speed_factor = 0.7
        self.ship_speed_factor = 1
        self.alien_points = 5


# save game data
class GameStats(object):
    def __init__(self, ai_setting):
        self.ai_setting = ai_setting
        self.game_active = False
        self.reset_stats()

    def reset_stats(self):
        self.ships_left = self.ai_setting.ships_limit
        self.score = 0
        self.last_score_time = pygame.time.get_ticks()
        self.start_time = 0

# create button
class Button(object):
  def __init__(self, ai_setting, screen, msg):
    self.ai_setting = ai_setting
    self.screen = screen
    self.screen_rect = self.screen.get_rect()

    self.width, self.height = 200, 50
    self.button_color = (0, 0, 0)
    self.text_color = (0, 255, 255)
    self.font = pygame.font.SysFont(None, 48)
    # set rectangle w/h
    self.rect = pygame.Rect(0, 0, self.width, self.height)
    self.rect.center = self.screen_rect.center
    self.msg_image = pygame.image.load('images/play.png')
    self.msg_image_rect = self.msg_image.get_rect()
    self.msg_image_rect.center = self.screen_rect.center

  def draw_button(self):
    self.screen.fill(self.button_color, self.rect)
    self.screen.blit(self.msg_image, self.msg_image_rect)


# create an alien
class Alien(Sprite):
    def __init__(self, ai_setting, screen):
        super().__init__()
        self.ai_setting = ai_setting
        self.screen = screen
        self.image = pygame.image.load('images/enemy.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = self.rect.x

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        alien_speed = 0.6
        self.x += alien_speed * self.ai_setting.fleet_direction
        self.rect.x = self.x

# create a space ship
class Ship(Sprite):
    def __init__(self, screen, ai_setting):
        super().__init__()
        # set ship at its initial position
        self.screen = screen
        self.moving_right = False
        self.moving_left = False
        self.ai_setting = ai_setting
        # set ship img
        self.image = pygame.image.load('images/blueship.png')
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()
        # ship should be put at the screen bottom
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.center = float(self.rect.centerx)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.moving_right and self.rect.centerx < self.screen_rect.right:
            self.center += self.ai_setting.ship_speed_factor
        elif self.moving_left and self.rect.centerx > 0:
            self.center -= self.ai_setting.ship_speed_factor

        self.rect.centerx = self.center

    def center_ship(self):
        self.center = self.screen_rect.centerx

# create Bullet for Alien
class AlienBullet(Sprite):
    def __init__(self, screen, alien):
        super().__init__()
        self.screen = screen

        # Set the bullet’s initial position and size
        self.rect = pygame.Rect(0, 0, 10, 10)
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.bottom

        self.y = float(self.rect.y)
        self.color = (204, 0, 0)  # Blue for alien bullets
        self.speed_factor = 0.5  # Speed of alien bullet

    def update(self):
        self.y += self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)


def fire_alien_bullet( screen, aliens, alien_bullets):
    # Randomly pick an alien to fire
    if random.randint(1, 50) == 1:  # 1 in 50 chance per frame
        alien = random.choice(aliens.sprites())
        new_bullet = AlienBullet(screen, alien)
        alien_bullets.add(new_bullet)


def update_alien_bullets(ai_setting, alien_bullets, screen, ship,aliens, stats, sb):
    alien_bullets.update()
    # Remove bullets that are off the screen
    for bullet in alien_bullets.copy():
        if bullet.rect.top >= screen.get_rect().bottom:
            alien_bullets.remove(bullet)
    # Check for collisions with the player's ship
    if pygame.sprite.spritecollideany(ship, alien_bullets):
        ship_hit(ai_setting, stats, screen, aliens, ship, alien_bullets, sb)


def detect_key_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_play_button(stats, play_button, mouse_x, mouse_y, ai_setting, screen, ship, bullets, aliens, sb):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        pygame.mouse.set_visible(False)
        ai_setting.initialize_dynamic_settings()
        stats.reset_stats()
        stats.game_active = True

        aliens.empty()
        bullets.empty()

        sb.prep_score()
        sb.prep_lives()

        create_fleet(ai_setting, screen, aliens, ship)
        ship.center_ship()


def check_events(ai_setting, screen, ship, bullets, aliens, stats, play_button, sb):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            detect_key_events(event, ship)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y, ai_setting, screen, ship, bullets, aliens, sb)


def update_screen(screen, ship, aliens, alien_bullets, stats, play_button, sb ):

    for alien_bullet in alien_bullets.sprites():
        alien_bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    sb.prep_lives()
    sb.show_lives()
    # Prepare the elapsed time
    # Show the elapsed time
    sb.prep_elapsed_time()
    sb.show_elapsed_time()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()


def get_number_aliens_x(ai_setting, alien_width):

    available_space_x = ai_setting.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_aliens_y(ai_setting, alien_height, ship_height):
    available_space_y = ai_setting.screen_height - 3 * alien_height - ship_height
    number_aliens_y = int(available_space_y / (2 * alien_height))
    return number_aliens_y


def create_alien(ai_setting, screen, aliens, alien_number, row_number):
    alien = Alien(ai_setting, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien_height + 2 * alien_height * row_number
    aliens.add(alien)


def create_fleet(ai_setting, screen, aliens, ship):

    alien = Alien(ai_setting, screen)
    number_aliens_x = get_number_aliens_x(ai_setting, alien.rect.width)
    number_aliens_y = get_number_aliens_y(ai_setting, alien.rect.height, ship.rect.height)

    for row_number in range(number_aliens_y):
        for alien_number in range(number_aliens_x):
            create_alien(ai_setting, screen, aliens, alien_number, row_number)


def ship_hit(ai_setting, stats, screen, aliens, ship, aline_bullets, sb):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_lives()
        aliens.empty()
        aline_bullets.empty()
        create_fleet(ai_setting, screen, aliens, ship)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)



def check_aliens_bottom(ai_setting, stats, screen, aliens, ship, bullets, sb):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_setting, stats, screen, aliens, ship, bullets, sb)
            break


def update_score(stats, sb):
    # Check if 2 seconds have passed since the last score update
    current_time = pygame.time.get_ticks()  # Get the current time in milliseconds
    if current_time - stats.last_score_time >= 2000:  # 2000ms = 2 seconds
        stats.score += 5  # Add 5 points to the score
        sb.prep_score()  # Update the score on the screen
        stats.last_score_time = current_time  # Update the last score time to the current time


def update_aliens(ai_setting, stats, screen, aliens, ship, sb, alien_bullets):
    # Existing alien movement and collision handling
    for alien in aliens.sprites():
        if alien.check_edges():
            ai_setting.fleet_direction *= -1
            break
    aliens.update()

    # Randomly fire alien bullets
    fire_alien_bullet(screen, aliens, alien_bullets)

    # Update alien bullets
    update_alien_bullets(ai_setting, alien_bullets, screen, ship, aliens, stats, sb)
    update_score(stats, sb)

    # Check if the ship collides with any alien bullets
    check_aliens_bottom(ai_setting, stats, screen, aliens, ship, alien_bullets, sb)
