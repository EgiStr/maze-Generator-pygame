import pygame
import random
import time

# maze Generator using Prims Algorithm 
# pygame setup
pygame.init()
screen = pygame.display.set_mode((801, 601))
clock = pygame.time.Clock()
running = True

CELL_WIDTH = 20
CELL_HEIGHT = 20
cols = screen.get_width() // CELL_WIDTH
rows = screen.get_height() // CELL_HEIGHT

grid = []


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = [True, True, True, True]
        self.visited = False

    def show(self):
        x = self.x * CELL_WIDTH
        y = self.y * CELL_HEIGHT
        if self.walls[0]:
            pygame.draw.line(screen, "white", (x, y), (x + CELL_WIDTH, y))
        if self.walls[1]:
            pygame.draw.line(screen, "white", (x + CELL_WIDTH, y), (x + CELL_WIDTH, y + CELL_HEIGHT))
        if self.walls[2]:
            pygame.draw.line(screen, "white", (x + CELL_WIDTH, y + CELL_HEIGHT), (x, y + CELL_HEIGHT))
        if self.walls[3]:
            pygame.draw.line(screen, "white", (x, y + CELL_HEIGHT), (x, y))

    def checkNeighbors(self):
        neighbors = []
        top = grid[index(self.x, self.y - 1)]
        right = grid[index(self.x + 1, self.y)]
        left = grid[index(self.x - 1, self.y)]
        bottom = grid[index(self.x, self.y + 1)]

        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if left and not left.visited:
            neighbors.append(left)
        if bottom and not bottom.visited:
            neighbors.append(bottom)

        return neighbors

    def removeWalls(self, other):
        x = self.x - other.x
        if x == 1:
            self.walls[3] = False
            other.walls[1] = False
        elif x == -1:
            self.walls[1] = False
            other.walls[3] = False

        y = self.y - other.y
        if y == 1:
            self.walls[0] = False
            other.walls[2] = False
        elif y == -1:
            self.walls[2] = False
            other.walls[0] = False

    def getPos(self):
        return (self.x, self.y)
    
    def highlight(self):
        x = self.x * CELL_WIDTH
        y = self.y * CELL_HEIGHT
        pygame.draw.rect(screen, "yellow", (x, y, CELL_WIDTH, CELL_HEIGHT))

    def visitedGrid(self):
        self.visited = True
        self.highlight()

    
def index(x, y):
    if x < 0 or y < 0 or x > cols - 1 or y > rows - 1:
        return None
    return x + y * cols


def removeWalls(a, b):
    x = a.x - b.x
    if x == 1:
        a.walls[3] = False
        b.walls[1] = False
    elif x == -1:
        a.walls[1] = False
        b.walls[3] = False

    y = a.y - b.y
    if y == 1:
        a.walls[0] = False
        b.walls[2] = False
    elif y == -1:
        a.walls[2] = False
        b.walls[0] = False


# create grid
for j in range(rows):
    for i in range(cols):
        cell = Cell(i, j)
        grid.append(cell)

# setup
current = grid[0]
stack = [current]

def primsAlorithm():
    global current, visited
    neighbors = current.checkNeighbors()
    if len(neighbors) > 0:
        next = random.choice(neighbors)
        stack.append(current)
        removeWalls(current, next)
        current = next
        current.visitedGrid()
        visited += 1
    elif len(stack) > 0:
        current = stack.pop()
        current.visitedGrid()
        visited += 1
# game loop
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")
    primsAlorithm()

    
    

    # draw grid
    for cell in grid:
        cell.show()

    # draw current cell
    current.highlight()

    pygame.display.update()

pygame.quit()

