
import pygame.font

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
    # self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
    self.msg_image = pygame.image.load('images/play.png')
    self.msg_image_rect = self.msg_image.get_rect()
    self.msg_image_rect.center = self.screen_rect.center

  def draw_button(self):
    self.screen.fill(self.button_color, self.rect)
    self.screen.blit(self.msg_image, self.msg_image_rect)