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

# struct class for lines
class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.x = p2.x - p1.x
        self.y = p2.y - p1.y

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

# class for polygons
class Polygon:
    def __init__(self, points):
        self.points = [Point.fromTuple(point) for point in points]
        self.lines = [Line(self.points[i], self.points[(i + 1) % len(self.points)]) for i in range(len(self.points))]

    def fill(self, screen, color):
        n = len(self.lines)

        # get lowest and highest point
        lowest = math.floor(min([point.y for point in self.points]))
        highest = math.ceil(max([point.y for point in self.points]))

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
            # if line is stretched out in x direction, scan x-verticals and draw points at intersections
            if abs(line.x) > abs(line.y):
                lowest = math.floor(min(line.p1.x, line.p2.x))
                highest = math.ceil(max(line.p1.x, line.p2.x))
                for x in range(lowest, highest):
                    point = line.intersectX(x)
                    screen.set_at((x, round(point.y)), color)
            # if line is stretched out in y direction, scan y-horizontals and draw points at intersections
            else:
                lowest = math.floor(min(line.p1.y, line.p2.y))
                highest = math.ceil(max(line.p1.y, line.p2.y))
                for y in range(lowest, highest):
                    point = line.intersectY(y)
                    screen.set_at((round(point.x), y), color)
