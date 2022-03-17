import math

# struct class for points
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def equals(self, point):
        return self.x == point.x and self.y == point.y

    def toTuple(self):
        return (self.x, self.y)

    @staticmethod
    def fromTuple(t):
        return Point(t[0], t[1])

# class for lines
class Line:
    def __init__(self, p1, p2):
        if isinstance(p1, Point):
            self.p1 = p1
            self.p2 = p2
        elif isinstance(p1, tuple):
            self.p1 = Point.fromTuple(p1)
            self.p2 = Point.fromTuple(p2)

        self.x = self.p2.x - self.p1.x
        self.y = self.p2.y - self.p1.y

    # get intersection of line with vertical line; returns False if no intersections; returns True if line lies on vertical; otherwise returns intersection point
    def intersectX(self, x):
        # handle trivial cases to avoid division by 0; solved using vector lines
        if (self.p1.x == self.p2.x):
            if (self.p1.y == self.p2.y):
                if (self.p1.x == x):
                    return Point(x, self.p1.y)
            else:
                if (self.p1.x == x):
                    return True
        else:
            # vector line: a = p1 + (p1 - p2) * r; vector vertical: a = (x | 0) + (0 | 1) * y
            # solve for r, if 0 <= r <= 1: point lies in line segment
            if 0 <= (x - self.p1.x) / self.x <= 1:
                # solve for y using system of linear equations
                return Point(x, self.p1.y + (x - self.p1.x) / self.x * self.y)

        return False

    # get intersection of line with horizontal line; returns False if no intersections; returns True if line lies on horizontal; otherwise returns intersection point
    def intersectY(self, y):
        # handle trivial cases to avoid division by 0; solved using vector lines
        if (self.y == 0):
            if (self.x == 0):
                if (self.p1.y == y):
                    return Point(self.p1.x, y)
            else:
                if (self.p1.y == y):
                    return True
        else:
            # vector line: a = p1 + (p1 - p2) * r; vector horizontal: a = (0 | y) + (1 | 0) * x
            # solve for r, if 0 <= r <= 1: point lies in line segment
            if 0 <= (y - self.p1.y) / self.y <= 1:
                # solve for y using system of linear equations
                return Point(self.p1.x + (y - self.p1.y) / self.y * self.x, y)

        return False

    # check if lines are open or closed in x-direction
    def isClosedCorner(self, line):
        return self.y > 0 and line.y < 0 or self.y < 0 and line.y > 0

    def draw(self, screen, color):
        # if line is stretched out in x direction, scan x-verticals and draw points at intersections
        if abs(self.x) > abs(self.y):
            lowest = math.ceil(min(self.p1.x, self.p2.x))
            highest = math.floor(max(self.p1.x, self.p2.x))
            for x in range(lowest, highest + 1):
                point = self.intersectX(x)
                screen.set_at((x, round(point.y)), color)
        # if line is stretched out in y direction, scan y-horizontals and draw points at intersections
        else:
            lowest = math.ceil(min(self.p1.y, self.p2.y))
            highest = math.floor(max(self.p1.y, self.p2.y))
            for y in range(lowest, highest + 1):
                point = self.intersectY(y)
                screen.set_at((round(point.x), y), color)

# class for polygons
class Polygon:
    def __init__(self, points):
        self.points = [Point.fromTuple(point) for point in points]
        self.lines = [Line(self.points[i], self.points[(i + 1) % len(self.points)]) for i in range(len(self.points))]

    def fill(self, screen, color):
        n = len(self.lines)

        # get lowest and highest point
        lowest = math.ceil(min([point.y for point in self.points]))
        highest = math.floor(max([point.y for point in self.points]))

        # scan all horizontals
        for y in range(lowest, highest + 1):
            # get intersections of lines with horizontal
            lineRelations = [line.intersectY(y) for line in self.lines]
            xPoints = []

            for i in range(n):
                checkedPoint = None

                if lineRelations[i] is True:
                    # if line lies on horizontal, add first point, check if second point is connected to open or close corner
                    xPoints.append(self.lines[i].p1.x)
                    if self.lines[(i + 1) % n].y == 0:
                        xPoints.append(self.lines[i].p2.x)
                    else:
                        # check if corner is closed when delayed by a straight line
                        firstLine = i - 1
                        while self.lines[firstLine].y == 0:
                            firstLine = (firstLine - 1) % n
                        else:
                            if not self.lines[firstLine].isClosedCorner(self.lines[(i + 1) % n]):
                                xPoints.append(self.lines[i].p2.x)

                elif isinstance(lineRelations[i], Point):
                    # if intersection point is the end point, check if it is connected to open or close corner, else add it
                    if lineRelations[i].equals(self.lines[i].p2):
                        # check if point is open or closed in x-direction, if open, don't add it, so the line gets drawn to another intersection with horizontal instead of to the point itself
                        if self.lines[i].isClosedCorner(self.lines[(i + 1) % n]):
                            xPoints.append(lineRelations[i].x)
                    else:
                        xPoints.append(lineRelations[i].x)  

            # sort x-values
            xPoints = sorted(xPoints)

            # connect first and second point, third and fourth...
            for i in range(0, len(xPoints), 2):
                left = round(min(xPoints[i], xPoints[i + 1]))
                right = round(max(xPoints[i], xPoints[i + 1]))
                for x in range(left, right + 1):
                    screen.set_at((x, y), color)

    def outline(self, screen, color):
        for line in self.lines:
            line.draw(screen, color)

# class for rectangles
class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def fill(self, screen, color):
        # scan all horizontals and fill
        for y in range(round(self.y), round(self.y + self.height) + 1):
            for x in range(round(self.x), round(self.x + self.width) + 1):
                screen.set_at((x, y), color)

    def outline(self, screen, color):
        # scan all horizontals
        for y in range(round(self.y), round(self.y + self.height) + 1):
            screen.set_at((round(self.x), y), color)
            screen.set_at((round(self.x + self.width), y), color)

        # scan all verticals
        for x in range(round(self.x), round(self.x + self.width) + 1):
            screen.set_at((x, round(self.y)), color)
            screen.set_at((x, round(self.y + self.height)), color)

# class for circles
class Circle:
    def __init__(self, center, radius):
        self.center = Point.fromTuple(center)
        self.radius = radius

    def fill(self, screen, color):
        # scan all horizontals
        for y in range(math.ceil(self.center.y - self.radius), math.floor(self.center.y + self.radius) + 1):
            # calculate intersections from x^2+y^2=r^2
            offset = math.sqrt(self.radius ** 2 - (y - self.center.y) ** 2)
            left = round(self.center.x - offset)
            right = round(self.center.x + offset)
            for x in range(left, right + 1):
                screen.set_at((x, y), color)

    def outline(self, screen, color):
        # to outline a circle, it is cut in four quarters to avoid gaps, 2 are rendered horizontally, 2 are rendered vertically
        d45 = math.sqrt(2) / 2 * self.radius

        # scan all horizontals
        for y in range(round(self.center.y - d45), round(self.center.y + d45) + 1):
            # calculate intersections from x^2+y^2=r^2
            offset = math.sqrt(self.radius ** 2 - (y - self.center.y) ** 2)
            screen.set_at((round(self.center.x - offset), y), color)
            screen.set_at((round(self.center.x + offset), y), color)

        # scan all verticals
        for x in range(round(self.center.x - d45), round(self.center.x + d45) + 1):
            # calculate intersections from x^2+y^2=r^2
            offset = math.sqrt(self.radius ** 2 - (x - self.center.x) ** 2)
            screen.set_at((x, round(self.center.y - offset)), color)
            screen.set_at((x, round(self.center.y + offset)), color)