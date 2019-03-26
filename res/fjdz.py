#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pygame
import sys
import pygame.locals
import random
img_icon = "C:/Users/Rioron/PycharmProjects/untitled11/res/app.ico"
img_bg = "C:/Users/Rioron/PycharmProjects/untitled11/res/img_bg_level_1.jpg"
img_player = "C:/Users/Rioron/PycharmProjects/untitled11/res/hero.png"
img_enemys = ("C:/Users/Rioron/PycharmProjects/untitled11/res/img-plane_1.png","C:/Users/Rioron/PycharmProjects/untitled11/res/img-plane_2.png","C:/Users/Rioron/PycharmProjects/untitled11/res/img-plane_3.png","C:/Users/Rioron/PycharmProjects/untitled11/res/img-plane_4.png"
              ,"C:/Users/Rioron/PycharmProjects/untitled11/res/img-plane_5.png","C:/Users/Rioron/PycharmProjects/untitled11/res/img-plane_6.png","C:/Users/Rioron/PycharmProjects/untitled11/res/img-plane_7.png")
img_bullet = "C:/Users/Rioron/PycharmProjects/untitled11/res/bullet_2.png"
msc_bg = "C:/Users/Rioron/PycharmProjects/untitled11/res/bg.wav"
msc_bomb = "C:/Users/Rioron/PycharmProjects/untitled11/res/bomb.wav"
msc_gover = "C:/Users/Rioron/PycharmProjects/untitled11/res/gameover.wav"
class Model():
    WINDOW_HEIGHT = 768
    WINDOW_WIDTH = 512
    window = None                       #定义类变量
    def __init__(self,img,x,y):
        self.img = pygame.image.load(img)
        self.x = x
        self.y = y
    def display(self):
        self.window.blit(self.img,(self.x,self.y))          #构造窗体展示方法
    @staticmethod
    def is_hit(rect1,rect2):            #判断两个矩形是否重叠
        return pygame.Rect.colliderect(rect1,rect2)
class Background(Model):
    def move(self):
        if self.y <Model.WINDOW_HEIGHT:
            self.y+=4
        else:
            self.y = 0
    def display(self):
        self.window.blit(self.img,(self.x,self.y))
        self.window.blit(self.img,(self.x,self.y - Model.WINDOW_HEIGHT))
class PlayerPlane(Model):
    def __init__(self,img,x,y):
        super().__init__(img,x,y)
        self.bullets=[]             #子弹类实例存放在子弹列表中
    def display(self,eonemys):        #优先访问子类,  todo:这里的enemys是同名参数
        super().display()              #看起来这里的enemys作用,属性与Enemy相同，但实际上只有名称相同
        bullet_remove = []
        player_react = pygame.locals.Rect(self.x,self.y,120,78)
        for bullet in self.bullets:
            bullet_react = pygame.locals.Rect(bullet.x,bullet.y,20,29)      #为每颗子弹创建矩形
            if bullet.y < -29:
                bullet_remove.append(bullet)
            else:
                for ene in eonemys:            #
                    ene_react = pygame.locals.Rect(ene.x,ene.y,100,68)        #为每个敌人创建矩形
                    if Model.is_hit(bullet_react,ene_react):
                        ene.is_hited = True             #todo:
                        Game.SCORES += 1
                        ene.bomb.is_show = True
                        ene.bomb.x = ene.x
                        ene.bomb.y = ene.y
                        ene.bomb.display()        #如果子弹击中敌人，则调用子弹爆炸效果
                        sound = pygame.mixer.Sound(msc_bomb)            #创建声音实例
                        sound.play()
                        bullet_remove.append(bullet)
                        break
        for bullet in bullet_remove:
            self.bullets.remove(bullet)
        for ene in eonemys:
            ene_react = pygame.locals.Rect(ene.x,ene.y,100,68)
            if Model.is_hit(player_react,ene_react):
                ene.is_hited = True
                pygame.mixer.music.load(msc_gover)
                pygame.mixer.music.play(loops =1)
                return 2
        return 1
class EnemyPlane(Model):
    def __init__(self):
        self.img = pygame.image.load(img_enemys[random.randint(0,6)])
        self.x = random.randint(0,Model.WINDOW_WIDTH-100)
        self.y = random.randint(-Model.WINDOW_HEIGHT,-68)
        # super().__init__()
        self.is_hited = False
        self.bomb = Bomb()
    def move(self):
        if self.y < Model.WINDOW_HEIGHT and not self.is_hited:     #敌机被击中，或者被敌机到达窗口底部
            self.y += 6                                             #则敌机初始化
        else:
            self.__init__()


class Bullet(Model):
    def move(self):
        self.y -= 12
    pass
class Bomb(Model):
    def __init__(self):
        # self.x = None
        # self.y = None
        self.imgs =[pygame.image.load("C:/Users/Rioron/PycharmProjects/untitled11/res/bomb-%d.png" %i) for i in range(1,8)]
        self.is_show = False
        self.times = 0
    def display(self):
        if self.is_show and self.times<len(self.imgs)*10:
            self.window.blit(self.imgs[self.times//10],(self.x,self.y))
            self.times += 1
        else:
            self.times = 0
            self.is_show = False


class Game():
    SCORES = 0
    def __init__(self):
        self.game_status = 0
        self.game_level = 0
    def run(self):          #TODO:游戏程序入口
        pygame.init()
        pygame.mixer.init()         #背景音乐模块初始化

        self.frame_init()
        self.model_init()

        pygame.mixer.music.play()
        while True:
            pygame.init()
            self.background.display()
            self.background.move()
            # self.event_init()

            # self.player.display(self.enemys)           #实例调用子类类的父类的display方法，当子类有
                                            #同名方法时，优先访问子类

            if self.game_status == 0:
                font_over = pygame.font.Font("C:/Users/Rioron/PycharmProjects/untitled11/res/DENGB.TTF",40)
                text_over = font_over.render("飞机大战",1,(255,255,0))
                self.window.blit(text_over,pygame.locals.Rect(256-80,200,226,43))

                font_over = pygame.font.Font("C:/Users/Rioron/PycharmProjects/untitled11/res/DENGB.TTF",40)
                text_over = font_over.render("请选择难度：",1,(255,255,255))
                self.window.blit(text_over,pygame.locals.Rect(256-80,300,226,43))

                font_over = pygame.font.Font("C:/Users/Rioron/PycharmProjects/untitled11/res/DENGB.TTF",40)
                text_over = font_over.render("1-简单",1,(0,255,0))
                self.window.blit(text_over,pygame.locals.Rect(256-45,350,226,43))

                font_over = pygame.font.Font("C:/Users/Rioron/PycharmProjects/untitled11/res/DENGB.TTF",40)
                text_over = font_over.render("2-一般",1,(0,255,0))
                self.window.blit(text_over,pygame.locals.Rect(256-45,400,226,43))

                font_over = pygame.font.Font("C:/Users/Rioron/PycharmProjects/untitled11/res/DENGB.TTF",40)
                text_over = font_over.render("3-困难",1,(0,255,0))
                self.window.blit(text_over,pygame.locals.Rect(256-45,450,226,43))


            elif self.game_status == 1:


                for enemy in self.enemys:
                    enemy.move()
                    enemy.display()
                    enemy.bomb.display()
                    # if enemy.is_hited == True:
                    #     self.SCORES += 1
                self.player.display(self.enemys)
                font_over = pygame.font.Font("C:/Users/Rioron/PycharmProjects/untitled11/res/DENGB.TTF", 40)
                text_over = font_over.render("Scores: %d" % self.SCORES, 1, (0, 255, 0))
                self.window.blit(text_over, pygame.locals.Rect(320, 50, 226, 43))

                self.game_status = self.player.display(self.enemys)
                for bullet in self.player.bullets:
                    bullet.display()
                    bullet.move()
            elif self.game_status==2:            #如果发生碰撞，游戏结束
                font_over = pygame.font.Font("C:/Users/Rioron/PycharmProjects/untitled11/res/DENGB.TTF",40)
                                                #创建字体对象
                text_obj = font_over.render("GAME OVER",1,(255,0,0))
                self.window.blit(text_obj,pygame.locals.Rect(143,300,226,43))
            pygame.display.update()             #todo:反复刷新使窗体保持运行
            self.event_init()                   #不断获取事件


    def frame_init(self):           #TODO:游戏框架
        self.window = pygame.display.set_mode((Model.WINDOW_WIDTH,Model.WINDOW_HEIGHT))
        Model.window = self.window          #游戏窗体展示
        img_icon_o = pygame.image.load(img_icon)
        pygame.display.set_icon(img_icon_o)           #展示窗体图标
        pygame.display.set_caption("何祥琪出品")     #加上标题
        pass
    def model_init(self):               #游戏模型，加入窗体中的元素
        self.background = Background(img_bg,0,0)            #加入背景
        pygame.mixer.music.load(msc_bg)                        #加入背景音乐
        self.player = PlayerPlane(img_player,200,500)           #加入玩家飞机
        self.enemys = []
    def event_init(self):                       #事件
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                sys.exit()
            if event.type == pygame.locals.MOUSEMOTION and self.game_status == 1:        #监听玩家飞机移动事件
                pos = pygame.mouse.get_pos()        #获取坐标，返回值是元组
                self.player.x = pos[0]-35
                self.player.y = pos[1]-50
            if event.type == pygame.locals.KEYDOWN and self.game_status == 0:     #如果键盘发生按下事件

                if event.key == pygame.locals.K_1:     #=event.key == 49 如果按1键
                    self.game_level = 1
                elif event.key == pygame.locals.K_2:    #如果按2键
                    self.game_level = 2
                elif event.key == pygame.locals.K_3:
                    self.game_level = 3
                self.game_status = 1
                if self.game_level == 1:
                    for _ in range(5):
                        self.enemys.append(EnemyPlane())
                elif self.game_level == 2:
                    for _ in range(30):
                        self.enemys.append(EnemyPlane())
                elif self.game_level == 3:
                    for _ in range(100):
                        self.enemys.append(EnemyPlane())

        press = pygame.mouse.get_pressed()          #监听鼠标按下事件
        if press[0] == 1:
            pos = pygame.mouse.get_pos()
            bullet = Bullet(img_bullet,pos[0]+7,pos[1]-100)
            self.player.bullets.append(bullet)

if __name__=="__main__":
    Game().run()
