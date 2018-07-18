class Settings(object):
    """存储《外星人入侵》 的所有设置的类"""

    def __init__(self):
        """初始化游戏的设置"""

        self.screen_width = 1200
        self.screen_height = 800
        """RGB: 取值范围都为0~255
                (255, 0, 0)表示红色， 
                (0, 255, 0)表示绿色， 
                (0, 0,255)表示蓝色
            """
        self.bg_color = (0, 0, 0)

        # 飞船的设置
        self.ship_speed_factor = 1.5
        # 子弹设置
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 5
        # 外星人设置
        self.alien_speed_factor = 0.3
        self.fleet_drop_speed = 2
        # fleet_direction为1表示向右移， 为-1表示向左移
        self.fleet_direction = 1

