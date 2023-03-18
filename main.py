# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#Libraries
import pygame
import sys
from bacteria import Bacteria
import random
import constants as const
import food
import information_panel as inform

#constants, если хотите их изменить, меняйте в файле "constants"
WIDTH = const.WIDTH  # ширина игрового окна
HEIGHT = const.HEIGHT  # высота игрового окна
FPS = const.FPS  # частота кадров в секунду
screen = const.screen
pygame.display.set_caption("Evolution Modeling")
clock = pygame.time.Clock()

# основная функция игры
def run(N_bac):
    pygame.init()
    pygame.font.init()  # вызов шрифтов, чтобы использовать текст
    bg_color = const.BLACK #цвет фона

    all_sprites = pygame.sprite.Group()
    bacteries = pygame.sprite.Group() # группа объектов типа бактерия
    meals = pygame.sprite.Group() # группа объектов типа еда
    #infos = pygame.sprite.Group() # группа информационных уведомлений
    for i in range(N_bac):
        x = random.uniform(0, 1) * WIDTH
        y = random.uniform(0, 1) * HEIGHT
        bac = Bacteria(x, y)
        all_sprites.add(bac)
        bacteries.add(bac)
    running = True

    time = 0  #счётчик шагов моделирования

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: pause(bacteries, all_sprites) # пауза

        time += 1
        time_render = const.font.render("Time: %d ticks" %(time), False, const.WHITE) # рендерим текст



        nearest_neighbours(bacteries, meals)
        all_sprites.update() #

        food_spawn(all_sprites, meals, time) # спавним еду
        eating(bacteries, meals)

        checking_for_johan_pohan(all_sprites, bacteries) # проверяем не пора ли размножаться



        screen.fill(bg_color) # прорисовка бэкграунда
        all_sprites.draw(screen) # прорисовка спрайтов
        screen.blit(time_render, (0, 0)) # прорисовка текста со временем симуляции
        if 1: # отрисовка круга чутья бактерии
            for bac in bacteries:
                pygame.draw.circle(const.screen, const.GRAY, bac.rect.center, bac.sensitive, 1)

        pygame.display.flip() #прорисовка последнего кадра

    pygame.quit()


def food_spawn(all_sprites, meals, time):
    if (time % (const.food_spawn_time) == 0):  # каждые 10 сек спавним новую еду
        for i in range(const.N_food):
            meal = food.Glucose(screen)
            all_sprites.add(meal)
            meals.add(meal)

def eating(bacteries, meals):
    breakfast = pygame.sprite.groupcollide(bacteries, meals, False, True)  # проверяем столкновение еды и бактерии
    for hit in breakfast:
        for bac in bacteries:
            if hit == bac:
                bac.image = pygame.image.load('sprites/bac_ate.png')
                bac.energy += const.food_value
                if bac.energy >= const.max_energy:
                    bac.energy = const.max_energy

def checking_for_johan_pohan(all_sprites, group): #смотрим кто готов размножаться и размножаем
    for bac in group:
        if bac.status_father == True:
            child = Bacteria(bac.rect.centerx, bac.rect.centery, energy = int(bac.energy/2), speed = bac.speed,
                             sensitive = bac.sensitive, size = bac.size)
            bac.energy = int(bac.energy/2 + 1) # делим энергию отца между ним и ребунком
            all_sprites.add(child)
            group.add(child)
            print("Я родился!")
            bac.status_father = False

def nearest_neighbours(bacteries, meals):

    for bac1 in bacteries:
        bac1.prev_neighbour = bac1.neighbour
        min_distance1 = WIDTH * WIDTH + HEIGHT * HEIGHT
        min_distance2 = WIDTH * WIDTH + HEIGHT * HEIGHT
        if len(bacteries) >1:
            for bac2 in bacteries:
                if bac2 == bac1:
                    continue
                dx = bac1.rect.centerx - bac2.rect.centerx
                dy = bac1.rect.centery - bac2.rect.centery
                dist = dx*dx+dy*dy
                if dist < min_distance1:
                    min_distance1 = dist
                    coord_x_target = bac2.rect.centerx
                    coord_y_target = bac2.rect.centery
            bac1.neighbour[0][0] = min_distance1
            bac1.neighbour[1][0] = coord_x_target
            bac1.neighbour[2][0] = coord_y_target
        else:
            bac1.neighbour[0][0] = WIDTH * WIDTH + HEIGHT * HEIGHT

        if len(meals) > 0:
            for meal in meals:
                dx = bac1.rect.centerx - meal.rect.centerx
                dy = bac1.rect.centery - meal.rect.centery
                dist = dx*dx+dy*dy
                if dist < min_distance2:
                    min_distance2 = dist
                    coord_x_target = meal.rect.centerx
                    coord_y_target = meal.rect.centery
            bac1.neighbour[0][1] = min_distance2
            bac1.neighbour[1][1] = coord_x_target
            bac1.neighbour[2][1] = coord_y_target
        else:
            bac1.neighbour[0][1] = WIDTH * WIDTH + HEIGHT * HEIGHT





def pause(bacteries, all_sprites): #пауза. Пробел - снять с паузы, p - поставить на паузу
    paused = True
    infos = pygame.sprite.Group()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos() # отслеживаем клик
                clicked_bacs = 0
                flag = False # флаг нужен для удаления инф плашки по второму клику, иначе бы на месте удалённой создавалась новая
                for bac in bacteries:
                    if bac.rect.collidepoint(pos): # если кликнули на бактерию, она она выделяется
                        clicked_bacs = bac

                for info in infos: # по клику на табличку, удаляем её
                    if info.rect.collidepoint(pos):
                        info.kill()
                        screen.fill(const.BLACK)
                        all_sprites.draw(screen)
                        pygame.display.flip()
                        flag = True

                if clicked_bacs != 0 and flag == False:  # блок вывода таблички с информацией о бактерии (нужна инициализация файла information_panel.py)
                    clicked_bacs.image = pygame.image.load('sprites/bac_4.png')
                    info = inform.Info_panel(clicked_bacs, screen)
                    all_sprites.add(info)
                    all_sprites.draw(screen)
                    infos.add(info)

        if infos != 0: # визуализируем текст
            for info in infos:
                info.vizualize_text(screen)

        pygame.display.update()
        clock.tick(15)

    for info in infos: # удаляем плашки
        info.kill()


def main():
    print('Hello! GAYS')
    run(const.N_bac)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
