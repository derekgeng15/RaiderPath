import math
import pygame
import pygame.gfxdraw
import Geometry as geo


class Robot:
    def __init__(self, pos, width, length):
        self.pos = pos
        self.length = length
        self.width = width
        self.lookAheadDistance = 50

    def move(self, leftVel, rightVel):
        if leftVel == rightVel:
            rightVel += 0.0000001
        R = (self.width/2)*(leftVel + rightVel)/(rightVel - leftVel)
        angVel = (rightVel - leftVel)/self.width
        ICC = geo.Point(self.pos.x - R * math.sin(self.pos.theta),
                        self.pos.y + R * math.cos(self.pos.theta))
        x = (self.pos.x - ICC.x)*math.cos(angVel) + \
            (self.pos.y - ICC.y) * -math.sin(angVel) + ICC.x
        y = (self.pos.x - ICC.x)*math.sin(angVel) + \
            (self.pos.y - ICC.y) * math.cos(angVel) + ICC.y
        theta = angVel + self.pos.theta
        self.pos = geo.Pose(x, y, theta)

    def draw(self, surface, color):
        corners = []
        corners.append(geo.Point(self.pos.x * 1.5 - self.length /
                                 3, self.pos.y * 1.5 - self.width/3))
        corners.append(geo.Point(self.pos.x * 1.5 - self.length /
                                 3, self.pos.y * 1.5 + self.width/3))
        corners.append(geo.Point(self.pos.x * 1.5 + self.length /
                                 3, self.pos.y * 1.5 + self.width/3))
        corners.append(geo.Point(self.pos.x * 1.5 + self.length /
                                 3, self.pos.y * 1.5 - self.width/3))
        shape = []
        for corner in corners:
            corner.rot(geo.Point(self.pos.x * 1.5, self.pos.y * 1.5), self.pos.theta)
            shape.append((corner.x, 323.25 * 1.5 - corner.y))
        pygame.gfxdraw.polygon(surface, shape, color)
        pygame.gfxdraw.line(surface, int(corners[2].x), int(
            323.25 * 1.5 - corners[2].y), int(corners[3].x), int(323.25 * 1.5 - corners[3].y), [255, 150, 0])
