from PyFaceGen.Mesh.Mesh import Mesh
from PyFaceGen.Mesh.Graph import MeshGraph

import numpy as np

def get_components_given_vertex(mesh, vert):
    
    graph = MeshGraph(mesh)
    
    component = set([])
    frontier = set([vert])
    while len(frontier) != 0:
        x = frontier.pop()
        component.add(x)
        for sink in graph.edges[x]:
            frontier.add(sink)
        print(len(frontier))    
    return component

        
def get_components(mesh):
    
    # The idea is that we will create components of verex indicies
    # and merge them if there is a face that contains verticies from different components
    
    components = []
    faces = mesh.faces[:,:,0]
    
    for i, face in enumerate(faces):
        a,b,c = face
        a_comp, b_comp, c_comp = -1,-1,-1 # -1 means no exiting component contains them
        
        # Find which, if any, components each a,b and c already belong to
        for j,component in enumerate(components):
            
            # Iterate over each vertex
            for vertex in component:
                
                if vertex == a:
                    a_comp = j
                if vertex == b:
                    b_comp = j
                if vertex == c:
                    c_comp = j
                    
        # Now we consider a few cases
        
        # Firstly if none of the vertices are already assigned to a component
        if a_comp == b_comp == c_comp == -1:
            # In this case, make a new one for them
            components.append([a,b,c])
            
        # Next if only one vertex belongs to a component then assign all other vertices to it
        elif a_comp != -1 and b_comp == c_comp == -1:
            components[a_comp].append(b)
            components[a_comp].append(c)
            
        elif b_comp != -1 and a_comp == c_comp == -1:
            components[b_comp].append(a)
            components[b_comp].append(c)
            
        elif c_comp != -1 and b_comp == a_comp == -1:
            components[c_comp].append(b)
            components[c_comp].append(a)
            
        # Next if any two vertices already have a component 
        # If its the same we add the third vertex to it
        # If not we merge the components and add the other vertex
        elif a_comp != -1 and b_comp != -1 and c_comp == -1:
            # Merge and delete
            if a_comp != b_comp:
                # Add all of component b to component a along with c and remove component b
                components[a_comp].extend(components[b_comp])
                components[a_comp].append(c)
                components.pop(b_comp)
            # Just add the remaining vertex
            else:
                components[a_comp].append(c)
                
        elif b_comp != -1 and c_comp != -1 and a_comp == -1:
            # Merge and delete
            if b_comp != c_comp:
                # Add all of component c to component b along with a and remove component c
                components[b_comp].extend(components[c_comp])
                components[b_comp].append(a)
                components.pop(c_comp)
            # Just add the remaining vertex
            else:
                components[b_comp].append(a)
        elif c_comp != -1 and a_comp != -1 and b_comp == -1:
            # Merge and delete
            if c_comp != a_comp:
                # Add all of component a to component c along with b and remove component a
                components[c_comp].extend(components[a_comp])
                components[c_comp].append(b)
                components.pop(a_comp)
            # Just add the remaining component
            else:
                components[c_comp].append(b)
                
        # Finally if all vertices already belong to components
        # Merge any components that are seperate
        elif a_comp != -1 and b_comp != -1 and c_comp != -1:
            
            if a_comp == b_comp == c_comp:
                continue #do nothing, all already fine
            
            # Merge component c into the component containing both a and b 
            if a_comp == b_comp != c_comp:
                components[a_comp].extend(components[c_comp])
                components.pop(c_comp)
                
            # Merge component a into the component containing both b and c 
            elif a_comp != b_comp == c_comp:
                components[c_comp].extend(components[a_comp])
                components.pop(a_comp)
                
            # Merge component b into the component containing both a and c 
            elif a_comp == c_comp != b_comp:
                components[a_comp].extend(components[b_comp])
                components.pop(b_comp)
            
            # Everything is different, we have to be careful removing 2 components
            elif a_comp != b_comp != c_comp:
                components[a_comp].extend(components[b_comp])
                components[a_comp].extend(components[c_comp])
                
                copy = [] # We need to do this as a copy as removing would change indicies
                for c_id, component in enumerate(components):
                    if c_id not in [b_comp, c_comp]:
                        copy.append(component)
                components = copy
                
            else:
                # We shouldn't get here if this code is correct
                raise RuntimeError('Components %s, %s, %s should not be valid'%(a_comp, b_comp, c_comp))
        else:
            # We shouldn't get here if this code is correct
            raise RuntimeError('Components %s, %s, %s should not be valid'%(a_comp, b_comp, c_comp))

    return components

def split_by_components(mesh, components):
    
    # Convert vertices
    vertices = [mesh.vertices[component] for component in components]
    normals = [[] for component in components]
    uvs = [[] for component in components]
    faces = [[] for component in components]
    uv_ids = [[] for component in components]
    n_ids = [[] for component in components]
    
    for face in mesh.faces:
        a,b,c = face[:,0] # The split is based on position
        ta,tb,tc = face[:,1] # We still want the UV though
        na,nb,nc = face[:,2] # And normals
        
        for i,component in enumerate(components):
            
            # Find the component assositated with this face
            id_a, id_b, id_c = -1,-1,-1  # These will be -1 if this is the wrong componemt
            
            for j,v in enumerate(component):
                if v==a:
                    # We have found the right component
                    id_a = j # j will be the index of the vertex in the split vertex list
                elif v==b:
                    id_b = j
                elif v==c:
                    id_c = j
            if id_a == id_b == id_c == -1:
                # Wrong component 
                continue
            else:
                
                # We have found the component this face is in
                if -1 in [id_a, id_b, id_c]:
                    # This is a failsafe, shouldn't happen
                    raise RuntimeError('This shouldnt happen, components has failed')
                    
                uv_a, uv_b, uv_c = face[:,1]
                n_a, n_b, n_c = face[:,2]
                
                # Ensure we dont duplicate the uvs
                if uv_a not in uv_ids[i]:
                    uv_ids[i].append(uv_a)
                    uvs[i].append(mesh.UVs[uv_a])
                    uv_id_a = len(uvs[i]) - 1
                else:
                    uv_id_a = uv_ids[i].index(uv_a)
                    
                if uv_b not in uv_ids[i]:
                    uv_ids[i].append(uv_b)
                    uvs[i].append(mesh.UVs[uv_b])
                    uv_id_b = len(uvs[i]) - 1
                else:
                    uv_id_b = uv_ids[i].index(uv_b)
                    
                if uv_c not in uv_ids[i]:
                    uv_ids[i].append(uv_c)
                    uvs[i].append(mesh.UVs[uv_c])
                    uv_id_c = len(uvs[i]) - 1
                else:
                    uv_id_c = uv_ids[i].index(uv_c)
                    
                
                # Ensure we dont duplicate the normals
                if n_a not in n_ids[i]:
                    n_ids[i].append(n_a)
                    normals[i].append(mesh.normals[n_a])
                    n_id_a = len(normals[i]) - 1
                else:
                    n_id_a = n_ids[i].index(n_a)
                    
                if n_b not in n_ids[i]:
                    n_ids[i].append(n_b)
                    normals[i].append(mesh.normals[n_b])
                    n_id_b = len(normals[i]) - 1
                else:
                    n_id_b = n_ids[i].index(n_b)
                    
                if n_c not in n_ids[i]:
                    n_ids[i].append(n_c)
                    normals[i].append(mesh.normals[n_c])
                    n_id_c = len(normals[i]) - 1
                else:
                    n_id_c = n_ids[i].index(n_c)
                    
                
                    
                
                faces[i].append(np.array([[id_a,id_b,id_c],
                                          [uv_id_a, uv_id_b, uv_id_c],
                                          [n_id_a, n_id_b, n_id_c]]).T)

                
    return [Mesh(np.array(vertices[i]), np.array(uvs[i]), np.array(normals[i]), np.array(faces[i])) for i in range(len(components))]
