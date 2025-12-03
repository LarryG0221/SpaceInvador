
import sys 
import pygame
from time import sleep
from pygame.sprite import Sprite

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

# create a bullet shot
class Bullet(Sprite):

    def __init__(self, screen, ship):
        super().__init__()
        self.screen = screen

        # set a bullet at (0,0), size is 10*10
        self.rect = pygame.Rect(0, 0, 10, 10)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        self.y = float(self.rect.y)
        # bullet color is red
        self.color =  (255, 60, 60)
        self.speed_factor = 0.9

    def update(self):
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

def fire_bullet( screen, ship, bullets):
    bullets_max = 100
    if len(bullets) < bullets_max:
        new_bullet = Bullet(screen, ship)
        bullets.add(new_bullet)

def detect_key_events(event, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(screen, ship, bullets)
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
        sb.prep_level()
        sb.prep_ships()

        create_fleet(ai_setting, screen, aliens, ship)
        ship.center_ship()


def check_events(ai_setting, screen, ship, bullets, aliens, stats, play_button, sb):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            detect_key_events(event, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y, ai_setting, screen, ship, bullets, aliens, sb)


def update_screen(ai_setting, screen, ship, aliens, bullets, stats, play_button, sb):
    # update the screen
    screen.fill(ai_setting.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()

    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()


def check_high_score(stats, sb):
    # update score if there is highter score
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_bullet_alien_collisions(bullets, ai_setting, screen, aliens, ship, stats, sb):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for als in collisions.values():
            stats.score += ai_setting.alien_points * len(als)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        bullets.empty()
        ai_setting.increase_speed()
        create_fleet(ai_setting, screen, aliens, ship)

        stats.level += 1
        sb.prep_level()


def update_bullets(bullets, ai_setting, screen, aliens, ship, stats, sb):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(bullets, ai_setting, screen, aliens, ship, stats, sb)            


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
        

def check_fleet_edges(ai_setting, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_direction(ai_setting, aliens)
            break


def change_direction(ai_setting, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_setting.alien_drop_speed
    ai_setting.fleet_direction *= -1


def ship_hit(ai_setting, stats, screen, aliens, ship, bullets, sb):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
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


def update_aliens(ai_setting, stats, screen, aliens, ship, bullets, sb):
    check_fleet_edges(ai_setting, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_setting, stats, screen, aliens, ship, bullets, sb)
    check_aliens_bottom(ai_setting, stats, screen, aliens, ship, bullets, sb)