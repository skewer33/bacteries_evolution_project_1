import pygame
import constants as const

pygame.init()
pygame.font.init()

class Info_panel(pygame.sprite.Sprite): #выводит табличку с характеристиками объекта

    def __init__(self, obj, screen):
        #инициализация бактерии
        pygame.sprite.Sprite.__init__(self) #инициализатор встроенных классов Sprite
        self.image = pygame.Surface((const.table_size_x, const.table_size_y))
        self.image.fill(const.GRAY)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()  # get_rect() оценивает изображение image и высчитывает прямоугольник, способный окружить его
        if obj.rect.centerx > const.WIDTH/2:   # размещаем плашку рядом с бактерией, но таким образом, чтоб она не выходила за экран
            if obj.rect.centery > const.HEIGHT/2:
                self.rect.centerx = obj.rect.centerx - const.table_size_x/2
                self.rect.centery = obj.rect.centery - const.table_size_y/2
            else:
                self.rect.centerx = obj.rect.centerx - const.table_size_x/2
                self.rect.centery = obj.rect.centery + const.table_size_y/2
        if obj.rect.centerx < const.WIDTH/2:
            if obj.rect.centery > const.HEIGHT/2:
                self.rect.centerx = obj.rect.centerx + const.table_size_x/2
                self.rect.centery = obj.rect.centery - const.table_size_y/2
            else:
                self.rect.centerx = obj.rect.centerx + const.table_size_x/2
                self.rect.centery = obj.rect.centery + const.table_size_y/2
        self.text = "Energy = % d\nLife time = %d\nSpeed = %d\nSensitive = %d\nSize = %d\nCoordinates =\n(%d, %d)\nNeighbour = %s" \
                    %(int(obj.energy), int(obj.lifetime), int(obj.speed), int(obj.sensitive), int(obj.size),
                      int(obj.rect.centerx), int(obj.rect.centery), str(obj.neighbour_size))

    def vizualize_text(self, screen):
        blit_text(screen, self.text, (self.rect.centerx - const.table_size_x/2+5, self.rect.centery - const.table_size_y/2 + 2))
    def __del__(self):  # деструктор
        print('ушла плашка')

    def output(self, screen):
        # вывод на экран
        self.screen.blit(self.image, self.rect, self.text)
        self.vizualize_text(screen)
    def update(self, screen):
        self.vizualize_text(screen)


def blit_text(surface, text, pos, font = const.font, color = const.WHITE): #для отображения многострочных текстов
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.