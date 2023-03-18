import pygame
pygame.init()
pygame.font.init()

#global constants
WIDTH = 1200  # ширина игрового окна
HEIGHT = 800  # высота игрового окна
FPS = 20  # частота кадров в секунду

screen = pygame.display.set_mode((WIDTH, HEIGHT))
# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (75, 75, 75)

#info window
alpha = 0.5 # коэф сдвига информационного окна относительно бактерий
table_size_x, table_size_y = 125, 125

    #text for inform table
text = "This is a really long sentence with a couple of breaks.\nSometimes it will break even if there isn't a break " \
       "in the sentence, but that's because the text is too long to fit the screen.\nIt can look strange sometimes.\n" \
       "This function doesn't check if the text is too high to fit on the height of the surface though, so sometimes " \
       "text will disappear underneath the surface"
font = pygame.font.SysFont('Calibri', 16)

#parameters of modelling
#food
N_food = 30
food_spawn_time = 50
food_value = 15000

#bacteria
N_bac = 30
default_energy = 150000
max_energy = default_energy * 2
spawn_time = 300
mutation_period = 50
mutation_value = 0.4

default_sensitive = 50
default_speed = 10
default_speed_infection = 5
default_size = 20

#virus
default_virus_speed = 20
danger = 0.01
infectisity = 0.2