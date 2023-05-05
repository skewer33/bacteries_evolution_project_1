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


class InputBox(pygame.sprite.Sprite):

    def __init__(self, x, y, w, h, text, text_input=''):
        pygame.sprite.Sprite.__init__(self)
        #self.image =

        #self.image.fill(const.GRAY)
        self.rect = pygame.Rect(x+200, y, w, h)
        self.color = const.LIGHT_GRAY
        self.text = text
        self.text_input = text_input
        self.txt_surface = const.font.render(text_input, True, self.color)
        self.txt_surface_static = const.font.render(self.text, True, self.color)
        self.active = False


    def handle_event(self, event, parameter):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.

            self.color = const.YELLOW if self.active else const.LIGHT_GRAY
            print(self.active)

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    parameter = int(self.text_input)
                    print(self.text_input)
                    self.text_input = ''

                elif event.key == pygame.K_BACKSPACE:
                    self.text_input = self.text_input[:-1]
                else:
                    self.text_input += event.unicode
                # Re-render the text.
                self.txt_surface = const.font.render(self.text_input, True, self.color)
        return parameter

    def update(self):
        # Resize the box if the text is too long.
        self.txt_surface_static = const.font.render(self.text, True, self.color)
        width = max(40, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface_static, (self.rect.x - 150, self.rect.y + 5))
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


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