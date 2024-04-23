import pygame 
import math
from queue import PriorityQueue #Ayuda a calcular el numero menor al estar en una matriz

WIDTH = 500 #alto de la ventana
WIN = pygame.display.set_mode((WIDTH, WIDTH)) #El tamaño de la ventana 
pygame.display.set_caption("Algoritmo a estrella")

ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 255, 0)
AMARILLO = (255, 255, 0)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
MORADO = (128, 0, 128)
NARANGA = (255, 165, 0)
GRIS = (128, 128, 128)
TURQUESA = (64, 224, 208)


class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.width = width
        self.total_rows = total_rows
        self.x = row * width
        self.y = col * width
        self.color = BLANCO
        self.neighbords = []

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        self.color = ROJO

    def is_open(self):
        self.color = VERDE

    def is_barrier(self):
        self.color = NEGRO

    def is_start(self):
        self.color = NARANGA

    def is_end(self):
        self.color = TURQUESA

    def reset(self):
        self.color = BLANCO

    def make_start(self):
        self.color = NARANGA
   
    def make_closed(self):
        self.color = ROJO

    def make_open(self):
        self.color =  VERDE

    def make_barrier(self):
        self.color = NEGRO

    def make_end(self):
        self.color = TURQUESA

    def make_path(self):
        self.color = MORADO

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbords(self, grid):
        self.neighbords = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbords.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbords.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbords.append(grid[self.row][self.col + 1 ])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbords.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def h(p1 , p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2) 


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbords:
            temp_g_score = g_score[current] + 1 

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GRIS, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GRIS, ( j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(BLANCO)
            
    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap 

    return row, col


def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if True:
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    print('botón izquierdo')
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, width)
                    spot = grid[row][col]

                    print(f'pos: {pos}\nrow: {row}\ncol:{col}\nspot:{spot}')
                    if not start and spot != end:
                        start = spot
                        start.make_start()

                    elif not end and spot != start:
                        end = spot
                        end.make_end()

                    elif spot != end and spot != start:
                        spot.make_barrier()

                elif pygame.mouse.get_pressed()[2]:
                    print('Boton derecho')
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, width)
                    spot = grid[row][col]
                    spot.reset()
                    if spot == start:
                        start = None
                    if spot == end:
                        end = None

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and start and end:
                        for row in grid:
                            for spot in row:
                                spot.update_neighbords(grid)

                            algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                        if event.key == pygame.K_c:
                            start = None
                            end = None
                            grid = make_grid(ROWS, width)

    pygame.quit()


main(WIN, WIDTH)
