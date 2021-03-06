import pygame
import random
from pygame.locals import *
from sys import exit

# markers for map_rotation
MAP_LEFT = 0
MAP_RIGHT = 1
MAP_UP = 2
MAP_DOWN = 3

PIXEL_SIZE   = 150  # dimension of blocks
MAP_SIZE     = 4    # number of blocks
SCORE_HEIGHT = 50   # scoreboard height

COLOR = [(255, 250, 240), (255, 239, 213), (255, 222, 173), (255, 215, 0), (255, 193, 37), (255, 185, 15), (238, 173, 14), (205, 149, 12)]

class Map_2048:

    def __init__(self, size):
        """
        size: the size of the map
        score: the score of the game
        rotation: the orientation of the map, which will be the "LEFT" direction in key_move()
        """
        self.size = size
        self.score = 0
        self.rotation = MAP_LEFT
        self.map = [[0 for _ in range(size)] for _ in range(size)]
        for _ in range(random.randint(2, 3)):
            self.generate_new()

    def __del__(self):
        del self.map

    def generate_new(self):
        """generate new elements in the map """
        # collect all blank positions
        blank_position = [(i, j)
                        for i in range(self.size)
                        for j in range(self.size)
                        if self.map[i][j] == 0]
        
        # if there is nowhere to add elements we return False
        if len(blank_position) == 0:
            return False

        # generate -1, 0, 1, 2 uniformly, here "-1, 0, 1" represents 1 while "2" represents 2
        new_element = random.randint(-1, 2)
        if new_element != 2:
            new_element = 1

        # generate a random blank position
        rand_pos = random.randint(0, len(blank_position) - 1)
        x_pos = blank_position[rand_pos][0]
        y_pos = blank_position[rand_pos][1]
        self.map[x_pos][y_pos] = new_element
        return True
        
    def set_element(self, i, j, new_value):
        """set the element value to new_value at (i, j) taken rotation into consideration"""
        if self.rotation == MAP_LEFT:
            self.map[i][j] = new_value
        elif self.rotation == MAP_RIGHT:
            self.map[self.size - 1 - i][self.size - 1 - j] = new_value
        elif self.rotation == MAP_UP:
            self.map[j][self.size - 1 - i] = new_value
        elif self.rotation == MAP_DOWN:
            self.map[self.size - 1 - j][i]= new_value

    def get_element(self, i, j):
        """get the element at (i, j) taken rotation into consideration"""
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

        # for each row
        for i in range(self.size):

            # collecting all nonzero blocks to current_row
            current_row = []
            for j in range(self.size):
                if self.get_element(i, j) != 0:
                    current_row.append(self.get_element(i, j))
            current_row.append(0)

            # combining consective identitical blocks, keep the result in new_row
            j = 0
            new_row = []
            while j < len(current_row) - 1:
                if current_row[j] == current_row[j + 1]:
                    new_row.append(current_row[j] + 1)
                    self.score += 2 ** (current_row[j] + 1)
                    j += 1
                else:
                    new_row.append(current_row[j])
                j += 1

            # rewrite the row[i] in the map using data from new_row
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
        """check if there is any possible move"""

        # check if there is any blank block
        for i in range(self.size):
            for j in range(self.size):
                if self.map[i][j] == 0:
                    return False

        # check if there is any consective identitical block horizontally
        for i in range(self.size):
            for j in range(self.size - 1):
                if self.map[i][j] == self.map[i][j + 1]:
                    return False
                
        # check if there is any consective identitical block vertically
        for i in range(self.size - 1):
            for j in range(self.size):
                if self.map[i][j] == self.map[i + 1][j]:
                    return False
        return True
                
    def move(self, symbol):
        """call the key_move() function"""
        self.rotation = symbol
        if self.key_move():
            self.generate_new()

    def print_map(self):
        """CUI output"""
        for i in range(self.size):
            print(self.map[i])
            
# end of class-definition

def get_color(map, i, j):
    if map.map[i][j] == 0:
        return (255, 255, 255)
    else:
        return COLOR[map.map[i][j] - 1]
    
def show(map, screen):
    for i in range(map.size):
        for j in range(map.size):
            # draw blocks for each block
            pygame.draw.rect(screen, get_color(map, i, j), (PIXEL_SIZE * j, SCORE_HEIGHT + PIXEL_SIZE * i, PIXEL_SIZE, PIXEL_SIZE), 0)
            # draw the numbers
            if map.map[i][j] != 0:
                number_text = number_font.render(str(2 ** map.map[i][j]), True, (106, 90, 205))
                text_rect = number_text.get_rect()
                text_rect.center = (PIXEL_SIZE * j + PIXEL_SIZE / 2, SCORE_HEIGHT + PIXEL_SIZE * i + PIXEL_SIZE / 2)
                screen.blit(number_text, text_rect)

    screen.blit(score_block, (0, 0))

    # draw scoreboard
    tip_text = tip_font.render(("Press 'r' to restart at any time; Press 'q' to QUIT! "), True, (106, 90, 205))
    tip_rect = tip_text.get_rect()
    tip_rect.center = (PIXEL_SIZE * MAP_SIZE / 2, SCORE_HEIGHT / 5)
    screen.blit(tip_text, tip_rect)
    
    # draw scoreboard
    if map.is_over():
        score_text = score_font.render(("Game Over! Your final score is ") + str(map.score), True, (106, 90, 205))
    else:
        score_text = score_font.render(("Score: ") + str(map.score), True, (106, 90, 205))
    score_rect = score_text.get_rect()
    score_rect.center = (PIXEL_SIZE * MAP_SIZE / 2, SCORE_HEIGHT * 7 / 10)
    screen.blit(score_text, score_rect)
    
    pygame.display.update()
            
pygame.init()
map = Map_2048(MAP_SIZE)

screen = pygame.display.set_mode((PIXEL_SIZE * MAP_SIZE, SCORE_HEIGHT + PIXEL_SIZE * MAP_SIZE))
pygame.display.set_caption("2048")

# score display block
score_block = pygame.Surface((PIXEL_SIZE * MAP_SIZE, SCORE_HEIGHT))
score_block.fill((245, 245, 245))

# set the font size for numbers in the map
number_font = pygame.font.Font(None, int(PIXEL_SIZE * 2 / 3))

# set the font size for the tip
tip_font = pygame.font.Font(None, int(SCORE_HEIGHT * 2 / 5))

# set the font size for the score
score_font = pygame.font.Font(None, int(SCORE_HEIGHT * 3 / 5))

show(map, screen)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == KEYUP:
            if event.key == K_q:
                pygame.quit()
                exit()
            elif event.key == K_DOWN:
                map.move(MAP_DOWN)
            elif event.key == K_UP:
                map.move(MAP_UP)
            elif event.key == K_LEFT:
                map.move(MAP_LEFT)
            elif event.key == K_RIGHT:
                map.move(MAP_RIGHT)
            elif event.key == K_r:
                del map
                map = Map_2048(MAP_SIZE)
            show(map, screen)
