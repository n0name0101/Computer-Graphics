import numpy as np

# Define constants
WHITE = (1, 1, 1)
RED = (1,0,0)
GREEN = (0,1,0)
BLACK = (0, 0, 0)

#Integrating With Euler Method
def integrateR_ME(rotation_matrix, angular_velocity, dt):
    skew_symmetric_matrix = np.array([[0, -angular_velocity[2], angular_velocity[1]],
                                      [angular_velocity[2], 0, -angular_velocity[0]],
                                      [-angular_velocity[1], angular_velocity[0], 0]])
    
    delta_rotation_matrix = np.eye(3) + skew_symmetric_matrix * dt
    new_rotation_matrix = np.dot(delta_rotation_matrix, rotation_matrix)

    # Another Way to Integrate Rotation Matrix
    # delta_rotation_matrix = np.dot(skew_symmetric_matrix,rotation_matrix) * dt
    # new_rotation_matrix = rotation_matrix + delta_rotation_matrix
    
    temp = new_rotation_matrix.copy()
    new_rotation_matrix[:,0] = new_rotation_matrix[:,0]/np.linalg.norm(new_rotation_matrix[:,0])
    new_rotation_matrix[:,2] = np.cross(new_rotation_matrix[:,0] , temp[:,1])
    new_rotation_matrix[:,1] = np.cross(temp[:,2] ,new_rotation_matrix[:,0])

    norms = np.linalg.norm(new_rotation_matrix, axis=0)
    new_rotation_matrix /= norms

    return new_rotation_matrix

