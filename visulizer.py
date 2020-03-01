# Libraries
import pygame
import random
from math import inf as infinity

# Modules
from settings import *  # All settings constants written in CAPS
from algorithms import astar, astar_diagonals, Dijkstra


# prints grid
def åäö(grid):
    for row in grid:
        print(row)


def create_grid(rows, cols):
    return [[0] * cols for i in range(rows)]


def draw_square(surface, color, x, y, width, height):
    pygame.draw.rect(surface, color, ((x, y), (width, height)), 0)


class Visualizer:
    def __init__(self, algorithm=None):
        pygame.init()
        self.width = WIDTH
        self.height = HEIGHT

        # Pygame
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Pathfinding Visualizer')
        self.clock = pygame.time.Clock()
        self.text_font_name = pygame.font.match_font(FONT_NAME)

        # Running variables
        self.running = True
        self.visualizing = False
        self.updating = False
        self.first = True

        self.algorithm = None
        self.maze = None
        self.start = None
        self.goal = None

        self.square = 30
        self.spot_colors = [WHITE, BLUE, BLUE, BLACK, RED, GREEN]
        self.rows = int(self.height / self.square)
        self.cols = int(self.width / self.square)
        self.grid = create_grid(self.rows, self.cols)

    def new(self):
        self.visualizing = True
        self.start_screen()

    # Startscreen where user can decide settings
    def start_screen(self):
        # Startskärmen
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.quit()

                if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    if self.algorithm is None:
                        self.algorithm = 'astar'
                    waiting = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        waiting = False
                        self.quit()

                    if event.key == pygame.K_c:
                        self.algorithm = None
                        self.maze = None

                    if event.key == pygame.K_i:
                        self.information_screen()

                    # PATHFINDING
                    if event.key == pygame.K_a:
                        self.algorithm = 'astar'

                    if event.key == pygame.K_b:
                        self.algorithm = 'astar_diagonals'

                    if event.key == pygame.K_d:
                        self.algorithm = 'dijkstra'
                    # MAZES
                    if event.key == pygame.K_1:
                        self.maze = 'DFS_RB'

            self.screen.fill(WHITE)
            self.draw_text('PATHFINDING VISUALIZER', 70, BLACK, WIDTH / 2, HEIGHT * 0.10)

            # Menu
            self.draw_text('Choose an algorithm by pressing corresponing number', 40, BLACK, WIDTH / 2, HEIGHT * 0.15)

            self.draw_text(str(self.algorithm) + ' | ' + str(self.maze), 35, GREEN, WIDTH / 2, HEIGHT * 0 * 35)
            self.draw_alternative('C: Clear options', WIDTH / 4, HEIGHT * 0.35)
            self.draw_alternative('I: Information page', WIDTH * 0.75, HEIGHT * 0.35)
            self.draw_text('Press space to start', 50, BLACK, WIDTH / 2, HEIGHT - (HEIGHT / 8))

            # Pathfinding
            self.draw_alternative('A: A* (Default)', WIDTH / 4, HEIGHT * 0.45)
            self.draw_alternative('B: A* Diagonals', WIDTH / 4, HEIGHT * 0.50)
            self.draw_alternative("D: Dijkstra's algorithm", WIDTH / 4, HEIGHT * 0.55)

            # Mazes
            self.draw_alternative('1: Depth-first Search Recursive Backtracker', WIDTH * 0.75, HEIGHT * 0.45)

            pygame.display.flip()

        self.run()

    def information_screen(self):
        # Startskärmen
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    waiting = False
                    self.quit()

                if event.type == pygame.KEYUP and event.key == pygame.K_m:
                    if self.algorithm is None:
                        self.algorithm = 'astar'
                    waiting = False

            self.screen.fill(WHITE)
            self.draw_text('Information Page', 70, BLACK, WIDTH / 2, HEIGHT * 0.10)

            # Menu
            self.draw_text('Press M or Escape to goto main menu', 40, BLACK, WIDTH / 2, HEIGHT * 0.20)

            self.draw_alternative('A* and A* Diagonal uses Euclidean distance as heuristic function', WIDTH / 2,
                                  HEIGHT * 0.35)
            self.draw_alternative('Dijkstra finishes completely to ensure optimal path', WIDTH / 2,
                                  HEIGHT * 0.40)

            pygame.display.flip()

    def run(self):
        # Visualizing loop
        while self.visualizing:
            self.clock.tick(FPS)
            self.events()
            if self.updating:
                self.update()
            self.draw()

    def quit(self):
        self.running = False
        self.visualizing = False  # if self.visualizing else True

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            # Button presses
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    self.quit()

                if event.key == pygame.K_SPACE:
                    self.updating = True

                if event.key == pygame.K_m:
                    self.updating = False
                    self.new()
                # Place start
                if not self.updating:
                    try:

                        if event.key in [pygame.K_s, pygame.K_g]:
                            pos = pygame.mouse.get_pos()
                            row, col = int(pos[0] / self.square), int(pos[1] / self.square)
                            # Set start
                            if event.key == pygame.K_s:
                                if self.start is not None:
                                    # Removes Old
                                    startcol = self.start[0]
                                    startrow = self.start[1]
                                    self.grid[startcol][startrow] = 0
                                # Places new
                                self.start = (col, row)
                                self.grid[col][row] = 1

                            # Set goal
                            if event.key == pygame.K_g:
                                if self.goal is not None:
                                    # Removes Old
                                    goalcol = self.goal[0]
                                    goalrow = self.goal[1]
                                    self.grid[goalcol][goalrow] = 0
                                # Places new
                                self.goal = (col, row)
                                self.grid[col][row] = 2

                    except IndexError:
                        print('Location out of bounds')

                    if event.key == pygame.K_r:
                        for i in range(len(self.grid)):
                            for j in range(len(self.grid[i])):
                                if random.random() < RANDOM_PROBABILITY and self.grid[i][j] not in [1, 2]:
                                    self.grid[i][j] = 3

            # Mousebutton
            try:
                # Drawing walls
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    row, col = (int(pos[0] / self.square), int(pos[1] / self.square))  # Grid coordinates
                    self.grid[col][row] = 3

                # Removing nodes
                if pygame.mouse.get_pressed()[2]:
                    pos = pygame.mouse.get_pos()
                    row, col = (int(pos[0] / self.square), int(pos[1] / self.square))  # Grid coordinates
                    self.grid[col][row] = 0

            except IndexError:
                print('Location out of bounds')

    # The algorithm
    def update(self):

        if self.algorithm in ['astar', 'astar_diagonals']:
            if self.algorithm == 'astar':
                algorithm = astar.A_Star

            if self.algorithm == 'astar_diagonals':
                algorithm = astar_diagonals.A_Star

            if self.first:
                a = algorithm(self.grid, self.start, self.goal, astar.distance)
                self.args = a[2:]
                self.first = False

            else:
                a = algorithm(self.grid, self.start, self.goal, astar.distance, self.args)
                if a == -1:
                    self.updating = False

                elif a[0] == 0:
                    self.updating = False
                    self.path = a[1]

                elif a[0] == 1:
                    self.args = a[2:]
                    self.path = a[1]

                open_set = a[2]
                closed_set = a[3]



                for x, y in closed_set:
                    self.grid[x][y] = 4

                for x, y in open_set:
                    self.grid[x][y] = 5

                for x, y in self.path:
                    self.grid[x][y] = 1



        if self.algorithm == 'dijkstra':
            print(0)
            if self.first:
                return_code, self.path, self.args = Dijkstra.dijkstra(self.grid, self.start, self.goal, astar.distance)
                self.first = False

            else:
                return_code, self.path, self.args = Dijkstra.dijkstra(self.grid, self.start, self.goal,
                                                                      Dijkstra.distance, self.args)

                if return_code == -1:
                    self.updating = False
                    self.path = []
                    for i in range(len(self.grid)):
                        for j in range(len(self.grid[i])):
                            if self.grid[i][j] == 5:
                                self.grid[i][j] = 4


                elif return_code == 0:
                    self.updating = False
                    for i in range(len(self.grid)):
                        for j in range(len(self.grid[i])):
                            if self.grid[i][j] in [1, 2]:
                                self.grid[i][j] = 0

                unvisited = self.args[0]

                if return_code == 0:
                    color = 1

                else:
                    color = 5

                for x, y in self.path:
                    self.grid[x][y] = color

                self.grid[self.goal[0]][self.goal[1]] = 2
                self.grid[self.start[0]][self.start[1]] = 1

    def draw_alternative(self, text, x, y):
        self.draw_text(text, 30, BLACK, x, y)

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.text_font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw(self):
        self.screen.fill(WHITE)
        # Fill spots
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] != 0:
                    draw_square(self.screen, self.spot_colors[self.grid[i][j]], self.square * j, self.square * i,
                                self.square, self.square)

        # Horizontal
        for i in range(self.rows + 1):
            pygame.draw.line(self.screen, BLACK, (0, i * self.square),
                             (self.width - self.width % self.square, i * self.square), 1)

        # Vertical
        for i in range(self.cols + 1):
            pygame.draw.line(self.screen, BLACK, (i * self.square, 0),
                             (i * self.square, self.height - self.height % self.square), 1)

        # Flip the drawn image
        pygame.display.flip()


v = Visualizer()
print('Starting..')
while v.running:
    v.new()


åäö(v.grid)
print('Exiting Program...')
pygame.quit()
