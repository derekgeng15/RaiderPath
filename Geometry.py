import math
import pygame
import pygame.gfxdraw


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw_point(self, surface, color, size):
        DPoint = pygame.Rect(self.x * 1.5 - size/2, 319 * 1.5 -
                             self.y * 1.5 - size/2, size, size)
        pygame.gfxdraw.box(surface, DPoint, color)

    def dist(self, p):
        return math.sqrt((self.x - p.x)**2 + (self.y - p.y)**2)

    def rot(self, point, theta):
        x = math.cos(theta) * (self.x-point.x) - \
            math.sin(theta) * (self.y-point.y) + point.x
        y = math.sin(theta) * (self.x-point.x) + \
            math.cos(theta) * (self.y-point.y) + point.y
        self.x = x
        self.y = y


class TrajPoint(Point):
    def __init__(self, x, y, curvature=0, vel=0):
        super().__init__(x, y)
        self.curvature = curvature
        self.vel = vel


class WayPoint(Point):
    def __init__(self, x, y, theta=0.0):
        super().__init__(x, y)
        self.theta = theta
        self.tanVec = Point(math.sin(theta), math.cos(theta))


class Pose(Point):
    def __init__(self, x, y, theta):
        super().__init__(x, y)
        self.theta = theta
