import pygame
import pygame.locals
import sys
import random
class Model():      #绘制模型
    """窗口大小，窗口实现形式"""
    #1.TODO：构造窗体
    WINDOW_HIGHT = 768
    WINDOW_WIDTH = 512
    WINDOW = None

    def __init__(self,img_path,x,y):        #初始化模型
        self.img = pygame.image.load(img_path)  #图片传入方式
        self.x = x
        self.y = y                  #窗口坐标
    def dispaly(self):      #图片发送到窗体实现方法
        Model.WINDOW.blit(self.img,(self.x,self.y))

class Background(Model):    #定义背景类
    """导入背景图片，实现背景移动"""
    def display(self):          #窗体背景实现方法
        Model.WINDOW.blit(self.img,(self.x,self.y))
        Model.WINDOW.blit(self.img,(self.x,self.y - Model.WINDOW_HIGHT))
    def move(self):         #窗体背景移动实现方法
        if self.y > Model.WINDOW_HIGHT:
            self.y = 0
        else:
            self.y += 1

class PlayerPlane(Model):
    """1.飞机模型
        2.子弹
        3.碰撞--重叠
        4.移动":子弹，飞机"""
    def __init__(self,img_path,x,y):
        super().__init__(img_path,x,y)             #战机机模型
        # self.bullet_img = pygame.image.load(bullet_img_path)            #子弹模型
        self.bullets = []       #定义炮弹列表
    def display(self,enemys):
        super().dispaly()
        for bullet in bullets:
            bullet.move
            bullet.display()
            bullet_react = pygame.locals.Rect(bullet.x, bullet.y, 100, 68)
            if pygame.Rect.colliderect(bullet_rect, enemy_rect):  # 如果碰撞
                enemy.img = pygame.image.load(IMG_ENEMYS[random.randint(0, 6)])  # TODO 1.敌机被击中后恢复初始状态
                enemy.x = random.randint(0, Model.WINDOW_WIDTH - 100)  # TODO 1.敌机被击中后恢复初始状态
                enemy.y = random.randint(-Model.WINDOW_HEIGHT, -68)  # TODO 1.敌机被击中后恢复初始状态
                remove_bullets.append(bullet)  # TODO 2.将产生碰撞的子弹加入删除列表
                break
    def move(self):
        pos = pygame.mouse.get_pos()        #飞机的中心坐标设置在鼠标坐标
        self.x = pos[0] - 120/2
        self.y = pos[1] -132
    # def fire(self):                  #开火展示
    #     """1.移动
    #         2.开火
    #         3.重叠"""
    #     super().dispaly
    #     bullet -= 12
    #     for bullet in self.bullets:
    #         bullet.move()
    #         bullet.display()
    #         bullet_react = pygame.locals.Rect(bullet.x,bullet.y,100,68)       #创建炮火爆炸矩形，坐标为敌机，长宽100，,6
    #         for enemy in enemys:
    #             enemy_react = pygame.locals.Rect(enemy.x,enemy.y,20,29)
    #             if pygame.Rect.colliderect(bullet_rect, enemy_rect):  # 如果碰撞
    #                 enemy.img = pygame.image.load(IMG_ENEMYS[random.randint(0, 6)])  # TODO 1.敌机被击中后恢复初始状态
    #                 enemy.x = random.randint(0, Game.WINDOW_WIDTH - 100)  # TODO 1.敌机被击中后恢复初始状态
    #                 enemy.y = random.randint(-Game.WINDOW_HEIGHT, -68)  # TODO 1.敌机被击中后恢复初始状态
    #                 remove_bullets.append(bullet)  # TODO 2.将产生碰撞的子弹加入删除列表
    #                 break
class EnemyPlane(Model):
    def __init__(self,enemys):
        self.img = pygame.image.load(IMG_ENEMYS[random.randint(0,6)])       #敌机模型随机选取
        enemy.x = random.randint(0,Model.WINDOW_WIDTH - 100)
        enemy.y = random.randint(-Model.WINDOW_HIGHT,-68)
        self.enemys = []#敌机被摧毁后恢复原样
    def move(self):
        if self.y <= Model.WINDOW_HIGHT:
            self.y += 4
        else:
            EnemyPlane.__init__()
    def fired(self,bullet_rect):
        for enemy in self.enemys:
            enemy_react = pygame.locals.Rect(enemy.x,enemy.y,100,68)
            if pygame.Rect.colliderect(bullet_rect,enemy_react):
                self.__init__()
class Game():
    """1.初始化窗体
        2.加入战机：玩家-敌机
        3.加入子弹
        4.加入事件监听机制----事件：鼠标点击，鼠标移动，关闭"""
    """加载模型框架"""
    def frame_init(self):
        self.WINDOW = pygame.display.set_mode((Model.WINDOW_WIDTH,Model.WINDOW_HIGHT))
        Model.WINDOW = self.WINDOW
        img = pygame.image.load("C:/Users/Rioron/PycharmProjects/untitled11/res/app.ico")
        pygame.display.set_icon(img)
        pygame.display.set_caption("Plane Battle v1.0 何祥琪 出品")
    """加载窗体对象：背景，敌机，战机"""
    def model_init(self):
        jpg_bg = pygame.image.load("res/img_bg_level_2.jpg")            #加入背景
        self.background = Background(jpg_bg,0,0)
        # for _ in range(5):          #加入                                            敌机
        #     EnemyPlane.enemys.append(EnemyPlane())
        img_player = pygame.image.load("res/hero2.png")              #加入战机
        img_player1 = pygame.image.load("res/hero_bullet_7.png")
        self.player = PlayerPlane(img_player,200,500)
    def run(self):
        self.frame_init()
        # self.model_init()
        while True:
            self.background.move()
            self.background.display()
            pygame.display.update()
if __name__ == "__main__":
    Game().run()
