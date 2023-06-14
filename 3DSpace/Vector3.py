import math

class Vector3:
    def __init__(self, x, y, z, texture=False , u=0 , v=0):
        self.x = x
        self.y = y
        self.z = z
        self.texture = texture
        self.u = u
        self.v = v

    def __str__(self):
        return f"(X:{self.x}, Y:{self.y}, Z:{self.z})"

    def __add__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            raise TypeError("Unsupported operand type for +")

    def __sub__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            raise TypeError("Unsupported operand type for -")

    def __mul__(self, other):
        if isinstance(other, Vector3):
            # Dot product
            return self.x * other.x + self.y * other.y + self.z * other.z
        elif isinstance(other, (int, float)):
            # Scalar multiplication
            return Vector3(self.x * other, self.y * other, self.z * other)
        else:
            raise TypeError("Unsupported operand type for *")

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            # Scalar division
            return Vector3(self.x / other, self.y / other, self.z / other)
        else:
            raise TypeError("Unsupported operand type for /")

    def __abs__(self):
        # Magnitude or length of the vector
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self):
        # Normalize the vector
        magnitude = abs(self)
        return self / magnitude

    def cross(self, other):
        # Cross product
        if isinstance(other, Vector3):
            return Vector3(
                self.y * other.z - self.z * other.y,
                self.z * other.x - self.x * other.z,
                self.x * other.y - self.y * other.x
            )
        else:
            raise TypeError("Unsupported operand type for cross product")

    def rotate(self, angle_x, angle_y, angle_z):
        # Rotate the vector by the given angles (in radians) for each axis
        # Rotate around X-axis
        rotated_x = self.x
        rotated_y = self.y * math.cos(angle_x) - self.z * math.sin(angle_x)
        rotated_z = self.y * math.sin(angle_x) + self.z * math.cos(angle_x)

        # Rotate around Y-axis
        rotated_x = rotated_x * math.cos(angle_y) + rotated_z * math.sin(angle_y)
        rotated_y = rotated_y
        rotated_z = -rotated_x * math.sin(angle_y) + rotated_z * math.cos(angle_y)

        # Rotate around Z-axis
        rotated_x = rotated_x * math.cos(angle_z) - rotated_y * math.sin(angle_z)
        rotated_y = rotated_x * math.sin(angle_z) + rotated_y * math.cos(angle_z)
        rotated_z = rotated_z

        return Vector3(rotated_x, rotated_y, rotated_z)


    def getlist(self) :
        return [self.x,self.y,self.z]


