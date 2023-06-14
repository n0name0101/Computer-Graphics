import math

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"(X:{self.x}, Y:{self.y})"

    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        else:
            raise TypeError("Unsupported operand type for +")

    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        else:
            raise TypeError("Unsupported operand type for -")

    def __mul__(self, other):
        if isinstance(other, Vector2):
            # Dot product
            return self.x * other.x + self.y * other.y
        elif isinstance(other, (int, float)):
            # Scalar multiplication
            return Vector2(self.x * other, self.y * other)
        else:
            raise TypeError("Unsupported operand type for *")

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            # Scalar division
            return Vector2(self.x / other, self.y / other)
        else:
            raise TypeError("Unsupported operand type for /")

    def __abs__(self):
        # Magnitude or length of the vector
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        # Normalize the vector
        magnitude = abs(self)
        return self / magnitude

    def limit(self,limit):
        if abs(self) <= limit :
            return Vector2(self.x,self.y)
        return self / abs(self) * limit

    def rotate(self, degrees):
        radians = math.radians(degrees)
        cos_theta = math.cos(radians)
        sin_theta = math.sin(radians)
        x_new = self.x * cos_theta - self.y * sin_theta
        y_new = self.x * sin_theta + self.y * cos_theta
        return Vector2(x_new, y_new)

    def setXY(self,x,y):
        self.x = x
        self.y = y

    def getlist(self) :
        return [self.x,self.y]
