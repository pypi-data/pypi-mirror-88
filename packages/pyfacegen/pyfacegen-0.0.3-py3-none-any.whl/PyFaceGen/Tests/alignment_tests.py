import numpy as np

from PyFaceGen.Mesh.Mesh import Mesh
from PyFaceGen.Mesh.Graph import MeshGraph
from PyFaceGen.IO.wobj_loader import wobj_2_mesh, mesh_2_wobj
from PyFaceGen.Alignment.RigidAlignment import rigid_align, rigid_align_with_points
from PyFaceGen.Alignment.landmarks import read_wrap_landmark
from PyFaceGen.Alignment.NRICP import NRICP, Transform, get_d_loss, get_s_loss

def rigid_test():
    
    fixed = wobj_2_mesh('Data/Faces/rig_neutral.obj')
    floating = wobj_2_mesh('Data/Faces/lyhm_1.obj')
    
    fl_land = read_wrap_landmark('Data/Faces/flame_landmarks.txt')
    fi_land = read_wrap_landmark('Data/Faces/rig_landmarks.txt')
    
    mesh = rigid_align_with_points(fixed, floating, fi_land, fl_land)
    mesh_2_wobj(mesh, "Data/Faces/align.obj")

def NRICP_transform_test():
    
    # Load a cube in homogenous co-ordinates
    cube = wobj_2_mesh('Data/Tests/primatives/cube.obj') 
    V = np.concatenate((cube.vertices, np.ones((cube.vertices.shape[0], 1))), axis=1)
    transform = Transform(cube.vertices.shape[0])
    V_ = transform.apply_transform(V)

    assert np.sum(abs(V - V_)) == 0    

def NRICP_d_loss_test():
    
    # Load a cube in homogenous co-ordinates
    cube = wobj_2_mesh('Data/Tests/primatives/cube.obj') 
    V = np.concatenate((cube.vertices, np.ones((cube.vertices.shape[0], 1))), axis=1)
    transform = Transform(cube.vertices.shape[0])
    V_ = transform.apply_transform(V)

    assert get_d_loss(V,V_) == 0
    
    V_[0,0] = V_[0,0]+1 
    assert get_d_loss(V, V_) == 1
    
def NRICP_g_loss_test():
    
    # Load a cube in homogenous co-ordinates
    cube = wobj_2_mesh('Data/Tests/primatives/cube.obj') 
    V = np.concatenate((cube.vertices, np.ones((cube.vertices.shape[0], 1))), axis=1)
    transform = Transform(cube.vertices.shape[0])
    V_ = transform.apply_transform(V)
    graph = MeshGraph(cube)
    assert get_s_loss(graph, transform, 1) == 0
    
def NRICP_test():
    
    cube = wobj_2_mesh('Data/Tests/primatives/cube.obj') 
    sphere = wobj_2_mesh('Data/Tests/primatives/sphere.obj')
    cube_landmarks = read_wrap_landmark('Data/Tests/primatives/cube_landmarks.txt')
    sphere_landmarks = read_wrap_landmark('Data/Tests/primatives/sphere_landmarks.txt')
    sphere_cube = NRICP(sphere, cube, sphere_landmarks, cube_landmarks, verbose=True)
    mesh_2_wobj(sphere_cube , 'Data/Tests/primatives/sphere_cube.obj')
    
def non_rigid_test():
    
    NRICP_transform_test()
    NRICP_d_loss_test()
    NRICP_g_loss_test()
    NRICP_test()
