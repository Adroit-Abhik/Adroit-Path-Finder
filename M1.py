import pygame
import sys
from pygame.locals import *
import math


screen = pygame.display.set_mode((800, 800))
rows = 50
cols = 50
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (220, 220, 220)
w = 800 / cols
h = 800 / rows
openset = []
closedset = []
loop = True
pygame.init()


class Spot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.obs = False
        self.neighbours = []
        self.closed = False
        self.previous = None
        self.distance = 0

    def show(self, color, wt):
        if not self.closed:
            pygame.draw.rect(screen, color, (self.x * w, self.y * h, w, h), wt)
            pygame.display.update()

    def add_neighbours(self, grid):
        x = self.x
        y = self.y
        if x < cols-1 and grid[x + 1][y].obs == False:
            self.neighbours.append(grid[x + 1][y])
        if x > 0 and grid[x - 1][y].obs == False:
            self.neighbours.append(grid[x - 1][y])
        if y < rows - 1 and grid[x][y + 1].obs == False:
            self.neighbours.append(grid[x][y + 1])
        if y > 0 and grid[x][y - 1] == False:
            self.neighbours.append(grid[x][y - 1])


grid = [[Spot(i, j) for j in range(rows)] for i in range(cols)]
start = grid[1][1]
end = grid[48][48]
openset.append(start)

for i in range(cols):
    for j in range(rows):
        grid[i][j].show((255, 255, 255), 1)

for i in range(0,rows):
    grid[0][i].show(grey, 0)
    grid[0][i].obs = True
    grid[cols-1][i].obs = True
    grid[cols-1][i].show(grey, 0)
    grid[i][rows-1].show(grey, 0)
    grid[i][0].show(grey, 0)
    grid[i][0].obs = True
    grid[i][rows-1].obs = True



def mouse_press(x):
    t = x[0]
    w = x[1]
    g1 = t // (800 // cols)
    g2 = w // (800 // rows)
    access = grid[g1][g2]
    if access != start and access != end:
        if access.obs == False:
            access.obs = True
            access.show((255, 255, 255), 0)


end.show((255, 8, 127), 0)
start.show((255, 8, 127), 0)

flag = True
while flag:
    ev = pygame.event.get()
    for event in ev:
        if event.type == QUIT:
            pygame.quit()
        if pygame.mouse.get_pressed()[0]:
            try:
                pos = pygame.mouse.get_pos()
                mouse_press(pos)
            except AttributeError:
                pass
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                flag = False
                break

for i in range(cols):
    for j in range(rows):
        grid[i][j].add_neighbours(grid)


def heuristic(n, e):
    d = math.sqrt((n.x - e.x)**2 + (n.y - e.y)**2)
    return d


def main():
    end.show((255, 8, 127), 0)
    start.show((255, 8, 127), 0)

    while len(openset) > 0:
        lowest_index = 0
        for i in range(len(openset)):
            if openset[i].f < openset[lowest_index].f:
                lowest_index = i
        current = openset[lowest_index]
        openset.pop(lowest_index)
        closedset.append(current)

        if current == end:
            #print('done', current.f)
            start.show((255, 255, 0), 0)
            temp = current
            for i in range(round(current.f)):
                current.closed = False
                current.show((0,0,255), 0)
                current = current.previous
            end.show((255, 255, 0), 0)
            global loop
            loop = False
            break



        neighbours = current.neighbours
        for i in range(len(neighbours)):
            neighbour = neighbours[i]
            if neighbour not in closedset:
                tempg = current.g + 1

                if neighbour in openset:
                    if tempg < neighbour.g:
                        neighbour.g = tempg

                else:
                    neighbour.g = tempg

                    openset.append(neighbour)

            neighbour.h = heuristic(neighbour, end)
            neighbour.f = neighbour.g + neighbour.h

            if neighbour.previous == None:
                neighbour.previous = current
        for i in range(len(openset)):
            openset[i].show(green, 0)

        for i in range(len(closedset)):
            if closedset[i] != start:
                closedset[i].show(red, 0)

queue = []
path = []
for i in range(cols):
    for j in range(rows):
        if grid[i][j] != start:
            grid[i][j].distance = 99999999
        queue.append(grid[i][j])

def main2():
    while len(queue) > 0:
        lowest_index = 0
        for i in range(len(queue)):
            if queue[i].distance < queue[lowest_index].distance:
                lowest_index = i
        current = queue[lowest_index]

        queue.pop(lowest_index)
        if current == end:
            #print('done', current.f)
            start.show((255, 255, 0), 0)
            temp = current
            for i in range(round(current.distance)):
                current.show((0,0,255), 0)
                current = current.previous
            end.show((255, 255, 0), 0)
            global loop
            loop = False
            break

        neighbours = current.neighbours
        for i in range(len(neighbours)):
            neighbour = neighbours[i]
            alt = current.distance + heuristic(current, neighbour)
            if alt < neighbour.distance:
                neighbour.distance = alt
                if neighbour.previous == None:
                    neighbour.previous = current
            path.append(neighbour)


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    if loop:
        main2()




















