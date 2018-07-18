import sys
import pygame
from bullet import Bullet
from alien import Alien


# 按键按下
def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        # 向右移动飞船
        # ship.rect.centerx += 1
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # 向左移动飞船
        # ship.rect.centerx -= 1
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        # 向上移动飞船
        ship.moving_top = True
    elif event.key == pygame.K_DOWN:
        # 向下移动飞船
        ship.moving_bottom = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_ESCAPE:
        sys.exit()


# 按键抬起
def check_keyup_event(event, ship):
    if event.key == pygame.K_RIGHT:
        # 按键抬起停止移动
        # ship.rect.centerx += 1
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        # 向左移动飞船
        # ship.rect.centerx -= 1
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        # 向上移动飞船
        # ship.rect.centerx -= 1
        ship.moving_top = False
    elif event.key == pygame.K_DOWN:
        # 向下移动飞船
        # ship.rect.centerx -= 1
        ship.moving_bottom = False


# 查询按键情况
def check_event(ai_settings, screen, ship, bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_event(event, ship)


# 子弹设置
def fire_bullet(ai_settings, screen, ship, bullets):
    """"如果没有达到限制，就发射一颗子弹"""
    # 创建一颗子弹， 并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


# 更新子弹
def update_bullets(ai_settings, screen, bullets, ship, aliens):
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)
        # print(len(bullets))
        check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)


# 子弹和外星人消失
def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
    # 检查是否有子弹击中了外星人
    # 如果是这样， 就删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if len(aliens) == 0:
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)


# 更新屏幕
def update_screen(ai_settings, screen, ship, aliens, bullets):
    """更新屏幕上的图像， 并切换到新屏幕"""
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    # 让最近绘制的屏幕可见
    pygame.display.flip()


# 计算每行可容纳的外星人
def get_number_aliens_x(ai_settings, alien_width):
    """计算每行可容纳多少个外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


# 计算屏幕可容纳多少行外星人
def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


# 创建一个外星人
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人并将其放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


# 创建外星人群
def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    # 创建一个外星人， 并计算一行可容纳多少个外星人
    # 外星人间距为外星人宽度
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    for number_row in range(number_rows):
        for alien_number in range(number_aliens_x):
            # 创建一个外星人并将其加入当前行
            create_alien(ai_settings, screen, aliens, alien_number, number_row)


def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移， 并改变它们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, aliens):
    """检查是否有外星人位于屏幕边缘， 并更新整群外星人的位置
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()