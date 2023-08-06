# python version 3.8
# This code describes the mesh class which we will work with

import numpy as np

class Mesh:
    
    def __init__(self, vertices, UVs, normals, faces, dtype='float32'):
        
        ''' The custom Mesh class that we will work with
        
            (params):
                verticies (ndarray): The positions of the vertices in 3D
                UVs (ndarray): The UV co-ordinates of each vertex
                normals (ndarray): The normals to each vertex
                faces (ndarray nFacesx3x3): The indexes of the vertices making up each face
                    faces[:,:,0] is positions, faces[:,:,1] is UVs, faces[:,:,2] is normals
                
        '''
        
        self.vertices = np.array(vertices, dtype=dtype)
        self.UVs = np.array( UVs, dtype=dtype)
        self.normals = np.array(normals, dtype=dtype)
        self.faces = faces
        
        self.n_vertices = len(self.vertices)
        
        self.order = []
        
    def update_buffer(self):
        
        ''' Updates the internal buffer that is used GLFW '''
        
        buffer = []
        for idx in self.faces.shape[0]:
            
            face = self.faces[idx,:,:] # 3x3
            
            buffer.extend(self.vertices[face[0,0]])
            buffer.extend(self.UVs[face[0,1]])
            buffer.extend(self.normals[face[0,2]])
            
            buffer.extend(self.vertices[face[1,0]])
            buffer.extend(self.UVs[face[1,1]])
            buffer.extend(self.normals[face[1,2]])
            
            buffer.extend(self.vertices[face[1,0]])
            buffer.extend(self.UVs[face[1,1]])
            buffer.extend(self.normals[face[2,2]])
            
        self.buffer = np.array(buffer, dtype='float32')
        
    def apply_translation(self, vector):
        
        ''' Applies a translation of the mesh by a given vector 
        
            (params): 
                vector (3x1 numpy array): The 3D translation vector 
        '''
        
        # Note that only vertex positions are altered, we do not change the UV
        # or the normals
        self.vertices += vector
        
        
    def apply_transformation(self, matrix):
        
        ''' Applies a linear transformation of the mesh defined by
            a given 3x3 matrix 
        
            (params): 
                matrix (3x3 numpy array): The 3D transformation matrix 
        '''
        
        # Here the normals need to be updated as well as the positions
        self.vertices = self.vertices @ matrix
        norm_transform = np.linalg.inv(matrix.T)        
        self.normals = self.normals @ norm_transform
        
    
        