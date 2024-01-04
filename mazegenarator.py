import pygame
import random 
import time

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
    def __init__(self,x,y):
        self.x=x
        self.y = y
        self.walls = [True,True,True,True]
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
        top = grid[index(self.x,self.y-1)]
        right = grid[index(self.x+1,self.y)]
        left = grid[index(self.x-1,self.y)]
        bottom = grid[index(self.x,self.y+1)]

        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if left and not left.visited:
            neighbors.append(left)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        
        return neighbors
    
    def removeWalls(self,other):
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
        return (self.x,self.y)
    
    def visitedGrid(self):
        self.visited = True
        self.highlight()

    def highlight(self):
        x = self.x * CELL_WIDTH
        y = self.y * CELL_HEIGHT
        pygame.draw.rect(screen,"red",(x,y,CELL_WIDTH,CELL_HEIGHT))

    def unhightlight(self):
        x = self.x * CELL_WIDTH
        y = self.y * CELL_HEIGHT
        pygame.draw.rect(screen,"green",(x,y,CELL_WIDTH,CELL_HEIGHT))
  
    def drawPath(self):
        x = self.x * CELL_WIDTH
        y = self.y * CELL_HEIGHT
        pygame.draw.rect(screen,"blue",(x,y,CELL_WIDTH,CELL_HEIGHT))
    
    def drawStart(self):
        x = self.x * CELL_WIDTH
        y = self.y * CELL_HEIGHT
        pygame.draw.rect(screen,"yellow",(x,y,CELL_WIDTH,CELL_HEIGHT))
    
    def drawEnd(self):
        x = self.x * CELL_WIDTH
        y = self.y * CELL_HEIGHT
        pygame.draw.rect(screen,"orange",(x,y,CELL_WIDTH,CELL_HEIGHT))


def index(i,j):
    if i < 0 or j < 0 or i > cols - 1 or j > rows - 1:
        return -1
    return i + j * cols

for j in range(rows):
    for i in range(cols):
        cell = Cell(i,j)
        grid.append(cell)



start = random.choice(grid)
end = random.choice(grid)
stack = [start]


    

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE
    clock.tick(24)  # limits FPS to 60
    
    for cell in grid:
        cell.show()
  
    

    while len(stack)>0:
        current = stack.pop()
        if current.visited == False:
            current.visitedGrid()
            pygame.display.flip()
            if len(stack)>1:
                next = stack[-1]
                current.removeWalls(next)
                pygame.display.flip()

            for cell in grid:
                if cell.visited == True:
                    cell.unhightlight()
                cell.show()

            pygame.display.flip()
            # shuffle the neighbors
            neighbors = current.checkNeighbors()
            random.shuffle(neighbors)
            for neighbor in neighbors:
                stack.append(current)
                stack.append(neighbor)

    start.drawStart()
    end.drawEnd()

    # restart visited grid
    for cell in grid:
        cell.visited = False
    
    # find path
    path = []
    path.append(start)

    print(start.walls)
    pygame.display.flip()


    # update the display
    pygame.display.flip()

    



     




pygame.quit()