import pygame
import random
import constants as const

WIDTH = const.WIDTH
HEIGHT = const.HEIGHT
FPS = const.FPS


class Glucose(pygame.sprite.Sprite):

    def __init__(self, screen):
        # инициализация бактерии
        pygame.sprite.Sprite.__init__(self)  # инициализатор встроенных классов Sprite
        #self.image = pygame.Surface((20, 20))
        #self.image.fill(const.YELLOW)
        self.image = pygame.image.load('sprites/eat.png')
        self.rect = self.image.get_rect()
        self.rect.center = (random.uniform(0, 1) * WIDTH, random.uniform(0, 1) * HEIGHT)

    def __del__(self):  # деструктор
        #print('Кто-то подкрепился')
        pass

    def output(self):
        # вывод еды на экран
        self.screen.blit(self.image, self.rect)