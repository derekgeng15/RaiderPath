import math
import Geometry as geo

WHITE = [255, 255, 255]
RED = [255, 0, 0]
BLACK = [0, 0, 0]
GREEN = [0, 255, 0]


class Segment:
    def __init__(self, p0, p1):
        self.p0 = p0
        self.p1 = p1
        self.points = []
    def get_divisor(self, currDivisor = 1):
        t = 1/currDivisor
        h1 = 2 * t**3 - 3 * t**2 + 1
        h2 = -2 * t**3 + 3 * t**2
        h3 = t**3 - 2 * t**2 + t
        h4 = t**3 - t**2
        x = h1 * self.p0.x + h2 * self.p1.x + h3 * \
            self.p0.tanVec.x + h4 * self.p1.tanVec.x
        y = h1 * self.p0.y + h2 * self.p1.y + h3 * \
            self.p0.tanVec.y + h4 * self.p1.tanVec.y
        p = geo.TrajPoint(x, y)
        if p.dist(self.p0) <= 1:
            return currDivisor
        return self.get_divisor(currDivisor * 2)

    def draw(self, surface, color):
        d = self.get_divisor()
        for i in range(d):
            t = i / d
            h1 = 2 * t**3 - 3 * t**2 + 1
            h2 = -2 * t**3 + 3 * t**2
            h3 = t**3 - 2 * t**2 + t
            h4 = t**3 - t**2
            x = h1 * self.p0.x + h2 * self.p1.x + h3 * \
                self.p0.tanVec.x + h4 * self.p1.tanVec.x
            y = h1 * self.p0.y + h2 * self.p1.y + h3 * \
                self.p0.tanVec.y + h4 * self.p1.tanVec.y
            p = geo.TrajPoint(x, y)
            self.points.append(p)
            p.draw_point(surface, color, 5)
    


class Curve:
    def __init__(self, startHeading, endHeading):
        self.waypoints = []
        self.points = []
        self.startHeading = startHeading
        self.endHeading = endHeading
        self.calc_tang()

    def findTan(self, w1, w2, heading, start):
        dist = 0
        if heading == 90 or heading == -90:
            dist = 2 * abs(w1.y - w2.y)
        elif heading == 0 or heading == -180 or heading == 180:
            dist = 2 * abs(w1.x - w2.x)
        else:
            m = math.tan(heading)
            im = -1/m
            if start:
                x = (m * w2.x - im * w1.x + w1.y - w2.y)/(m - im)
                y = m * (x - w2.x) + w2.y
                dist = 2 * w2.dist(geo.Point(x, y))
            else:
                x = (m * w1.x - im * w2.x + w2.y - w1.y)/(m - im)
                y = m * (x - w1.x) + w1.y
                dist = 2 * w1.dist(geo.Point(x, y))
        if start:
            x = w2.x - dist * math.cos(heading)
            y = w2.y - dist * math.sin(heading)
            w1.tanVec.x = (w2.x - x) * 0.5
            w1.tanVec.y = (w2.y - y) * 0.5
            w1.theta = heading
        else:
            x = w1.x + dist * math.cos(heading)
            y = w1.y + dist * math.sin(heading)
            w2.tanVec.x = (x - w1.x) * 0.5
            w2.tanVec.y = (y - w1.y) * 0.5
            w2.theta = heading

    def calc_tang(self):
        if len(self.waypoints) < 2:
            return
        for i in range(1, len(self.waypoints)-1):
            x = 0.5 * (self.waypoints[i+1].x - self.waypoints[i-1].x)
            y = 0.5 * (self.waypoints[i+1].y - self.waypoints[i-1].y)
            self.waypoints[i].tanVec.x = x
            self.waypoints[i].tanVec.y = y
            self.waypoints[i].theta = math.atan2(y, x)
        self.findTan(self.waypoints[0],
                     self.waypoints[1], self.startHeading, True)
        self.findTan(self.waypoints[-2],
                     self.waypoints[-1], self.endHeading, False)

    def drawCurve(self, surface, color):
        self.points = []
        for i in range(1, len(self.waypoints)):
            seg = Segment(self.waypoints[i - 1], self.waypoints[i])
            seg.draw(surface, color)
            for segpoint in seg.points:
                self.points.append(segpoint)

    def drawWayPoints(self, surface, color):
        for point in self.waypoints:
            point.draw_point(surface, color, 10)

    def add_point(self, point):
        self.waypoints.append(point)
        self.calc_tang()
