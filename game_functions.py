# -*- coding:utf-8 -*-
# @Time: 2020/6/20 11:30
# @Author: Lj
# @File: game_functions.py

import sys
from time import sleep

import pygame

from Alien_Invasion.bullet import Bullet
from Alien_Invasion.alien import Alien

def check_events(ship,ai_settings, screen,bullets, stats, play_button, aliens, score):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(ship, event, ai_settings, screen,bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(ship, event)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            _check_play_button(ai_settings, screen, aliens, ship, stats, bullets, play_button, mouse_x, mouse_y, score)

def _check_play_button(ai_settings, screen, aliens, ship, stats, bullets, play_button, mouse_x, mouse_y, score):
    """检测玩家是否点击了play键"""
    button_clicked =  play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True

        #重置记分牌信息
        score.prep_score()
        score.prep_high_score()
        score.prep_level()
        score.prep_ships()

        #清空外星人和子弹
        aliens.empty()
        bullets.empty()

        #重置游戏速度设置
        ai_settings.initialize_dynamic_settings()

        #创建外星人和飞船
        create_alien_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()

        #隐藏光标
        pygame.mouse.set_visible(False)

def check_keydown_events(ship, event, ai_settings, screen,bullets):
    """响应按下键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(bullets, ai_settings, screen, ship)
    #结束游戏键
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(ship, event):
    """响应松开键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def update_screen(ai_settings, screen, ship, bullets, aliens, play_button, stats, score):
    """更新屏幕上的图像，并切换到新屏幕"""
    #每次循环时都重绘图像
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    aliens.draw(screen)     #对aliens组里面每个成员调用blitme()

    #更新所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    #显示得分板
    score.show_score()

    #创建play按钮
    if stats.game_active == False:
        play_button.draw_button()

    #让最近绘制的图像可见
    pygame.display.flip()

def update_bullets(bullets, aliens, ai_settings, screen, ship, stats, score):
    """更新子弹位置，并消除消失的子弹"""
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    _check_bullet_alien_collision(bullets, aliens, ai_settings, screen, ship, stats, score)

def _check_bullet_alien_collision(bullets, aliens, ai_settings, screen, ship, stats, score):
    """响应子弹和外星人的碰撞"""
    # 删除击中外星人的子弹
    collisoins = pygame.sprite.groupcollide(bullets, aliens, True, True)

    #消灭外星人后得分
    if collisoins:
        for aliens in collisoins.values():
            stats.score += ai_settings.alien_points * len(aliens)
            score.prep_score()
        _check_high_score(stats, score)

    # 若外星人全部消灭，则加快游戏速度，新建舰队
    if len(aliens) == 0:
        bullets.empty()     #删除所有子弹

        stats.level += 1    #提高玩家等级
        score.prep_level()
        ai_settings.increase_speed()

        create_alien_fleet(ai_settings, screen, aliens, ship)

def _check_high_score(stats, score):
    """检测是否诞生了最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        score.prep_high_score()

def fire_bullets(bullets, ai_settings, screen, ship):
    """发射子弹"""
    # 创建一颗子弹，并将其加入到编组中
    if len(bullets) < ai_settings.bullet_allowed:
        bullet = Bullet(ai_settings, screen, ship)
        bullets.add(bullet)

def create_alien_fleet(ai_settings, screen, aliens, ship):
    """创建外星人群"""
    #创建一个外星人
    alien = Alien(ai_settings, screen)
    number_aliens_x = _get_number_aliens_x(ai_settings, alien.rect.width)
    rows_number = _get_rows_number(ai_settings, alien.rect.height, ship.rect.height)

    #创建外星人舰队
    for row_number in range(rows_number):
        for alien_number in range(number_aliens_x):
            _create_alien(ai_settings, screen, aliens, alien_number, row_number)

def _get_number_aliens_x(ai_settings, alien_width):
    """计算一行可容纳多少个外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = available_space_x // (2 * alien_width)
    return number_aliens_x

def _get_rows_number(ai_settings, alien_height, ship_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = ai_settings.screen_height - 5*alien_height - ship_height
    rows_number = available_space_y // (2 * alien_height)
    return rows_number

def _create_alien(ai_settings, screen, aliens, alien_number, rows_number):
    """根据位置创建外星人"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height

    alien.x = alien_width + 2 * alien_number * alien_width
    alien.rect.x = alien.x
    alien.rect.y = 2*alien_height + 2 * rows_number * alien_height

    aliens.add(alien)

def update_aliens(aliens, ai_settings, ship, stats, bullets, screen, score):
    """检查是否有外星人到达屏幕边缘，并更新外星人位置"""
    _check_fleet_edges(aliens, ai_settings)
    aliens.update()

    #检测外星人与飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        _ship_hit(aliens, ai_settings, ship, stats, bullets, screen, score)

    #检测外星人是否到达屏幕底部
    _check_alien_bottom(aliens, ai_settings, ship, stats, bullets, screen, score)

def _check_alien_bottom(aliens, ai_settings, ship, stats, bullets, screen, score):
    """检查是否有外星人到达屏幕底部"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.top >= screen_rect.bottom:
            _ship_hit(aliens, ai_settings, ship, stats, bullets, screen, score)
            break

def _ship_hit(aliens, ai_settings, ship, stats, bullets, screen, score):
    """响应飞船被外星人碰撞"""
    if stats.ships_left > 0:
        stats.ships_left -= 1

        #更新记分牌
        score.prep_ships()

        aliens.empty()
        bullets.empty()

        #创建一群新的外星人
        create_alien_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()

        #暂停
        sleep(1)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def _check_fleet_edges(aliens, ai_settings):
    """检测是否有外星人到达屏幕边缘"""
    for alien in aliens.sprites():
        if alien.check_alien_edge():
            _change_fleet_direction(aliens, ai_settings)

def _change_fleet_direction(aliens, ai_settings):
    """改变外星人舰队的方向,并整体向下移"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.alien_drop_speed
    ai_settings.alien_direction *= -1
