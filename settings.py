class Settings(object):

    def __init__(self):
        self.screen_height = 600
        self.screen_width = 1200
        self.bg_color = (230, 230, 230)
        # bullet setting
        self.bullet_width = 300
        self.bullet_height = 10
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 100
        # alien setting
        self.alien_drop_speed = 10
        self.fleet_direction = 1
        # ships
        self.ships_limit = 3

        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.bullet_speed_factor = 0.8
        self.alien_speed_factor = 0.7
        self.ship_speed_factor = 1
        self.alien_points = 5

    def increase_speed(self):
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.ship_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)