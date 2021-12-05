import numpy as np
import pandas as pd
import collections
import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Point(%d, %d)" % (self.x, self.y)

    def __eq__(self, other):
        if isinstance(other, Point):
            return ((self.x == other.x) and (self.y == other.y))
        else:
            return False

    def __ne__(self, other):
        return (not self.__eq__(other))

    def __hash__(self):
        return hash(self.__repr__())

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def is_diagonal(self):
        if (self.p1.x == self.p2.x) or (self.p1.y == self.p2.y):
            return False
        else:
            return True

    def get_xdir(self):
        return math.copysign(1, self.p2.x - self.p1.x)

    def get_ydir(self):
        return math.copysign(1, self.p2.y - self.p1.y)

    def get_magnitude(self):
        return abs(self.p2.x - self.p1.x)

    def get_covered_points(self, incl_diagonal):
        # only works for non-diagonal points
        covered_points = []
        if self.is_diagonal() and incl_diagonal:
            x_incr = int(self.get_xdir())
            y_incr = int(self.get_ydir())
            num_points = self.get_magnitude()
            x = self.p1.x
            y = self.p1.y
            for i in range(num_points+1):
                covered_points.append(Point(x, y))
                x += x_incr
                y += y_incr
        elif not self.is_diagonal():
            for x in range(min(self.p1.x, self.p2.x), max(self.p1.x, self.p2.x)+1):
                for y in range(min(self.p1.y, self.p2.y), max(self.p1.y, self.p2.y)+1):
                    covered_points.append(Point(x, y))

        return covered_points

class Plane:
    def __init__(self):
        self.points = collections.Counter()
        self.max_x = 0
        self.max_y = 0

    def add_point(self, p):
        self.points[p] += 1
        self.max_x = max(self.max_x, p.x)
        self.max_y = max(self.max_y, p.y)

    def add_points(self, points):
        for p in points:
            self.add_point(p)

    def get_points(self):
        return self.points

    def display(self):
        display = np.full((self.max_y+1, self.max_x+1), '.')
        for p, count in self.points.items():
            display[p.y, p.x] = str(count)

        for row in display:
            print(''.join(row))

    def count_danger_points(self):
        return len([i for i in self.points.values() if i >= 2])


def create_plane(_input, incl_diagonal):
    """
    Parse input into coordinates on a 2d plane.
    """
    plane = Plane()
    for l in _input:
        if l:
            points = l.split(' -> ')
            p1_in = points[0].strip().split(',')
            p2_in = points[1].strip().split(',')
            p1 = Point(int(p1_in[0]), int(p1_in[1]))
            p2 = Point(int(p2_in[0]), int(p2_in[1]))
            line = Line(p1, p2)
            plane.add_points(line.get_covered_points(incl_diagonal))

    return plane


def run(_input):

    plane = create_plane(_input, False)
    # plane.display()

    print('Day 5, Part 1: {}'.format(plane.count_danger_points()))

    plane = create_plane(_input, True)
    # plane.display()

    print('Day 5, Part 2: {}'.format(plane.count_danger_points()))
