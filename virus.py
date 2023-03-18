import pygame
import random
import constants as const

WIDTH = const.WIDTH
HEIGHT = const.HEIGHT
FPS = const.FPS

class Bacteriophage(pygame.sprite.Sprite):

    default_speed = const.default_virus_speed

    def __init__(self, screen, speed = const.default_speed):
        #инициализация бактерии
        pygame.sprite.Sprite.__init__(self) #инициализатор встроенных классов Sprite
        self.speed = const.default_speed
        self.infection_status = False
        self.status_alive = True

        self.screen = screen
        self.image = pygame.image.load('sprites/virus1.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect() # get_rect() оценивает изображение image и высчитывает прямоугольник, способный окружить его
        self.rect.center = (random.uniform(0, 1)*WIDTH, random.uniform(0, 1)*HEIGHT)

    def __del__(self): # деструктор
        print('Бактериофаг умер')

    def treatment(self): #выздоровление
        self.speed = self.speed
        self.image = pygame.image.load('sprites/bac_2.png')
        self.infection_status = False

    def infection(self): #заражение
        self.infection_status = True
        self.speed = self.default_speed_infection
        self.image = pygame.image.load('sprites/bac_inf.png')
        p = random.uniform(0, 1)
        print(p)
        if (p < 0.4):
            self.kill()

    def update(self):
        move = random.randrange(1, 6) #случайное движение по 4 направлениям
        if (1 == move):
            self.rect.x += self.speed
        elif (2 == move):
            self.rect.x -= self.speed
        elif (3 == move):
            self.rect.y += self.speed
        elif (4 == move):
            self.rect.y -= self.speed

        if True: #зацикленный мир
            if self.rect.left > WIDTH:
                self.rect.right = 0
            if self.rect.right < 0:
                self.rect.left = WIDTH
            if self.rect.top <0:
                self.rect.bottom = HEIGHT
            if self.rect.bottom > HEIGHT:
                self.rect.top = 0

            if (self.t > 0): #блок выздоровления. Если произошло заражение, включается таймер, когда он >300 - выздоровление
                self.t += 1
                if (self.t > 300):
                    self.treatment()
                    self.t = 0

            if ((self.rect.left > WIDTH/2) and (False == self.infection_status)):
                #тут происходит заражение, если бактерия в правой части экрана
                if random.uniform(0, 1) < 0.01:
                    self.t += 1
                    self.infection()



    def output(self):
        #вывод бактерии на экран
        self.screen.blit(self.image, self.rect)