import numpy as np

# Define constants
WHITE = (255, 255, 255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0, 0, 0)

def update_rotation_matrix(rotation_matrix, angular_velocity, dt): # UNKNOWN ERROR
    """
    Update the rotation matrix with a given angular velocity vector for a time
    increment dt.
    """
    skew_symmetric_matrix = np.array([[0, -angular_velocity[2], angular_velocity[1]],
                                      [angular_velocity[2], 0, -angular_velocity[0]],
                                      [-angular_velocity[1], angular_velocity[0], 0]])
    delta_rotation_matrix = np.eye(3) + skew_symmetric_matrix * dt

    new_rotation_matrix = np.dot(delta_rotation_matrix, rotation_matrix)

    # Orthogonalize the new rotation matrix using Gram-Schmidt process
    new_rotation_matrix, _ = np.linalg.qr(new_rotation_matrix)
    return new_rotation_matrix

def update_rotation_matrix_ME(rotation_matrix, angular_velocity, dt):
    """
    Update the rotation matrix with a given angular velocity vector for a time
    increment dt.
    """
    skew_symmetric_matrix = np.array([[0, -angular_velocity[2], angular_velocity[1]],
                                      [angular_velocity[2], 0, -angular_velocity[0]],
                                      [-angular_velocity[1], angular_velocity[0], 0]])
    delta_rotation_matrix = np.eye(3) + skew_symmetric_matrix * dt

    new_rotation_matrix = np.dot(delta_rotation_matrix, rotation_matrix)
    
    temp = new_rotation_matrix.copy()
    #print(new_rotation_matrix)
    new_rotation_matrix[:,1] = np.cross(temp[:,2] , temp[:,0])
    new_rotation_matrix[:,2] = np.cross(temp[:,0] , temp[:,1])

    #Normalize
    #new_rotation_matrix[:,0] /=  np.linalg.norm(new_rotation_matrix[:,0])
    #new_rotation_matrix[:,1] /=  np.linalg.norm(new_rotation_matrix[:,1])
    #new_rotation_matrix[:,2] /=  np.linalg.norm(new_rotation_matrix[:,2])
    #Normalize Optimized
    norms = np.linalg.norm(new_rotation_matrix, axis=0)
    new_rotation_matrix /= norms

    return new_rotation_matrix

def update_rotation_matrix_exponential_coordinates(rotation_matrix, angular_velocity, dt):
    """
    Update the rotation matrix with a given angular velocity vector for a time
    increment dt.
    """
    angular_mag = np.linalg.norm(angular_velocity)
    if angular_mag == 0 :
        return rotation_matrix
    skew_symmetric_m = np.array([[0, -angular_velocity[2], angular_velocity[1]],
                                      [angular_velocity[2], 0, -angular_velocity[0]],
                                      [-angular_velocity[1], angular_velocity[0], 0]])
    first = np.dot(np.sin(angular_mag*dt) /angular_mag, skew_symmetric_m)
  
    skew_symmetric_m2 = np.dot(skew_symmetric_m,skew_symmetric_m)
    second = np.dot((1-np.cos(angular_mag*dt))/angular_mag**2 , skew_symmetric_m2)

    #print(rotation_matrix + first + second)
    e = np.array([[1, 0, 0],
                           [0, 1, 0],
                           [0, 0, 1]]) + first + second

    return np.dot(rotation_matrix,e)