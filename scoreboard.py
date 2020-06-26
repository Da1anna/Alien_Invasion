# -*- coding:utf-8 -*-
# @Time: 2020/6/24 10:40
# @Author: Lj
# @File: scoreboard.py

import pygame.font
from pygame.sprite import Group

from Alien_Invasion.ship import Ship

class Scoreboard():
    """显示得分信息的类"""

    def __init__(self, ai_settings, screen, stats):
        #初始化设计得分显示的属性
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats

        #得分字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 36)

        #准备初始得分图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """将得分转换成一幅图像，并置于右上角"""
        rounded_score = round(self.stats.score,-1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """将历史最高得分转换成一幅图像，并置于屏幕顶部中间"""
        rounded_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(rounded_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """将玩家等级置于得分下面"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.ai_settings.bg_color)

        self.level_image_rect = self.level_image.get_rect()
        self.level_image_rect.right = self.score_rect.right
        self.level_image_rect.top = self.score_rect.top + 30

    def prep_ships(self):
        """将玩家剩余飞船数置于屏幕左上角"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship.rect.width * ship_number
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """在屏幕上显示得分"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_image_rect)
        self.ships.draw(self.screen)

