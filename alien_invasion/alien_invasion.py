import pygame
from settings import Settings
from ship import Ship
from alien import Alien
import game_functions.game_functions as gf
from pygame.sprite import Group
from game_states import GameStates
from button import Button
from scoreboard import Scoreboard


def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # 创建Play按钮
    play = Button(ai_settings, screen, "Play")
    # 创建一个用于存储游戏统计信息的实例
    states = GameStates(ai_settings)
    # 创建记分牌
    scoreboard = Scoreboard(ai_settings, screen, states)

    # 创建一艘飞船
    ship = Ship(ai_settings, screen)
    # 创建一用于存储外星人的编组
    # alien = Alien(ai_settings, screen)
    # 创建外星人群
    aliens = Group()

    # 创建一个用于存储子弹的编组
    bullets = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # 开始游戏的主循环
    while True:
        # 监视键盘和鼠标事件
        gf.check_event(ai_settings, screen, states, play, scoreboard, ship, aliens, bullets)

        if states.game_active:
            # 更新界面
            ship.update()
            # 更新子弹
            gf.update_bullets(ai_settings, screen, states, scoreboard, bullets, ship, aliens)
            # 更新外星人
            gf.update_aliens(ai_settings, states, screen, scoreboard, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, states, scoreboard, ship, aliens, bullets, play)


run_game()
