class GameStats(object):
  def __init__(self, ai_setting):
    self.ai_setting = ai_setting
    self.game_active = False
    self.high_score = 0
    self.reset_stats() 

  def reset_stats(self):
    self.ships_left = self.ai_setting.ships_limit
    self.score = 0
    self.level = 1