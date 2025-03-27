import numpy as np

class Camera:
    def __init__(self, pos=np.array([0, 0, 0]), lookat=np.array([0, 0, 1])):
        self.pos = pos
        self.lookat = lookat/np.linalg.norm(lookat)

    def matrix_point_at(self):
        # Calculate new forward direction
        new_forward = self.lookat
        new_forward = new_forward / np.linalg.norm(new_forward)

        # Calculate new Up direction
        up = np.array([0,1,0])
        a = new_forward * np.dot(up, new_forward)
        new_up = up - a
        new_up = new_up / np.linalg.norm(new_up)

        # New Right direction is easy, its just cross product
        new_right = np.cross(new_up, new_forward)

        # Construct Dimensioning and Translation Matrix
        matrix = np.zeros((4, 4))
        matrix[0, :3] = new_right
        matrix[1, :3] = new_up
        matrix[2, :3] = new_forward
        matrix[3, :3] = self.pos
        matrix[3, 3] = 1.0

        return matrix


    def get_view_matrix(self):
        return np.linalg.inv(self.matrix_point_at())
