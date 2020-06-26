# -*- coding:utf-8 -*-
# @Time: 2020/6/22 21:16
# @Author: Lj
# @File: game_stats.py

class Game_stats():
    """跟踪游戏的统计信息"""

    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.game_active = False     #游戏启动时处于非活跃状态
        self.high_score = 0     #玩家获得的最高分

        self.reset_stats()

    def reset_stats(self):
        """初始化游戏期间可能变化的统计信息"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1      #玩家等级