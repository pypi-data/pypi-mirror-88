from PyFaceGen.Mesh.Mesh import Mesh

class MeshGraph:
    
    def __init__(self, mesh):
        
        """ A graph represntation of a mesh """
        
        self.vertices = mesh.vertices
        self.edges = {i:set({}) for i in range(len(mesh.vertices))}
        self.n_vertices = self.vertices.shape[0]
        self.n_edges = 0
        
        for face in mesh.faces[:,:,0]:
            self.edges[face[0]].add(face[1])
            self.edges[face[0]].add(face[2])
            
            self.edges[face[1]].add(face[0])
            self.edges[face[1]].add(face[2])
            
            self.edges[face[2]].add(face[1])
            self.edges[face[2]].add(face[0])
            
            self.n_edges += 6
            
    def print(self):
        
        for key in self.edges:
            
            line = "Index %s, value %s: {"%(key, self.vertices[key])
            for edge in self.edges[key]:
                line += str(edge)+" "
                
            line+= "}"
            print(line)

    
    
