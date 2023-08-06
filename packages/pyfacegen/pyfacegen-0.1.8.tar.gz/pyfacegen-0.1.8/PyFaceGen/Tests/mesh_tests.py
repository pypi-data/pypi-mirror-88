from PyFaceGen.Mesh.Mesh import Mesh
from PyFaceGen.Mesh.Graph import MeshGraph
from PyFaceGen.IO.wobj_loader import wobj_2_mesh

def GraphTest():
    
    cube = wobj_2_mesh('Data/Tests/primatives/cube.obj')
    graph = MeshGraph(cube)
    assert graph.edges[0] == set((1,2,4,5,6))
