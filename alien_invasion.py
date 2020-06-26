# -*- coding:utf-8 -*-
# @Time: 2020/6/20 10:33
# @Author: Lj
# @File: alien_invasion.py


import pygame
from pygame.sprite import Group

from Alien_Invasion.settings import Settings
from Alien_Invasion.ship import Ship
import Alien_Invasion.game_functions as gf
from Alien_Invasion.game_stats import Game_stats
from Alien_Invasion.button import Button
from Alien_Invasion.scoreboard import Scoreboard

def run_game():
    """

    """
    #初始化游戏并创建一个屏幕
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,
                                      ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    #创建开始按钮
    play_button = Button(ai_settings, screen, "Play")
    #创建一个用于游戏统计的实例
    stats = Game_stats(ai_settings)
    #创建一艘飞船
    ship = Ship(ai_settings, screen)
    #创建一个用于存放子弹的编组
    bullets = Group()
    #创建一个外星人编组
    aliens = Group()
    #创建外星人群
    gf.create_alien_fleet(ai_settings, screen, aliens, ship)
    #创建一个记分板
    score = Scoreboard(ai_settings, screen, stats)

    #游戏的主循环
    while True:
        #响应鼠标和按键事件
        gf.check_events(ship,ai_settings, screen,bullets, stats, play_button, aliens, score)
        if stats.game_active:
            #更新飞船位置
            ship.update()
            #更新子弹
            gf.update_bullets(bullets, aliens, ai_settings, screen, ship, stats, score)
            #更新外星人
            gf.update_aliens(aliens, ai_settings, ship, stats, bullets, screen, score)
        #更新屏幕
        gf.update_screen(ai_settings, screen, ship, bullets, aliens, play_button, stats, score)

run_game()


