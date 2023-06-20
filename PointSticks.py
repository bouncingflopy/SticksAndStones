import pygame as pg
import math
import numpy as np
import time
import random

points = []
sticks = []
gravity = 1
pointSize = 5
stickWidth = 3
iterations = 5
deltaTime = 0.1
bounce = 0.4

class Point:
    def __init__(self, x, y, locked):
        self.position = [x, y]
        self.prevPosition = self.position
        self.locked = locked
        self.color = (3, 161, 252)

    def Lock(self):
        self.locked = True
        self.color = (252, 78, 3)

    def Unlock(self):
        self.locked = False
        self.color = (3, 161, 252)

class Stick:
    color = (87, 56, 34)

    def __init__(self, pointA, pointB):
        self.pointA = pointA
        self.pointB = pointB
        self.length = math.sqrt((self.pointA.position[0] - self.pointB.position[0]) ** 2 + (self.pointA.position[1] - self.pointB.position[1]) ** 2)

def ScreenInit():
    pg.init()
    fps = 30
    width = 720
    height = 720
    screen = pg.display.set_mode((width, height))
    pg.display.set_caption("Point Sticks Simulation")
    screen.fill((84, 94, 110))
    return screen

def Change(position, other, offsetX, offsetY):
    final = position
    if final[0] > other[0]:
        final[0] += offsetX
    else:
        final[0] -= offsetX
    if final[1] > other[1]:
        final[1] += offsetY
    else:
        final[1] -= offsetY
    return final

    [stick.pointB.position[0] + offsetX, stick.pointB.position[1] + offsetY]

def Calculate():
    for point in points:
        if not point.locked:
            positionBeforeUpdate = point.position
            point.position = [2 * point.position[0] - point.prevPosition[0], 2 * point.position[1] - point.prevPosition[1]]
            point.position = [point.position[0], point.position[1] + gravity * deltaTime]

            if point.position[0] < 0:
                point.position[0] = 0
                positionBeforeUpdate[0] += 2 * (point.position[0] - point.prevPosition[0]) * bounce
            elif point.position[0] > 720:
                point.position[0] = 720
                positionBeforeUpdate[0] += 2 * (point.position[0] - point.prevPosition[0]) * bounce
            if point.position[1] < 0:
                point.position[1] = 0
                positionBeforeUpdate[1] += 2 * (point.position[1] - point.prevPosition[1]) * bounce
            elif point.position[1] > 720:
                point.position[1] = 720
                positionBeforeUpdate[1] += 2 * (point.position[1] - point.prevPosition[1]) * bounce

            point.prevPosition = positionBeforeUpdate

    for i in range(iterations):
        random.shuffle(sticks)
        for stick in sticks:
            dx = np.abs(stick.pointA.position[0] - stick.pointB.position[0])
            dy = np.abs(stick.pointA.position[1] - stick.pointB.position[1])
            distance = math.sqrt(dx ** 2 + dy ** 2)
            difference = stick.length - distance
            try:
                percent = difference / distance / 2
                offsetX = dx * percent
                offsetY = dy * percent
                if not stick.pointA.locked:
                    if stick.pointB.locked:
                        offsetX *= 2
                        offsetY *= 2
                    stick.pointA.position = Change(stick.pointA.position, stick.pointB.position, offsetX, offsetY)
                else:
                    offsetX *= 2
                    offsetY *= 2
                if not stick.pointB.locked:
                    stick.pointB.position = Change(stick.pointB.position, stick.pointA.position, offsetX, offsetY)
            except:
                pass

def Render(screen):
    screen.fill((84, 94, 110))
    for point in points:
        pg.draw.circle(screen, point.color, (point.position[0], point.position[1]), pointSize)

    for stick in sticks:
        pg.draw.line(screen, stick.color, (stick.pointA.position[0], stick.pointA.position[1]), (stick.pointB.position[0], stick.pointB.position[1]), stickWidth)

def SpawnBox():
    points.append(Point(100, 100, False))
    points.append(Point(100, 200, False))
    points.append(Point(200, 200, False))
    points.append(Point(200, 100, False))

    sticks.append(Stick(points[0], points[1]))
    sticks.append(Stick(points[1], points[2]))
    sticks.append(Stick(points[2], points[3]))
    sticks.append(Stick(points[3], points[0]))
    sticks.append(Stick(points[0], points[2]))

def SpawnDots():
    for y in range(10):
        for x in range(10):
            points.append(Point(y * 70 + 35, x * 70, False))

def SpawnGrid():
    for y in range(10):
        for x in range(10):
            points.append(Point(y * 70 + 35, x * 70, False))

    for y in range(10):
        for x in range(10):
            if x < 9:
                sticks.append(Stick(points[y*10+x], points[y*10+x+1]))
            if y < 9:
                sticks.append(Stick(points[y*10+x], points[y*10+x+10]))

def SpawnCape():
    for y in range(10):
        for x in range(10):
            points.append(Point(y * 70 + 35, x * 70, False))
    points[0].Lock()
    points[30].Lock()
    points[60].Lock()
    points[90].Lock()

    for y in range(10):
        for x in range(10):
            if x < 9:
                sticks.append(Stick(points[y*10+x], points[y*10+x+1]))
            if y < 9:
                sticks.append(Stick(points[y*10+x], points[y*10+x+10]))

def SpawnRigidBody():
    for y in range(10):
        for x in range(10):
            points.append(Point(y * 70 + 35, x * 70, False))

    for y in range(10):
        for x in range(10):
            if x < 9:
                sticks.append(Stick(points[y*10+x], points[y*10+x+1]))
            if y < 9:
                sticks.append(Stick(points[y*10+x], points[y*10+x+10]))
            if x < 9 and y < 9:
                sticks.append(Stick(points[y*10+x], points[y*10+x+11]))
            if y < 9 and x > 0:
                sticks.append(Stick(points[y*10+x], points[y*10+x+9]))

def SpawnPendulum():
    for i in range(10):
        points.append(Point(50 * i + 50, 100, False))
    points[-1].Lock()

    for i in range(9):
        sticks.append(Stick(points[i], points[i + 1]))

def Start(screen):
    # SpawnBox()
    # SpawnDots()
    # SpawnGrid()
    # SpawnCape()
    # SpawnRigidBody()
    # SpawnPendulum()

    global points
    global sticks

    lastClicked = [None, None]
    while True:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    return None
                elif event.key == pg.K_SPACE:
                    if lastClicked[0] != None and lastClicked[1] != None:
                        sticks.append(Stick(lastClicked[0], lastClicked[1]))
                elif event.key == pg.K_r:
                    points = []
                    sticks = []
            elif event.type == pg.MOUSEBUTTONDOWN:
                if pg.mouse.get_pressed()[0]:
                    pos = pg.mouse.get_pos()
                    points.append(Point(pos[0], pos[1], False))
                elif pg.mouse.get_pressed()[2]:
                    pos = pg.mouse.get_pos()
                    clicked = [p for p in points if math.sqrt((p.position[0] - pos[0]) ** 2 + (p.position[1] - pos[1]) ** 2) <= pointSize]
                    try:
                        lastClicked[0] = lastClicked[1]
                        lastClicked[1] = clicked[0]
                        if lastClicked[0] == lastClicked[1]:
                            if lastClicked[0].locked:
                                lastClicked[0].Unlock()
                            else:
                                lastClicked[0].Lock()
                    except:
                        pass

        Render(screen)
        pg.display.update()
    return None

def main():
    screen = ScreenInit()
    Start(screen)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return None
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    return None
                elif event.key == pg.K_r:
                    global points
                    global sticks

                    points = []
                    sticks = []
                    Start(screen)

        time.sleep(0.01)
        Calculate()
        Render(screen)
        pg.display.update()

main()
pg.quit()
