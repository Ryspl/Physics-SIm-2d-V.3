#physics v3

# real world constants -------------------------------------DONE
# object classes -------------------------------------------DONE (BALL)
# fixed points and objects----------------------------------
# implment equations (collisions, gravity, loss of energy)--DONE
# sub-stepping (optimnalisation)----------------------------MOSTLY >>> QUADTREE.PY IMPLEMENTSTION FAIL
# springs---------------------------------------------------
# fabric sim test??-----------------------------------------
# ball spin and sqare spin collisin handler ----------------


import pyglet 
import math
from random import *
import Quadtree as qt



#canvas setup -----------------------------------------------------------------

simWidth = 1000
simHeight = 1000
window = pyglet.window.Window(simWidth, simHeight)
batch = pyglet.graphics.Batch()


# vector math --------------------------------------------------------------

class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def set(v, self):
        self.x = v.x
        self.y = v.y
    
    def clone(self):
        return Vector(self.x, self.y)

    def add(self, v, s = 1.0):
        self.x += v.x * s
        self.y += v.y * s
        return self
    
    def add_vectors(self, a, b):
        self.x += a.x + b.x
        self.y += a.y + b.y
        return self
    
    def substract(self, v, s = 1.0):
        self.x -= v.x * s
        self.y -= v.y * s
        return self

    def sub_vectors(self, a, b):
        self.x -= a.x - b.x
        self.y -= a.y - b.y
        return self
    
    def lenght(self):
        return math.sqrt(self.x * self.x + self.y * self.y)
    
    def scale(self, s):
        self.x *= s
        self.y *= s
    
    def dot(self, v):
        return self.x * v.x + self.y * v.y
    


# objects------------------------------------------------------------------------
class Ball:

    def __init__(self, radius, mass, pos, vel, color, fixed = False, collided = False):  # +velang
        self.radius = radius
        self.pos = pos.clone()
        self.vel = vel.clone()
        # self.velang = velang.clone()
        self.mass = mass
        self.color = color
        self.fixed = fixed
        self.circle = pyglet.shapes.Circle(x= self.pos.x, y= self.pos.y, radius= self.radius, color= self.color, batch=batch)
        # self.moment_of_inertia = 0.5 * self.mass * self.radius * self.radius
        # self.lines = pyglet.shapes.Line(x=self.pos.x, y=self.pos.y, x2=self.pos.x, y2=self.pos.y - self.radius, width=3, color=(255, 255, 255), batch=batch)
    
    def sim(self, dt):
        if not self.fixed:
            self.vel.add(gravity, dt)
            self.pos.add(self.vel, dt)

    def intersects(self, other):
        d = math.dist((self.pos.x, self.pos.y), (other.pos.x, other.pos.y))
        return d < self.radius + other.radius



# collision handler ----------------------------------------------------------------------------------------

def handleBallCollision(ball1, ball2):
    
    dirr = Vector(0, 0)
    dirr.sub_vectors(ball1.pos, ball2.pos)
    d = dirr.lenght()
    if d==0 or d > ball1.radius + ball2.radius:
        return


    dirr.scale(1.0/d)

    corr = (ball1.radius + ball2.radius - d) / 2.0
    ball1.pos.add(dirr, -corr)
    ball2.pos.add(dirr, corr)

    v1 = ball1.vel.dot(dirr)
    v2 = ball2.vel.dot(dirr)
    

    m1 = ball1.mass
    m2 = ball2.mass 

    newV1 = (m1 * v1 + m2* v2 - m2 * (v1 - v2) * resstribution) / (m1 + m2)
    newV2 = (m1 * v1 + m2* v2 - m1 * (v2 - v1) * resstribution) / (m1 + m2)
    
    ball1.vel.add(dirr, newV1 - v1)
    ball2.vel.add(dirr, newV2 - v2)


def handleWallCollision(ball):

    if ball.pos.x < ball.radius:
        ball.pos.x = ball.radius
        ball.vel.x = -ball.vel.x * resstribution

    if ball.pos.x > simWidth - ball.radius:
        ball.pos.x = simWidth - ball.radius
        ball.vel.x = -ball.vel.x * resstribution
    
    if ball.pos.y < ball.radius:
        ball.pos.y = ball.radius
        ball.vel.y = -ball.vel.y * resstribution

    if ball.pos.y > simHeight - ball.radius:
        ball.pos.y = simHeight - ball.radius
        ball.vel.y = -ball.vel.y * resstribution

#vars -------------------------------------------------------------------------

fps_display = pyglet.window.FPSDisplay(window= window)
gravity = Vector(0.0, 0.0)
timestep = 1.0 / 60.0
resstribution = 1 # 1 - elastic, 0 - inelastic
paused = False
balls = []
ileKul = 10



#ball simulation---------------------------------------------------------------------

def simulate(dt, qtree):
     for i in range(len(balls)):
        ball1 = balls[i]
        ball1.sim(dt)

        rangeS = qt.Circle(ball1.pos.x, ball1.pos.y, ball1.radius * 2)
        points = qtree.query(rangeS)
        for point in points:
            ball2 = balls[point.refrence]
            handleBallCollision(ball1, ball2)

        handleWallCollision(ball1)


#Quadtree Setup --------------------------------------------------------------

def setup():

    boundary = qt.Rectangle(0, 0, simWidth, simHeight)
    qtree = qt.QuadTree(boundary, 4)

    for ball in balls:
        point = qt.Point(ball.pos.x, ball.pos.y, balls.index(ball))
        qtree.insert(point)  
    return qtree




# physics sim ---------------------------------------------------------------------

def addBalls():

    for i in range(ileKul):
        radius = 5 #+ randrange(10, 50)
        mass = math.pi * radius #* radius
        pos = Vector(random() * simWidth, random() * simHeight) #random() * simWidth, random() * simHeight
        vel = Vector(-1.0 + 2.0 * randrange(-50, 50), -1.0 + 2.0 * randrange(-50, 50)) # -1.0 + 2.0 * randrange(10, 50), -1.0 + 2.0 * randrange(10, 50)
        # velang = Vector(0, 0)
        color = [randint(0,255), randint(0,255), randint(0,255)]

        balls.append(Ball(radius, mass, pos, vel, color, False, False))


#canvas drawing module ---------------------------------------------------------
def draw():
    window.clear()
    fps_display.draw()

    for i in range(len(balls)):
        ball = balls[i]
        ball.circle.x = ball.pos.x
        ball.circle.y = ball.pos.y

        ball.circle.color = ball.color

        
    batch.draw()

# app runnning proccess ------------------------------------------------------------------------

### add balls wih click
@window.event
def on_mouse_press(x,y, buttons, modifiers):
    if buttons and pyglet.window.mouse.LEFT:
        addBalls()


@window.event
def on_draw():
    qtree = setup()
    simulate(timestep, qtree)
    draw()

    

# def update(dt):
#     qtree = setup()
#     simulate(dt, qtree)
#     draw()


addBalls()
# update(timestep)


# pyglet.clock.schedule_interval(update, timestep)
pyglet.app.run()