# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#Libraries
import pygame
import sys

import information_panel
from bacteria import Bacteria
import random
import constants as const
import food
import information_panel as inform
import statistics as stat
import pandas as pd

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
    add_bac(bacteries, all_sprites)
    running = True

    time = 0  #счётчик шагов моделирования
    era = 0 #счётчик эпох (моментов сбора статистики)
    time_line = []

    speed_stats = [[const.parametrs[0], 'era period = ', const.era_period]]
    sense_stats = [[const.parametrs[0], 'era period = ', const.era_period]]
    size_stats = [[const.parametrs[0], 'era period = ', const.era_period]]

    df_stat = pd.DataFrame(columns=['time, tick', 'N bacteries', 'mean speed', 'deviation speed',
                                    'mean sens', 'deviation sens', 'mean size', 'deviation size'])

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = pause(bacteries, all_sprites, speed_stats, sense_stats, size_stats, era, df_stat) # пауза
                    print("RUNNING = ", running)


        #if time % const.spawn_time == 0:
        #    add_bac(bacteries, all_sprites)

        nearest_neighbours(bacteries, meals)

        # симуляционные события (размножение, питание, размножение)
        food_spawn(all_sprites, meals, time) # спавним еду
        eating(bacteries, meals)
        #bac_hunt(bacteries)
        checking_for_duplicate(all_sprites, bacteries) # проверяем не пора ли размножаться

        # сбор статистики
        if (time % const.era_period == 0):
            era += 1
            time_line.append(era*const.era_period)
            stat.collect_statistics(bacteries, speed_stats, sense_stats, size_stats, df_stat, era)

        time += 1
        time_render = const.font.render("Time: %d ticks" %(time), False, const.WHITE) # рендерим текст

        all_sprites.update() #
        screen.fill(bg_color) # прорисовка бэкграунда
        all_sprites.draw(screen) # прорисовка спрайтов
        screen.blit(time_render, (0, 0)) # прорисовка текста со временем симуляции
        if 1: # отрисовка круга чутья бактерии
            for bac in bacteries:
                pygame.draw.circle(const.screen, const.GRAY, bac.rect.center, bac.sensitive, 1)

        pygame.display.flip() #прорисовка последнего кадра
        if len(bacteries) == 0:
            running = False

    # вывод графиков, сохранение статистики
    stat.plot_line(1, df_stat['time, tick'], df_stat["N bacteries"], interactive= True) # график числа бактерий
    plot_histograms(speed_stats, sense_stats, size_stats, era, True)
    plot_boxplot(speed_stats, sense_stats, size_stats, False)

    # собираем всю информацию об изменениях параметров в один файл
    df_speed = pd.DataFrame(speed_stats)
    df_sense = pd.DataFrame(sense_stats)
    df_size = pd.DataFrame(size_stats)
    df_parameters = pd.concat([df_speed, df_sense, df_size])

    # выводим в эксель

    df_parameters.to_excel("output_parameters.xlsx")
    df_stat.to_excel("output_simulation_stat.xlsx")


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


def add_bac(bacteries, all_sprites):
    for i in range(const.N_bac):
        x = random.uniform(0, 1) * WIDTH
        y = random.uniform(0, 1) * HEIGHT
        bac = Bacteria(x, y)
        all_sprites.add(bac)
        bacteries.add(bac)

def bac_hunt(bacteries):
    for bac1 in bacteries:  # съедение бактерий
        hunt = pygame.sprite.spritecollide(bac1, bacteries, False)
        for bac_hunt in hunt:
            for bac in bacteries:
                if ((bac_hunt == bac) and (bac.size > (bac1.size*1.2))):
                    bac.energy += bac1.energy*0.4
                    bac1.kill()
                    print("Скушал малого")
                elif ((bac_hunt == bac) and ((bac.size*1.2) < bac1.size)):
                    bac1.energy += bac.energy*0.4
                    bac.kill()
def checking_for_duplicate(all_sprites, group): #смотрим кто готов размножаться и размножаем
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
                    neighbour_size = bac2.size
            bac1.neighbour[0][0] = min_distance1
            bac1.neighbour[1][0] = coord_x_target
            bac1.neighbour[2][0] = coord_y_target
            bac1.neighbour_size = neighbour_size #запоминаем размер ближайшей бакерии
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





def pause(bacteries, all_sprites, speed_stats, sense_stats, size_stats, era, df_stat): #пауза. Пробел - снять с паузы, p - поставить на паузу
    paused = True
    global running
    infos = pygame.sprite.Group()
    input_boxes = pygame.sprite.Group()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                paused = False

                return running
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False
                if event.key == pygame.K_h:
                    plot_histograms(speed_stats, sense_stats, size_stats, era, False)
                if event.key == pygame.K_b:
                    plot_boxplot(speed_stats, sense_stats, size_stats, False)
                if event.key == pygame.K_l:
                    stat.plot_line(1, df_stat['time, tick'], df_stat["N bacteries"], interactive=False)

                if event.key == pygame.K_s:
                    input_box_N_food = information_panel.InputBox(WIDTH/2-100, HEIGHT/2 - 50, 40, 20, 'N food: %d' %(const.N_food))
                    input_box_Food_spawn_time = information_panel.InputBox(WIDTH/2-100, HEIGHT/2 - 80, 40, 20, 'Food spawn time: %d' %(const.food_spawn_time))
                    input_box_mut_period = information_panel.InputBox(WIDTH/2-100, HEIGHT/2 - 120, 40, 20, 'Mutation period: %d' %(const.mutation_period))
                    input_box_Era = information_panel.InputBox(WIDTH/2-100, HEIGHT/2 - 160, 40, 20, 'Period of era: %d' %(const.era_period))
                    input_boxes.add(input_box_N_food, input_box_Food_spawn_time, input_box_mut_period, input_box_Era)

            if len(input_boxes) != 0:
                const.N_food = input_box_N_food.handle_event(event, const.N_food)
                input_box_N_food.text = 'N food: %d' %(const.N_food)
                const.food_spawn_time = input_box_Food_spawn_time.handle_event(event, const.food_spawn_time)
                input_box_Food_spawn_time.text = 'Food spawn time: %d' %(const.food_spawn_time)
                const.mutation_value = input_box_mut_period.handle_event(event, const.mutation_value)
                input_box_mut_period.text = 'Mutation period: %d' %(const.mutation_period)
                const.era_period = input_box_Era.handle_event(event, const.era_period)
                input_box_Era.text = 'Period of era: %d' %(const.era_period)

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


        if len(infos) != 0: # визуализируем текст
            for info in infos:
                info.vizualize_text(screen)

        if len(input_boxes) != 0:
            screen.fill(const.BLACK)
            all_sprites.draw(screen)
            for box in input_boxes:
                box.update()
                box.draw(screen)

        #pygame.display.update()
        pygame.display.flip()
        clock.tick(15)

    for info in infos: # удаляем плашки
        info.kill()
    for box in input_boxes:
        box.kill()
    return running

def plot_histograms(speed_stats, sense_stats, size_stats, era, interactive_status):
    stat.hist_stat(2, speed_stats, const.parametrs[0], 1, era)
    stat.hist_stat(3, sense_stats, const.parametrs[1], 1, era)
    stat.hist_stat(4, size_stats, const.parametrs[2], 1, era, interactive=interactive_status)

def plot_boxplot(speed_stats, sense_stats, size_stats, interactive_status):
    stat.boxplot(5, speed_stats, const.parametrs[0])
    stat.boxplot(6, sense_stats, const.parametrs[1])
    stat.boxplot(7, size_stats, const.parametrs[2], interactive=interactive_status)

def main():
    print('Hello! GAYS')
    run(const.N_bac)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    running = True
    main()
