import sys
import pygame
from pygame.sprite import Group
import game_functions as gf
from game_functions import Settings
from game_functions import Ship
from game_functions import GameStats
from game_functions import Button
from scoreboard import Scoreboard
import random


def run_game():
    pygame.init()
    pygame.display.set_caption('Space Invader')
    circulation = False if len(sys.argv) > 1 else True

    ai_setting = Settings()
    screen = pygame.display.set_mode((ai_setting.screen_width, ai_setting.screen_height))

    background = pygame.image.load("images/bg.png")
    background = pygame.transform.smoothscale(background, (ai_setting.screen_width, ai_setting.screen_height))

    ship = Ship(screen, ai_setting)

    aliens = Group()
    alien_bullets = Group()
    stats = GameStats(ai_setting)
    play_button = Button(ai_setting, screen, 'Play')
    sb = Scoreboard(ai_setting, screen, stats)

    gf.create_fleet(ai_setting, screen, aliens, ship)
    screen.fill((0, 0, 0))

    while True:
        screen.blit(background, (0, 0))

        gf.check_events(ai_setting, screen, ship, alien_bullets, aliens, stats, play_button, sb)
        if stats.game_active:
            ship.update()
            gf.update_aliens(ai_setting, stats, screen, aliens, ship, sb, alien_bullets)
        gf.update_screen(screen, ship, aliens, alien_bullets, stats, play_button, sb )
        if  not circulation:
            break

        # save score in a text file
        with open('score.txt', 'w') as f:
            f.write(str(stats.score))
        pygame.display.update()

run_game()


