import sys
import pygame
from pygame.sprite import Group
import game_functions as gf
from settings import Settings
from game_functions import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from pygame.sprite import Sprite


def run_game():
    pygame.init()
    pygame.display.set_caption('Space Invader')
    circulation = False if len(sys.argv) > 1 else True

    ai_setting = Settings()
    screen = pygame.display.set_mode((ai_setting.screen_width, ai_setting.screen_height))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 40)  # default font, size 40

    start_time = pygame.time.get_ticks()
    background = pygame.image.load("images/bg.png")

    ship = Ship(screen, ai_setting)
    bullets = Group()
    aliens = Group()
    stats = GameStats(ai_setting)
    play_button = Button(ai_setting, screen, 'Play')
    sb = Scoreboard(ai_setting, screen, stats)

    gf.create_fleet(ai_setting, screen, aliens, ship)
    # Get elapsed time in seconds
    elapsed_ms = pygame.time.get_ticks() - start_time
    elapsed_sec = elapsed_ms // 1000

    # Format as mm:ss
    minutes = elapsed_sec // 60
    seconds = elapsed_sec % 60
    time_text = f"{minutes:02}:{seconds:02}"

    # Render
    scoreboard = font.render(f"Time: {time_text}", True, (255, 255, 255))

    screen.fill((0, 0, 0))

    while True:
        screen.blit(background, (0, 0))
        screen.blit(scoreboard, (120, 20))
        # pygame.display.flip()

        gf.check_events(ai_setting, screen, ship, bullets, aliens, stats, play_button, sb)
        if stats.game_active:
            ship.update()
            gf.update_bullets(bullets, ai_setting, screen, aliens, ship, stats, sb)
            gf.update_aliens(ai_setting, stats, screen, aliens, ship, bullets, sb)
        gf.update_screen(ai_setting, screen, ship, aliens, bullets, stats, play_button, sb)
        if  not circulation:
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(' score ', stats.high_score)
                with open('score.txt', 'w') as f:
                    f.write(str(stats.high_score))
                sys.exit()

            # Update display

        pygame.display.update()

run_game()


