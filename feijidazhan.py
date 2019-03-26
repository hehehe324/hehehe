import pygame
import pygame.locals
import sys
import random
import pygame.font

bg_img = "res/img_bg_level_5.jpg"
ico_img = "res/app.ico"
enm_img = ("res/img-plane_1 '.png","res/img-plane_2.png","res/img-plane_3.png","res/img-plane_4.png","res/img-plane_5.png","res/img-plane_6.png","res/img-plane_7.png")
plane_img = "res/hero.png"
bullet_img = "res/hero_bullet_7.png"
class Model():
    window = None
    WINDOW_HEIGHT = 768
    WINDOW_WIDTH = 512
    #todo:模型构造方法
    def __init__(self,img_path,x,y):
        self.img = pygame.image.load(img_path)
        self.x = x
        self.y = y
    #todo:模型展示方法
    def display(self):
        Model.window.blit(self.img,(self.x,self.y))
    #todo:碰撞操作
    @staticmethod
    def is_hit(rect1,rect2):
        return pygame.Rect.colliderect(rect1,rect2)

class Background(Model):
    def display(self):      #背景展示方法
        Model.window.blit(self.img,(self.x,self.y))
        Model.window.blit(self.img,(self.x,self.y-Model.WINDOW_HEIGHT))
    def Move(self):         #背景移动
        if self.y <= Model.WINDOW_HEIGHT:
            self.y += 1
        else:
            self.y = 0
    pass
    #todo:5:定义背景构造方法
class Bomb(Model):
    def __init__(self):
        self.x = None
        self.y = None
        self.imgs = [pygame.image.load("res/bomb-"+str(i)+".png") for i in range(1,7)]
        self.is_show = False
        self.times = 0

    def display(self):
        if self.is_show and self.times < len(self.imgs)*10:
            self.window.blit(self.imgs[self.times//10],(self.x,self.y))
            self.times += 1
        else:
            self.times = 0
            self.is_show = False

class PlayerPlane(Model):           #玩家飞机
    def __init__(self,img,x,y):         #初始化
        super().__init__(img,x,y)
        self.bullets = []
        # self.player_react = pygame.locals.Rect(self.x,self.y,120,78)

    def display(self,enemys):           #展示方法
        super().display()
        remove_bullets = []
        for bullet in self.bullets:
            # bullet.display()
            # bullet.move()
            bullet_react = pygame.locals.Rect(bullet.x, bullet.y, 20, 29)  # 子弹矩形
            if bullet.y < -29:
                remove_bullets.append(bullet)
            else:
                for enemy in enemys:
                    enemy_react = pygame.locals.Rect(enemy.x, enemy.y, 100, 68)
                    if Model.is_hit(bullet_react, enemy_react):
                        enemy.is_hited = True
                        enemy.bomb.is_show = True
                        enemy.bomb.x = enemy.x
                        enemy.bomb.y = enemy.y
                        # enemy.__init__()
                        enemy.bomb.display()
                        remove_bullets.append(bullet)
                        sound = pygame.mixer.Sound("C:/Users/Rioron/PycharmProjects/untitled11/res/bomb.wav")
                        sound.play()
                        break
        for bullet in remove_bullets:
            self.bullets.remove(bullet)
        player_react = pygame.locals.Rect(self.x, self.y, 120, 78)
        #todo:为什么定义为类属性和类变量结果不一样？？
        for enemy in enemys:
            enemy_react = pygame.locals.Rect(enemy.x,enemy.y,100,68)
            if Model.is_hit(player_react,enemy_react):
                enemy.is_hited = True
                pygame.mixer.music.load("C:/Users/Rioron/PycharmProjects/untitled11/res/gameover.wav")  # TODO 4.加载游戏背景音乐文件为游戏结束
                pygame.mixer.music.play(loops=1)
                return 2
        return 1

class Bullet(Model):
    def move(self):
        self.y -= 12

class EnemyPlane(Model):            #todo:敌机类
    #todo:构造方法
    def __init__(self):
        self.img = pygame.image.load(enm_img[random.randint(0,6)])
        self.x = random.randint(0,Model.WINDOW_WIDTH - 100)
        self.y = random.randint(-Model.WINDOW_HEIGHT,-68)
        # super().__init__(img_path,x,y)
        self.is_hited = False
        self.bomb = Bomb()
    #todo：移动方法
    def move(self):
        if self.y <= Model.WINDOW_HEIGHT and not self.is_hited:
            self.y += 4
        else:
            self.__init__()
    def display(self):
        super().display()
        if self.bomb.is_show:
            self.bomb.display()

class Game():
    #1.TODO:主程序入口
    def __init__(self):
        self.game_status = 1
    def run(self):
        pygame.init()
        pygame.mixer.init()
        self.frame_init()           #框架初始化
        self.model_init()           #模型初始化
        pygame.mixer.music.load("C:/Users/Rioron/PycharmProjects/untitled11/res/bg.wav")  # TODO 2.加载背景音乐文件
        pygame.mixer.music.play()
        while True:

            self.background.display()       #调用背景展示

            self.background.Move()      #调用背景移动

            if self.game_status == 0:
                font_over =  pygame.font.Font("res/DENGB.TTF",40)
                text_over = pygame.render("飞机大战",1,(255,255,0))
                self.window.blit(text_over,pygame.locals.Rect(256-45,300,226,43))

            elif self.game_status == 1:
                for enemy in self.enemys:       #敌机展示，移动
                    enemy.move()
                    enemy.display()
                    self.game_status=self.player.display(self.enemys)           #玩家飞机展示
                    for bullet in self.player.bullets:
                        bullet.display()
                        bullet.move()
            elif self.game_status == 2:
                font_over = pygame.font.Font("C:/Users/Rioron/PycharmProjects/untitled11/res/DENGB.TTF", 40)
                text_obj = font_over.render("GAMEOVER", 1, (255, 0, 0))
                self.window.blit(text_obj,pygame.locals.Rect(143, 300, 226, 43))
            self.player.display(self.enemys)
            pygame.display.update()     #窗体反复刷新
            self.event_init()           #事件监听

     #2.TODO:框架初始化
    def frame_init(self):
        self.window = pygame.display.set_mode((512,768))       #定义一个512*768的窗口
        Model.window = self.window

        img = pygame.image.load(ico_img)          #加载图标
        pygame.display.set_icon(img)
        pygame.display.set_caption("飞机大战")


    #3.TODO:模型初始化
    def model_init(self):
        self.background = Background(bg_img,0,0)  # TODO 5.初始化背景对象
        self.window.blit(self.background.img, (self.background.x, self.background.y))         #添加要显示的对象到窗体中显示

        self.enemys = []            #加入敌机

        for _ in range(5):
            self.enemys.append(EnemyPlane())         #敌机列表中创建敌机对象

        self.player = PlayerPlane(plane_img,200,200)       #创建玩家飞机对象
        self.player.bullets = []
    def event_init(self):                   #todo:4：监听事件
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                sys.exit()

            if event.type == pygame.locals.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                self.player.x = pos[0] - 120/2
                self.player.y = pos[1] -78/2+5

        mouse_state = pygame.mouse.get_pressed()        #获取鼠标按键状态
        if mouse_state[0] == 1:
            pos = pygame.mouse.get_pos()
            self.player.bullets.append(Bullet(bullet_img,pos[0]-20/2,pos[1]-29-40))     #创建子弹类实例
if __name__ == "__main__":
    Game().run()
