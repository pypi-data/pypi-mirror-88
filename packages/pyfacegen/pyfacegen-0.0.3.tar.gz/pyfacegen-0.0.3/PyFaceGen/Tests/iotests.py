#from PyFaceGen.IO.ply_loader import ply_2_mesh, mesh_2_ply
from PyFaceGen.IO.wobj_loader import wobj_2_mesh, mesh_2_wobj
import numpy as np
# ---------------------- Ply Tests ------------------------- #

'''# Test case 1 - can we load a simple obj
def plytestsimple():
    mesh = ply_2_mesh('Data/Tests/ply.ply')
    assert mesh.vertices[0][0] != 0


# Test case 2 - can we load a ply file with binary encoding    
def plytestbinary():
    
    mesh = ply_2_mesh('Data/Tests/ply_binary.ply')
    assert mesh.vertices[0][0] != 0
    
# Run all ply tests    
def plytests():
    
    plytestsimple()
    plytestbinary()'''

# Test case 1 - can we load a simple wavefront obj file
def wobjtestsimple():
    mesh = wobj_2_mesh('Data/Tests/wobj.obj')
    assert mesh.vertices[0][0] != 0

# Test case 2 - does reading/writing UVs work    
def wobjtestUVs():
    mesh = wobj_2_mesh('Data/Tests/wobj.obj')
    assert mesh.UVs[0][0] != 0
    mesh.UVs[0][0] = 0.5
    mesh_2_wobj(mesh, 'Data/Tests/wobj_uv.obj')
    mesh = wobj_2_mesh('Data/Tests/wobj_uv.obj')
    assert  mesh.UVs[0][0] == 0.5
    
# Test case 2 - does reading/writing normals work    
def wobjtestnormals():
    mesh = wobj_2_mesh('Data/Tests/wobj.obj')
    print(mesh.faces.shape)
    assert mesh.normals[0][0] != 0
    mesh.normals[0][0] = 0.5
    mesh_2_wobj(mesh, 'Data/Tests/wobj_norm.obj')
    mesh = wobj_2_mesh('Data/Tests/wobj_norm.obj')
    assert  mesh.normals[0][0] == 0.5
    

# Run all wobj tests
def wobjtests():
    wobjtestsimple()
    wobjtestUVs()
    wobjtestnormals()

