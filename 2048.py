import pygame
import random
from pygame.locals import *
from sys import exit

MAP_LEFT = 0
MAP_RIGHT = 1
MAP_UP = 2
MAP_DOWN = 3

PIXEL = 150
SIZE = 4

COLOR = [(255, 250, 240), (255, 239, 213), (255, 222, 173), (255, 215, 0), (255, 193, 37), (255, 185, 15), (238, 173, 14), (205, 149, 12)]

class Map_2048:

    def __init__(self, size):
        self.size = size
        self.score = 0
        self.rotation = MAP_LEFT
        self.map = [[0 for _ in range(size)] for _ in range(size)]
        for _ in range(random.randint(2, 3)):
            self.generate_new()

    def generate_new(self):
        new_element = random.randint(-1, 2)
        if new_element != 2:
            new_element = 1
        while True:
            x_pos = random.randint(0, self.size - 1)
            y_pos = random.randint(0, self.size - 1)
            if self.map[x_pos][y_pos] == 0:
                self.map[x_pos][y_pos] = new_element
                self.score += new_element
                break;
        
    def set_element(self, i, j, new_value):
        if self.rotation == MAP_LEFT:
            self.map[i][j] = new_value
        elif self.rotation == MAP_RIGHT:
            self.map[self.size - 1 - i][self.size - 1 - j] = new_value
        elif self.rotation == MAP_UP:
            self.map[j][self.size - 1 - i] = new_value
        elif self.rotation == MAP_DOWN:
            self.map[self.size - 1 - j][i]= new_value

    def get_element(self, i, j):
        if self.rotation == MAP_LEFT:
            return self.map[i][j]
        elif self.rotation == MAP_RIGHT:
            return self.map[self.size - 1 - i][self.size - 1 - j]
        elif self.rotation == MAP_UP:
            return self.map[j][self.size - 1 - i]
        elif self.rotation == MAP_DOWN:
            return self.map[self.size - 1 - j][i]
    
    def key_move(self):
        """assuming that we are moving to the left"""
        changed = False
        for i in range(self.size):
            current_row = []
            for j in range(self.size):
                if self.get_element(i, j) != 0:
                    current_row.append(self.get_element(i, j))
            current_row.append(0)
            
            j = 0
            new_row = []
            while j < len(current_row) - 1:
                if current_row[j] == current_row[j + 1]:
                    new_row.append(current_row[j] + 1)
                    j += 1
                else:
                    new_row.append(current_row[j])
                j += 1
                
            for j in range(len(new_row)):
                if self.get_element(i, j) != new_row[j]:
                    self.set_element(i, j, new_row[j])
                    changed = True
            for j in range(len(new_row), self.size):
                if self.get_element(i ,j) != 0:
                    self.set_element(i, j, 0)
                    changed = True
        return changed

    def is_over(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.map[i][j] == 0:
                    return False
        for i in range(self.size):
            for j in range(self.size - 1):
                if self.map[i][j] == self.map[i][j + 1]:
                    return False
        for i in range(self.size - 1):
            for j in range(self.size):
                if self.map[i][j] == self.map[i + 1][j]:
                    return False
        return True
                
    def move(self, symbol):
        self.rotation = symbol
        if self.key_move():
            self.generate_new()
  #      return self.is_over()

    def print_map(self):
        for i in range(self.size):
            print(self.map[i])

def get_color(map, i, j):
    if map.map[i][j] == 0:
        return (255, 255, 255)
    else:
        return COLOR[map.map[i][j] - 1]
    
def show(map, screen):
    for i in range(map.size):
        for j in range(map.size):
            # 背景颜色块
            pygame.draw.rect(screen, get_color(map, i, j), (PIXEL * j, PIXEL * i, PIXEL, PIXEL), 0)
            # 数值显示
            if map.map[i][j] != 0:
                map_text = map_font.render(str(2 ** map.map[i][j]), True, (106, 90, 205))
                text_rect = map_text.get_rect()
                text_rect.center = (PIXEL * j + PIXEL / 2, PIXEL * i + PIXEL / 2)
                screen.blit(map_text, text_rect)
    # 分数显示
#    screen.blit(score_block, (0, PIXEL * SIZE))
#    score_text = score_font.render((map.over() and "Game over with score " or "Score: ") + str(map.score), True, (106, 90, 205))
#    score_rect = score_text.get_rect()
#    score_rect.center = (PIXEL * SIZE / 2, PIXEL * SIZE + SCORE_PIXEL / 2)
#    screen.blit(score_text, score_rect)
    pygame.display.update()
            
pygame.init()
map = Map_2048(SIZE)

screen = pygame.display.set_mode((PIXEL * SIZE, PIXEL * SIZE))
pygame.display.set_caption("2048")

# 设置字体
map_font = pygame.font.Font(None, int(PIXEL * 2 / 3))
#score_font = pygame.font.Font(None, int(SCORE_PIXEL * 2 / 3))

show(map, screen)

while not map.is_over():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == KEYUP:
            if event.key == K_DOWN:
                map.move(MAP_DOWN)
            elif event.key == K_UP:
                map.move(MAP_UP)
            elif event.key == K_LEFT:
                map.move(MAP_LEFT)
            elif event.key == K_RIGHT:
                map.move(MAP_RIGHT)
            show(map, screen)
