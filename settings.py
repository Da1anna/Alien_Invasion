# -*- coding:utf-8 -*-
# @Time: 2020/6/20 10:49
# @Author: Lj
# @File: settings.py

class Settings():
    """储存《外星人入侵》的所有设置的类"""

    def __init__(self):
        """游戏的静态设置"""
        #屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)

        #飞船设置
        self.ship_speed_factor = 1.5
        self.ship_limit = 2

        #子弹设置
        self.bullet_speed_factor = 3
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullet_allowed = 5

        #外星人设置
        self.alien_speed_factor = 1
        self.alien_drop_speed = 10
        self.alien_direction = 1    #1表示向右，-1表示向左
        self.alien_points = 10

        #加快游戏节奏
        self.speedup_scale = 1.2
        #外星人分数提升速度
        self.alien_points_scale = 1.5

        #初始化动态设置
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化动态设置"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        self.alien_drop_speed = 10


        self.alien_direction = 1    #1表示向右，-1表示向左

    def increase_speed(self):
        """游戏速度加快时发生变更的设置"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_drop_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.alien_points_scale)