from random import *
import pygame
import sys




# READY TO IMPLEMENT


#---CLASSES---AND---FUNCTIONS----------------------------------------------------------------------------


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    def contains(self, point):
        return (point.x >= self.x) and (point.x < self.x + self.w) and (point.y >= self.y) and (point.y <= self.y + self.h) 
    
    def intersects(self, range):
        left = self.x
        right = self.x + self.w
        top = self.y + self.h
        bottom = self.y
        oleft = range.x
        oright = range.x + range.w
        otop = range.y + range.h
        obottom = range.y
        return (left <= oright or right >= oleft or top >= obottom or bottom <= otop) 
    

class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def contains(self, point):
        d = (point.x - self.x) * (point.x - self.x) + (point.y - self.y) * (point.y - self.y)
        return d <= self.radius ^ 2
    
    def intersects(self, range):
        xDist = abs(range.x - self.x)
        yDist = abs(range.y - self.y)

        r = self.radius

        w = range.w
        h = range.h

        edges = (xDist - w) * (xDist - w) + (yDist - h) * (yDist - h)

        if xDist > r + w or yDist > r + h:
            return False
        
        if xDist <= w or yDist <= h:
            return True
        
        return edges <= self.radius ^ 2


class QuadTree:
    def __init__(self, boundary, n):
        self.boundary = boundary
        self.capacity = n
        self.points = []
        self.divided = False

    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h
        ne = Rectangle(x + w / 2,  y +  h / 2, w / 2, h / 2)
        self.northeast = QuadTree(ne, self.capacity)
        nw = Rectangle(x, y + h / 2, w / 2, h / 2)
        self.northwest = QuadTree(nw, self.capacity)
        se = Rectangle(x + w / 2, y, w / 2, h / 2)
        self.southeast = QuadTree(se, self.capacity) 
        sw = Rectangle(x, y, w / 2, h / 2)
        self.southwest = QuadTree(sw, self.capacity)
        self.divided = True
        
    
    def insert(self, point):
        if not self.boundary.contains(point):
            return False

        if len(self.points) < self.capacity and not self.divided:
            self.points.append(point)
            return True
        else:
            if not self.divided:
                self.subdivide()

            if self.northeast.insert(point):
                return True
            elif self.northwest.insert(point):
                return True
            elif self.southeast.insert(point):
                return True
            elif self.southwest.insert(point):
                return True
    

    def query(self, range, found = []):

        
        if not range.intersects(self.boundary):
            return 
        else:
            for p in self.points:
                if range.contains(p):
                    found.append(p)
            if self.divided:
                self.northwest.query(range, found)
                self.northeast.query(range, found)
                self.southeast.query(range, found)
                self.southwest.query(range, found)
                    
        return found


    def show(self, window):
        pygame.draw.rect(window, "white", pygame.Rect(self.boundary.x, self.boundary.y, self.boundary.w, self.boundary.h), 1)
        for p in self.points:
            pygame.draw.circle(window, "white", (p.x, p.y), 1, 0)
        if self.divided:
            self.northeast.show(window)
            self.northwest.show(window)
            self.southeast.show(window)
            self.southwest.show(window)
        
        

#----------SETUP---------------------------------------------------------------------

width = 1000
height = 1000
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
# fps = clock.get_fps()

boundary = Rectangle(0, 0, width, height)
tree = QuadTree(boundary, 2)


rangeS = Rectangle(100, 100, 100, 100)


def setup():
    # pass
    for i in range(1000):
        p = Point(gauss(width / 2, width / 8), gauss(height / 2, height / 8))
        tree.insert(p)

def draw():
    screen.fill("black")

    tree.show(screen)

    
    points = []
    tree.query(rangeS, points)

    x,y = pygame.mouse.get_pos()
    # p = Point(x, y)
    # tree.insert(p)

    for p in points:
        pygame.draw.circle(screen, "green", (p.x, p.y), 1, 1)

    pygame.draw.rect(screen, "green", pygame.Rect(rangeS.x, rangeS.y, rangeS.w, rangeS.w), 1)
    print(len(points))

    

    pygame.display.flip()

setup()
draw() 

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                # p = Point(x, y)
                # tree.insert(p)
                rangeS = Rectangle(x, y, 100, 100)
                    
    draw()


pygame.quit()
