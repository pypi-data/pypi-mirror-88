import pyassimp
import numpy as np
from PyFaceGen.Mesh.Mesh import Mesh

def pyassimp_2_mesh(path):
    
    ''' Converts a .obj file to the custom mesh class '''
    
    
    # Load the scene with pyassimp
    scene = pyassimp.load(path,  
                  processing=pyassimp.postprocess.aiProcess_JoinIdenticalVertices)
    
    # Extract the mesh and convert to our class
    mesh = scene.meshes[0]
    
    vertices = mesh.vertices
        
    if len(mesh.texturecoords) == 0:
        UVs = np.zeros((mesh.vertices.shape[0], 2))
    else:
        UVs = mesh.texturecoords[0,:,0:2]
    normals = mesh.normals
    faces = mesh.faces
    
    mesh = Mesh(vertices, UVs, normals, faces)
    
    return mesh


"""  

THIS CODE SHOULD NOT BE NEEDED
      
def force_pyassimp_uvs(path):
    
    mesh_no_uv = pyassimp_2_mesh(path)
    mesh_uvs_not_joined = obj_2_mesh(path)

    j = 0 # Index of vertex in non-joined mesh
    for i in range(mesh_no_uv.vertices.shape[0]):
        
        v1 = mesh_no_uv.vertices[i]
        v2 = mesh_uvs_not_joined.vertices[j]
        while np.linalg.norm(v1-v2) > 0.01:
            j += 1 
            v2 = mesh_uvs_not_joined.vertices[j]
        mesh_no_uv.UVs[i] = mesh_uvs_not_joined.UVs[j]
        j += 1
        
    return mesh_no_uv
"""
    
