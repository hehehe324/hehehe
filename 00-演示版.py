"""
飞机大战——传智播客·黑马程序员出品
"""
import sys  # 导入系统模块
import random   # 导入随机数模块

import pygame   # 导入pygame模块
import pygame.locals    # 导入pygame本地策略
# from pygame.locals import *

APP_ICON = "res/app.ico"    # 设计公共的图片常量，定义在文件中，方便管理
IMG_BACKGROUND = "res/img_bg_level_2.jpg"   # 设计公共的图片常量，定义在文件中，方便管理
# 设置敌机图片库常量元组
IMG_ENEMYS = ("res/img-plane_1.png","res/img-plane_2.png","res/img-plane_3.png","res/img-plane_4.png","res/img-plane_5.png","res/img-plane_6.png","res/img-plane_7.png")
IMG_PLAYER = "res/hero.png"    # 设置玩家飞机图片
IMG_BULLET = "res/bullet_13.png"    # 设置子弹图片

# 创建所有显示的图形父类Model
class Model:
    window = None   # 定义主窗体对象，用于模型访问使用
    # 构造方法
    def __init__(self,img_path,x,y):
        self.img = pygame.image.load(img_path)  # 背景图片
        self.x = x  # 窗体中放置的x坐标
        self.y = y  # 窗体中放置的y坐标

    # 将模型加入窗体的方法抽取到父类
    def display(self):
        Model.window.blit(self.img, (self.x, self.y))  # 使用Model的类变量访问窗体对象  # 调用bilt方法，将图片加入到窗体中

# 背景类
class Background(Model):
    # 定义背景移动的方法
    def move(self):
        # 加入背景移动的情况判定
        if self.y <= Game.WINDOW_HEIGHT:    # 如果没有超出屏幕就正常移动
            self.y += 1  # 纵坐标自增1
        else:   # 如果超出屏幕，恢复图片位置为原始位置
            self.y = 0  # 纵坐标 = 0

    # 覆盖父类display方法，制作原始背景贴图+辅助背景贴图
    def display(self):
        Model.window.blit(self.img, (self.x, self.y))   # 原始背景贴图，推荐使用super().display()
        Model.window.blit(self.img, (self.x, self.y - Game.WINDOW_HEIGHT)) # 辅助背景，坐标位置与原始背景贴图上下拼接吻合

# 玩家类
class PlayerPlane(Model):
    # 覆盖init方法
    def __init__(self,img_path,x,y):
        super().__init__(img_path,x,y)  # 调用父类init方法
        self.bullets = []   # 定义子弹列表为空，默认没有子弹
    # 重写玩家飞机display方法
    def display(self, enemys):  # 在显示飞机和子弹的同时，传入敌机列表
        super().display()   # 调用父类中对于飞机加入窗体的操作
        remove_bullets = [] # 定义被删除的子弹列表
        for bullet in self.bullets:     # 循环飞机中的子弹列表
            bullet.move()       # 调用子弹的移动操作
            bullet.display()    # 调用子弹加入窗体的操作
            # 优化子弹存储队列，将超出屏幕的子弹删除
            if self.y < -29:    # 如果子弹位置超出屏幕
                remove_bullets.append(bullet)   # 将要删除的子弹加入到待删除列表
            else:   # 如果子弹位置未超出屏幕范围
                bullet_rect = pygame.locals.Rect(bullet.x,bullet.y, 20, 29) # 创建子弹矩形对象，传入x,y,width,height
                for enemy in enemys:    # 使用子弹与所有敌机进行碰撞检测
                    enemy_rect = pygame.locals.Rect(enemy.x, enemy.y, 100, 68)  # 创建敌机矩形对象，传入x,y,width,height
                    # 调用碰撞检测方法，传入当前子弹对象，传入敌机对象，判断是否碰撞
                    if pygame.Rect.colliderect(bullet_rect, enemy_rect):    # 如果碰撞
                        enemy.img = pygame.image.load(IMG_ENEMYS[random.randint(0, 6)]) # TODO 1.敌机被击中后恢复初始状态
                        enemy.x = random.randint(0, Game.WINDOW_WIDTH - 100)    # TODO 1.敌机被击中后恢复初始状态
                        enemy.y = random.randint(-Game.WINDOW_HEIGHT, -68)  # TODO 1.敌机被击中后恢复初始状态
                        remove_bullets.append(bullet)   # TODO 2.将产生碰撞的子弹加入删除列表
                        break   # TODO 3.当前子弹击中了一架敌机，终止对剩余敌机的碰撞检测，终止敌机循环

        for bullet in remove_bullets:   # 循环删除子弹列表
            self.bullets.remove(bullet) # 从原始子弹列表中删除要删除的子弹

# 敌机类
class EnemyPlane(Model):
    # 覆盖init方法
    def __init__(self):
        self.img = pygame.image.load(IMG_ENEMYS[random.randint(0,6)])   # 设置图片路径随机从元组中获取
        self.x = random.randint(0,Game.WINDOW_WIDTH - 100) # 设置x坐标随机生成 横向位置 0 到 屏幕宽度 - 飞机宽度(100)
        self.y = random.randint( - Game.WINDOW_HEIGHT, -68)   # 设置y坐标随机生成 纵向位置 -屏幕高度 到 -飞机高度

    # 定义敌机移动的方法
    def move(self):
        # 判断敌机是否超出屏幕
        if self.y > Game.WINDOW_HEIGHT: # 如果超出屏幕
            self.img = pygame.image.load(IMG_ENEMYS[random.randint(0, 6)]) # 修改敌机到达底部后返回的图片随机生成，同初始化策略
            self.x = random.randint(0, Game.WINDOW_WIDTH - 100) # 修改敌机到达底部后返回顶部的策略，x随机生成，同初始化策略
            self.y = random.randint(-Game.WINDOW_HEIGHT, -68)   # 修改敌机到达底部后返回顶部的策略，y随机生成，同初始化策略
        else:   # 敌机未超出屏幕
            self.y += 4     # 控制敌机向下移动，移动速度设置为4

# 子弹类
class Bullet(Model):
    # 定义子弹的移动方法
    def move(self):
        self.y -= 12    # 设定子弹的移动速度为12

# 游戏类
class Game:
    WINDOW_WIDTH = 512      # 设计窗体尺寸常量，定义在类中，缩小作用范围
    WINDOW_HEIGHT = 768     #设计窗体尺寸常量，定义在类中，缩小作用范围

    # 主程序，运行游戏入口
    def run(self):
        self.frame_init()   # 执行窗体初始化

        self.model_init()   # 执行对象初始化

        while True:     # 构造反复执行的机制，刷新窗体，使窗体保持在屏幕上

            self.background.move()  # 调用背景移动操作，构造背景图片向下移动的效果
            self.background.display()  # 移动完毕后，将移动后的图片加入到窗体中

            for enemy in self.enemys:   # 加入所有敌机
                enemy.move()    # 每驾敌机移动
                enemy.display() # 每驾敌机加入窗体

            self.player.display(self.enemys)  # 飞机加入窗体时，传入敌机列表实参self.enemys # 玩家飞机加入窗体中

            pygame.display.update() # 刷新窗体

            self.event_init()   # 反复调用事件监听方法

    # 初始化窗体
    def frame_init(self):
        self.window = pygame.display.set_mode((Game.WINDOW_WIDTH, Game.WINDOW_HEIGHT))  # 使用窗体常量替换原始格式  # 初始化窗体
        Model.window = self.window  # 将窗体对象传入模型类中
        img = pygame.image.load(APP_ICON)  # 使用图片常量替换原始格式 # 加载图标文件为图片对象
        pygame.display.set_icon(img)    # 设置窗体图标为图片
        pygame.display.set_caption("Plane Battle v1.0 传智播客·黑马程序员出品")    # 设置窗体的标题

    #  定义事件处理的方法
    def event_init(self):
        for event in pygame.event.get():    # 获取当前发生的所有事件
            if event.type == pygame.locals.QUIT :   # 判断当前事件类别是不是点击窗体的关闭按钮
                sys.exit()      # 执行退出系统操作

            if event.type == pygame.locals.MOUSEMOTION :    # 设置监听鼠标移动事件
                pos = pygame.mouse.get_pos()    # 获取鼠标位置坐标，结果是元组
                self.player.x = pos[0] - 120/2      # 设置飞机中心位置在鼠标位置(x)  横坐标 - 飞机宽度1半
                self.player.y = pos[1] - 78/2 + 5   # 设置飞机中心位置在鼠标位置(y)  纵坐标 - 飞机高度1半 +-微调数据

        mouse_state = pygame.mouse.get_pressed()    # 获取鼠标按键压下状态，返回得到元组，其中保存鼠标左中右键按下状态（1,0,0）
        if mouse_state[0] == 1 :    # 判断左键是否按下
            pos = pygame.mouse.get_pos()    # 获取鼠标位置
            self.player.bullets.append(Bullet(IMG_BULLET,pos[0] - 20/2 ,pos[1] - 29 - 40))  # 创建子弹，加入飞机子弹列表，子弹横坐标为鼠标x坐标 - 子弹宽度1半，纵坐标为鼠标y坐标 - 子弹高度 +-微调数据

    # 初始化窗体中的对象
    def model_init(self):
        self.background = Background(IMG_BACKGROUND,0,0) # 扩大背景对象的使用范围  # 使用图片常量替换原始格式 # 初始化背景对象，传入图片路径，放置在0,0位

        self.enemys = []    # 定义用于保存敌机的空列表，保存多驾敌机
        for _ in range(5) : # 循环产生5架敌机
            self.enemys.append(EnemyPlane())    # 修改创建敌机操作

        self.player = PlayerPlane(IMG_PLAYER,200,500)   # 初始化玩家飞机对象，放置在200,500

# 设置测试类入口操作
if __name__ == "__main__":
    Game().run()


