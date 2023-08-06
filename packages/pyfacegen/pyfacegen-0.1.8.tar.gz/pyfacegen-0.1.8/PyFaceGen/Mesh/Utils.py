# python version 3.8
# This code is a collection of utility functions

import numpy as np
from math import sin, cos
from PyFaceGen.Mesh.Mesh import Mesh
from PyFaceGen.Mesh.Graph import MeshGraph

def cross(a,b):
    
    ''' A 2D cross product '''
    return a[0]*b[1] - a[1]*b[0]


def dot(a,b):
    
    ''' A 2D dot product '''
    return a[0]*b[0] + a[1]*b[1]


class TriangleTester:
    
    def __init__(self, a, b, c):
        
        ''' A class for testing if points belong to the interior of a triangle
            in two dimensions 
            
            (params):
                a, b, c (array-like): The three points in 2D that 
                        describe the triangle
        '''
        
        # By precalculating everything not involving the test point we can
        # speed up the code significantly
        self.ab = cross(a,b)
        self.bc = cross(b,c)
        self.ca = cross(c,a)
        
        self.d = max(1e-14, self.ab + self.bc + self.ca) # To avoid div by 0
        self.scale = 1/self.d
        
        self.amb = a-b
        self.bmc = b-c
        self.cma = c-a
        
        
    def test(self, p):
        
        ''' Tests if the point p is within the interior of the triangle defined
            for this class and gives the barycentric co-ordinates if it is
            (params):
                p (array-like): The point that is to be tested
            (returns):
                w_a, w_b, w_c (float): The barycentric co-ordinates
        '''
        
        if (abs(self.d) > 1e-13):
            
            w_a = self.scale * (self.bc + cross(p, self.bmc))
            w_b = self.scale * (self.ca + cross(p, self.cma))
            w_c = self.scale * (self.ab + cross(p, self.amb))
            
            is_in = (0 <= w_a <= 1 and 0 <= w_b <= 1 and 0 <= w_c <= 1 )
            
            return (is_in, w_a, w_b, w_c)
        
        else:
            return (False, 0,0,0)
        
        
class MultiTriangleTester:
    
    def __init__(self, a, b, c, width, height):
        
        ''' A class for testing if many points belong to the interior of a triangle
            in two dimensions 
            
            (params):
                a, b, c (array-like): The three points in 2D that 
                        describe the triangle
        '''
        
        # By precalculating everything not involving the test point we can
        # speed up the code significantly
        self.ab = cross(a,b)
        self.bc = cross(b,c)
        self.ca = cross(c,a)
        
        self.d = max(1e-14, self.ab + self.bc + self.ca) # To avoid div by 0
        self.scale = 1/self.d
        
        self.amb = a-b
        self.bmc = b-c
        self.cma = c-a
        
        self.width = width
        self.height = height
        
        # Vectorise everthing and let numpy do the heavy lifting
        self.AMB = np.zeros((height, width, 3))
        self.BMC = np.zeros((height, width, 3))
        self.CMA = np.zeros((height, width, 3))
        for u in range(width):
            for v in range(height):
                self.AMB[v,u,0:2] = a-b
                self.BMC[v,u,0:2] = b-c
                self.CMA[v,u,0:2] = c-a
        
    def test(self, P):
        
        ''' Tests if the points P are within the interior of the triangle defined
            for this class and gives the barycentric co-ordinates they are
            (params):
                p (ndarray, WxHx2): The points that are to be tested
            (returns):
                is_in (ndarray, WxH): If each point is in the triangle
                w_a, w_b, w_c (ndarray, WxH): The barycentric co-ordinates
        '''
        zeros = np.zeros((self.width, self.height))
        
        if (abs(self.d) > 1e-13):
            
            P = np.concatenate((P, np.zeros((self.height, self.width, 1))), axis=2)
            w_a = self.scale * (self.bc + np.cross(P, self.BMC))[:,:,2]
            w_b = self.scale * (self.ca + np.cross(P, self.CMA))[:,:,2]
            w_c = self.scale * (self.ab + np.cross(P, self.AMB))[:,:,2]
            
            is_in = 0 <= w_a
            is_in &= w_a <= 1
            is_in &= 0 <= w_b
            is_in &= w_b <= 1
            is_in &= 0 <= w_c
            is_in &= w_c <= 1
            #is_in = (0 <= w_a <= 1 and 0 <= w_b <= 1 and 0 <= w_c <= 1 )
            
            return (is_in, w_a, w_b, w_c)
        
        else:
            return (False, zeros,zeros,zeros)
        
        
def get_normals(vertices, faces):
    
    ''' This code calculates vertex normals without smoothing groups (yet) 
        
        (params):
            vertices (ndarray, Nx3): The vertices
            faces (ndarray, Nx3x3): The faces 
        (returns):
            normals (ndarray, Nx3): The normals listed in the same order 
                                        as the vertices
                                        
    '''
    
    normals = np.zeros((np.max(faces[:,:,2] + 1), 3))
    f_counts = np.zeros((np.max(faces[:,:,2] + 1), 3)) # Counts for averaging
    for face in faces:
        
        ia,ib,ic = face[:, 0]
        a,b,c = vertices[ia], vertices[ib], vertices[ic]
        na, nb, nc = face[:, 2]
        
        B,C = b-a,c-a
        n = np.cross(B,C)
        normals[na] += n
        f_counts[na] += 1
        normals[nb] += n
        f_counts[nb] += 1
        normals[nc] += n
        f_counts[nc] += 1
        
    for i in range(len(f_counts)):
        
        normals[i] /= f_counts[i]
        
    for normal in normals:

        normal /= np.linalg.norm(normal)
        
    return normals



def apply_rpy(mesh, roll, pitch, yaw):
    
    ''' Rotates, in-place, the mesh by given roll, pitch yaw (in radians)'''
    
    R_z = np.array([[cos(yaw), -sin(yaw), 0],
                    [sin(yaw), cos(yaw), 0 ],
                    [0,          0,       1]
        ])
    
    R_y = np.array([[cos(pitch), 0, sin(pitch)],
                    [0       , 1,        0],
                    [-sin(pitch), 0, cos(pitch)]
        ])
    
    R_x= np.array([[1, 0, 0],
                  [0, cos(roll), -sin(roll)],
                  [0, sin(roll), cos(roll)]
        ])
        
    mesh.apply_transformation(R_x)
    mesh.apply_transformation(R_y)
    mesh.apply_transformation(R_z)
    
    
"""
    
def fix_culled_backface(mesh: Mesh, proportion_to_flip: float = 0.7) -> Mesh:
    
    """ """ Fixes issues on a given mesh where some faces have inverted normals """ """
    
    graph = MeshGraph(mesh)
    
    # First normalise all normals
    for i in range(mesh.normals.shape[0]):
        
        mesh.normals[i] /= np.linalg.norm(mesh.normals[i])
    
    # To convert between vertex index and normal index
    vert2norm = np.zeros((mesh.n_vertices,), dtype='int')
    
    for face in mesh.faces:
        fv = face[:,0]
        fn = face[:,2]
        
        av,bv,cv = fv
        an,bn,cn = fn
        
        vert2norm[av] = an
        vert2norm[bv] = bn
        vert2norm[cv] = cn
        
    
    for i in range(mesh.n_vertices):
        # Get this normal
        normal = mesh.normals[vert2norm[i]]
        
        # Get the normals of the n-hop neighbourhood
        neighbourhood = np.array(list(graph.edges[i]), dtype='int')
        n_norms = mesh.normals[vert2norm[neighbourhood]]
        
        # Get the angle between this normal and neighbours normals
        n_copy1 = np.zeros((n_norms.shape[0], ))
        for j in range(n_norms.shape[0]):
            n_copy1[j] = np.dot(n_norms[j], normal)
            n_copy1[j] = np.arccos(n_copy1[j])
        # Calculate the proportion of neighbours that are in the opposite direction
        proprtion_wrong_dir = np.sum(n_copy1 > 3.1415/2)/ n_norms.shape[0]
        if proprtion_wrong_dir > proportion_to_flip:
            # Flip the normal
            mesh.normals[vert2norm[i]] *= -1
            print('Flipped')
            
"""
        
        
      