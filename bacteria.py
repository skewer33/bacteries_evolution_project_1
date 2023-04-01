import pygame
import random
import constants as const


WIDTH = const.WIDTH
HEIGHT = const.HEIGHT
FPS = const.FPS


class Bacteria(pygame.sprite.Sprite):

    default_energy = const.default_energy
    default_speed = const.default_speed
    default_sensitive = const.default_sensitive
    default_speed_infection = const.default_speed_infection
    default_size = const.default_size
    t = 0
    last_move = 0
    default_center = (random.uniform(0, 1) * WIDTH, random.uniform(0, 1) * HEIGHT)

    def __init__(self, x, y, energy = default_energy, speed = default_speed, sensitive = default_sensitive, size = default_size,
                 screen = const.screen):
        #инициализация бактерии
        pygame.sprite.Sprite.__init__(self) #инициализатор встроенных классов Sprite
        # эволюционные параметры
        self.speed = speed
        self.sensitive = sensitive
        self.size = size

        # чувствительность
        self.neighbour = [[WIDTH*WIDTH + HEIGHT*HEIGHT, WIDTH*WIDTH + HEIGHT*HEIGHT],
                          [-1, -1],
                          [-1, -1]] #первый столбик здесь - ближайшая бактерия. Второй - ближайшая еда
        # первая строка - расстояние до цели, вторая - её х координата, третья - её у координата
        # если появится разделение на больших и малых бактерий, добавить третий столбик
        self.prev_neighbour = [[WIDTH*WIDTH + HEIGHT*HEIGHT, WIDTH*WIDTH + HEIGHT*HEIGHT],
                          [-1, -1],
                          [-1, -1]] # структура - аналогично self.neighbour
        self.neighbour_size = 0


        #неэволюционные параметры
        self.infection_status = False
        self.status_alive = True
        self.status_father = False
        self.energy = energy
        self.lifetime = 0 #время жизни

        # расход энергии
        self.speed_energy = self.speed * self.speed / 4
        self.sensitive_energy = self.sensitive
        self.size_energy = self.size * self.size * self.size / 100

        # параметры вывода на экран
        self.screen = screen
        self.image = pygame.image.load('sprites/bac_1.png')
        self.image_orig = self.image  # оригинальное изображение. Нужно для поворотов
        self.image_orig = pygame.transform.scale(self.image_orig, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect() # get_rect() оценивает изображение image и высчитывает прямоугольник, способный окружить его
        self.rect.centerx = x
        self.rect.centery = y


    def __del__(self): # деструктор
        print('Бактерия умерла')

    def treatment(self): #выздоровление
        self.speed = self.speed
        self.image_orig = pygame.image.load('sprites/bac_2.png')
        self.infection_status = False

    def infection(self): #заражение
        self.infection_status = True
        self.speed = self.default_speed_infection
        self.image_orig = pygame.image.load('sprites/bac_inf.png')
        p = random.uniform(0, 1)
        if (p < const.danger):
            self.kill()

    def mutation(self): # мутация
        m = random.randrange(1, 4)
        if m == 1:
            self.speed += self.speed * const.mutation_value * random.uniform(-1, 1)
            self.speed_energy = self.speed * self.speed / 4
        if m == 2:
            self.sensitive += self.sensitive * const.mutation_value * random.uniform(-1, 1)
            self.sensitive_energy = self.sensitive
        if m == 3:
            self.size += self.size * const.mutation_value * random.uniform(-1, 1)
            self.size_energy = self.size * self.size * self.size / 100
            self.image = pygame.transform.scale(self.image_orig, (self.size, self.size))
            # границы параметров
            if (self.size <= 4):
                self.size = 4
            elif (self.size >= 90):
                self.size = 90

    def duplicate(self): # размножение
        self.status_father = True

    def rotation(self, angle): #поворот, нужен для движения
        self.image = pygame.transform.rotate(self.image_orig, angle)
        self.rect = self.image.get_rect(center = self.rect.center)

    def locator(self): #функция, распознающая объекты, попадающие в зону видимости, если таких нет,
        if self.neighbour[0][0] >= (self.sensitive * self.sensitive):
            self.neighbour[0][0] = -1
        if self.neighbour[0][1] >= (self.sensitive * self.sensitive):
            self.neighbour[0][1] = -1

    def move_to_target(self, objx, objy): # идти к цели
        dx = objx - self.rect.centerx
        dy = objy - self.rect.centery
        if(abs(dx) - abs(dy) > 0):
            if dx < 0:
                move = 5
            else:
                move = 2
        else:
            if dy < 0:
                move = 3
            else:
                move = 4
        return move

    def move_from_target(self, objx, objy): # убегать от цели, похожа на идти к цели, только движение в противоположном направлении
        dx = objx - self.rect.centerx
        dy = objy - self.rect.centery
        if abs(dx) - abs(dy) > 0:
            if dx < 0:
                move = 2
            else:
                move = 5
        else:
            if dy < 0:
                move = 4
            else:
                move = 3
        return move

    def moving_rules(self, move): # правила передвижения
        if (move > 5):
            move = self.last_move # в 6 случаях из 11 бактерия повторит предыдущее действие
        if (1 == move): # стоп
            self.rect.x += 0
        elif (2 == move): # вправо
            self.rotation(90)
            self.rect.x += self.speed
        elif (3 == move): # вниз
            self.rotation(90)
            self.rect.y -= self.speed
        elif (4 == move): # вверх
            self.rotation(-90)
            self.rect.y += self.speed
        elif (5 == move): # влево
            self.rotation(180)
            self.rect.x -= self.speed

    def cycle_world(self, WIDTH, HEIGHT): # зацикленный мир
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.top < 0:
            self.rect.bottom = HEIGHT
        if self.rect.bottom > HEIGHT:
            self.rect.top = 0

    def update(self):

        self.locator()
        if (self.neighbour[0][0] > 0) and (self.neighbour_size > (self.size*1.2)): #если бактерия больше на 20 процентов, её следует опасаться
            move = self.move_from_target(self.neighbour[1][0], self.neighbour[2][0])
        elif (self.neighbour[0][0] > 0) and (self.neighbour_size*1.2 <= self.size):
            move = self.move_to_target(self.neighbour[1][0], self.neighbour[2][0])
        elif (self.neighbour[0][1] > 0):
            move = self.move_to_target(self.neighbour[1][1], self.neighbour[2][1])
        else:
            move = random.randrange(1, 12) #случайное движение по 4 направлениям


        self.moving_rules(move) #движение бактерии
        self.last_move = move

        self.lifetime += 1 #время жизни

        self.energy -= self.size_energy + self.sensitive_energy + self.speed_energy
        if self.energy <= 0:
            self.kill()

        self.cycle_world(WIDTH, HEIGHT) # зацикленный мир

        # заражение и выздоровление
        if False: #
            if (self.t > 0): #блок выздоровления. Если произошло заражение, включается таймер, когда он >300 - выздоровление
                self.t += 1
                if (self.t > 300):
                    self.treatment()
                    self.t = 0

            if ((self.rect.left > WIDTH/2) and (False == self.infection_status)):
                #тут происходит заражение, если бактерия в правой части экрана
                if random.uniform(0, 1) < const.infectisity:
                    self.t += 1
                    self.infection() #

        if self.energy >= 0.8 * const.max_energy:
            self.duplicate() # размножение

        if self.lifetime % const.mutation_period == 1:
            self.mutation() # мутация


    def output(self):
        #вывод бактерии на экран
        self.screen.blit(self.image, self.rect)