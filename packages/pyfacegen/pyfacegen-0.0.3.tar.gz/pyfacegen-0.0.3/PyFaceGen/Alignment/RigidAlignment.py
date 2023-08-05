# python version 3.8
# This code is used to align any two arbitrary meshes using rotation, translation
# and scale. 

# We use ICP with additional scaling as done inhttp://web.stanford.edu/class/cs273/refs/umeyama.pdf 

import numpy as np
from sklearn.neighbors import NearestNeighbors
from PyFaceGen.Mesh.Mesh import Mesh
from PyFaceGen.Mesh.Utils import get_normals

def estimateRigidTransform(A,B):
    
    """ Estimates the optimal 4x4 rigid transform between points in correspondence
    
        (returns):
            T (ndarray of 4x4): The transformation matrix 
    
    """
    
    assert A.shape == B.shape, "A and B must be the same shape but are %s and %s"%(A.shape, B.shape)
    
    n = A.shape[0]
    
    # Compute centroids and shift the points
    centroid_A = np.mean(A, axis=0)
    centroid_B = np.mean(B, axis=0)
    
    A_ = A - centroid_A
    B_ = B - centroid_B
    
    # Compute the H matrix and perform single value decomposition
    H = A_.T @ B_ / n
    U, D, VT = np.linalg.svd(H)
    
    # Compute the optimal rotation which is VU^T
    R = VT.T @ U.T
    # special reflection case
    if np.linalg.det(R) < 0:
       VT[2,:] *= -1
       D[-1] *= 1
       R = VT.T @ U.T
    
    varP = np.var(A, axis=0).sum()
    scale = 1/varP * np.sum(D)
    
    '''if np.isnan(scale):
        T = np.eye(4)
        return T, np.eye(3), 1, np.zeros((3,1))'''
    
    RS = R * scale
    #print(scale)
    # Compute translation
    t = centroid_B.T - (RS @ centroid_A.T)
    
    
    T = np.eye(4)
    T[0:3,0:3] = RS
    T[0:3, 3] = t
    return T, R, scale, t
    
    
    

def rigid_align(fixed, floating, n_iters=10000, init_rotation=np.eye(3), init_translation=np.zeros((3,)), init_scale=np.ones((3,)), tolerance=0.001):
    
    """ Rigidly align, using rotation, translation and scale, a floating mesh
        to a fixed mesh 
        
        (params):
            fixed (Mesh): The mesh that will not be moving
            floating (Mesh): The mesh that will be transformed            
        (optional params)
            n_iters (int): The number of iterations
            init_rotation (3x3 ndarray): Provides an inital estimate for rotataion as a speed up
            init_translation (3, ndarray): Provides an inital estimate for translation as a speed up
            init_scale (3, ndarray): Provides an inital estimate for scale as a speed up
            tolerance (float): The tolerance at which to end the algorithm early
        (returns):
            (Mesh): The floating mesh, aligned to the fixed mesh
            (2d-ndarray of 4x4): The transformation matrix applied to the floating mesh
    
    """
    
    # Get the vertices and transpose
    
    f_copy = floating.vertices

    source = np.float32(floating.vertices.T)
    target = np.float32(fixed.vertices.T)
    
    # Convert to homogenous co-ordinates
    source = np.concatenate((source, np.ones((1, source.shape[1]), dtype='float32' )))
    target = np.concatenate((target, np.ones((1, target.shape[1]), dtype='float32' )))

    # Compute the 4x4 transformation matrix for the inital transformation    
    transform = np.eye(4)
    transform[0:3,0:3] = init_rotation * init_scale
    transform[0:3,3] = init_translation
    
    # Transform the source by the initial estimate
    source = transform @ source
    
    # Keep track of how good an estimate we have
    error = np.inf
    best_error = error
    best_transform = np.array(transform)
    
    for i in range(n_iters):
        # First we compute point correspondences
        
        nn = NearestNeighbors(n_neighbors=1).fit(target.T)
        #print(np.max(source.T))
        
        dist, idx = nn.kneighbors(source.T)
        
        # Get the optimal rigid transform for these point correspondences
        transform, _,s,_ = estimateRigidTransform(source[0:3,:].T, target[0:3, idx].reshape(3,-1).T)
        #print(s)
        
        # Do the transform
        s_copy = np.array(source)
        
        source = transform @ source
        
        new_error = np.sum(dist)/source.shape[0]
        
        if abs(error - new_error) < tolerance:
            break
        error = new_error
    
    verts = source.T[:,0:3]
    
    
    floating.vertices = verts
    
    # Transform the normals as well
    #norms = np.concatenate([floating.normals, np.ones((floating.normals.shape[0], 1))], axis=1).T
    #norms = np.linalg.inv(transform).T @ norms
    
    floating.normals = get_normals(floating.vertices, floating.faces)
    
    return floating

def rigid_align_with_points(fixed, floating, fi_landmarks, fl_landmarks, n_iters=100):
    
    """ Rigidly align the floating mesh to the fixed mesh using landmarks 
        in correspondance.
        
        A landmark should look like [id, a, b] where id is the index of
            the triangle containing the landmark and a,b its barycentric coords
    """
    
    if len(fl_landmarks) != len(fi_landmarks):
        
        raise RuntimeError('Must have a corresponance between the landmarks')
    
    if len(fl_landmarks) < 3:
        
        raise RuntimeError('Must have at least 3 landmarks')
        
    # First we get the 3D points from the landmarks using the barycentric coordinates
    fl_points = []
    fi_points = []
    
    for i in range(len(fl_landmarks)):
        fl_land, fi_land = fl_landmarks[i], fi_landmarks[i]
        
        fl_id, fl_a, fl_b = fl_land
        fi_id, fi_a, fi_b = fi_land
        
        # First the floating landmark
        a,b,c = floating.faces[fl_id,:,0]
        va,vb,vc = floating.vertices[a], floating.vertices[b], floating.vertices[c]
        
        fl_point = (fl_a * va) + (fl_b *vb) +((1- fl_a - fl_b) *  vc)
        fl_points.append(fl_point)
        
        # Then the fixed
        a,b,c = fixed.faces[fi_id,:,0]
        va,vb,vc = fixed.vertices[a], fixed.vertices[b], fixed.vertices[c]
        
        fi_point = (fi_a * va) + (fi_b *vb) +((1- fi_a - fi_b) *  vc)
        fi_points.append(fi_point)
        
    fl_points = np.array(fl_points)
    fi_points = np.array(fi_points)
    
    _, R, s, t = estimateRigidTransform(fl_points, fi_points)
    
    #print(R, s, t)
    
    return rigid_align(fixed, floating, n_iters, R, t, s)
