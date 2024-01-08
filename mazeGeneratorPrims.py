import pygame
import random 
import time

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1200, 600))
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
    
    def checkNeighborsAstar(self):
        neighbors = []
        top = grid[index(self.x,self.y-1)]
        right = grid[index(self.x+1,self.y)]
        left = grid[index(self.x-1,self.y)]
        bottom = grid[index(self.x,self.y+1)]

        if top and not top.walls[2]:
            neighbors.append(top)
        if right and not right.walls[3]:
            neighbors.append(right)
        if left and not left.walls[1]:
            neighbors.append(left)
        if bottom and not bottom.walls[0]:
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
    
    def heuristic(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)
    



def index(i,j):
    if i < 0 or j < 0 or i > cols - 1 or j > rows - 1:
        return -1
    return i + j * cols

for j in range(rows):
    for i in range(cols):
        cell = Cell(i,j)
        grid.append(cell)



def drawGrid():
    for cell in grid:
        cell.show()

def drawMazeFinal():
    for cell in grid:
        if cell.visited:
            cell.unhightlight()
        else:
            cell.highlight()
        cell.show()

def generate_maze():
    current = grid[0]
    current.visitedGrid()
    stack = []
    stack.append(current)
    while len(stack) > 0:
        current = stack.pop()
        current.visitedGrid()
        neighbors = current.checkNeighbors()
        if len(neighbors) > 0:
            stack.append(current)
            next = random.choice(neighbors)
            next.visitedGrid()
            stack.append(next)
            current.removeWalls(next)
    drawMazeFinal()
    pygame.display.flip()






def astar(start, end):
    openset =[(start, start.heuristic(end))]
    came_from = {}
    g_score = {start:start.heuristic(end)}

    while len(openset) > 0:
        # index of cell with lowest f_score
        index = openset.index(min(openset, key=lambda x: x[1]))
        current = openset.pop(index)[0]

        current.highlight()
        drawGrid()
        pygame.display.flip()
        if current == end:

            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            drawPath(path)
            pygame.display.flip()
            return path

        neighbors = current.checkNeighborsAstar()

        for neighbor in neighbors:
            if neighbor not in g_score:
                g_score[neighbor] = float('inf')
            else:
                continue

            if neighbor not in openset:
                openset.append((neighbor, neighbor.heuristic(end)))

            came_from[neighbor] = current
            g_score[neighbor] = g_score[neighbor] + neighbor.heuristic(end)

   

def getStartPoint():
    # using mouse position to get the start point
    start = None
    while start == None:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for cell in grid:
                    if cell.getPos() == (pos[0]//CELL_WIDTH,pos[1]//CELL_HEIGHT):
                        start = cell
                        start.drawStart()
                        pygame.display.flip()
                        break
    return start

def getEndPoint():
    # using mouse position to get the end point
    end = None
    while end == None:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for cell in grid:
                    if cell.getPos() == (pos[0]//CELL_WIDTH,pos[1]//CELL_HEIGHT):
                        end = cell
                        end.drawEnd()
                        pygame.display.flip()
                        break
    return end

def drawPath(path):
    for cell in path:

        cell.drawPath()
        drawGrid()
        pygame.display.flip()
       

    # prims algorithm for maze generation
generate_maze()
# get start point
start = getStartPoint()
# get end point
end = getEndPoint()

path = astar(start, end)


drawPath(path)
pygame.display.flip()




# pygame.quit()