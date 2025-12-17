class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    def __str__(self):
        return f"Point({self.x}, {self.y})"

    def distance(self, other):
        if isinstance(other, Point):
            return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5
        raise ValueError("Other must be a Point")

class Vector(Point):
    def __str__(self):
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        return NotImplemented

# Demonstrations
p1 = Point(1, 2)
p2 = Point(3, 4)
print("Point p1:", p1)
print("Point p2:", p2)
print("p1 == p2:", p1 == p2)
print("Distance between p1 and p2:", p1.distance(p2))

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print("Vector v1:", v1)
print("Vector v2:", v2)
v3 = v1 + v2
print("v1 + v2:", v3)
print("v1 == v2:", v1 == v2)
v4 = Vector(1, 2)
print("v1 == v4:", v1 == v4)
