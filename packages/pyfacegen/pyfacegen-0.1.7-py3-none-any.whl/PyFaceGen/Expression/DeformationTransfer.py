from PyFaceGen.Mesh.Mesh import Mesh
from PyFaceGen.Mesh.Utils import get_normals
import numpy as np

def check_topology_is_shared(a,b) -> bool:
    
    """ Checks if two meshes share the same number of vertices and faces """
    
    if a.vertices.shape != b.vertices.shape:
        return False
    if a.faces.shape != b.faces.shape:
        return False
    return True

def deformation_transfer(source_neutral, source_expression, target_neutral) -> Mesh:
    
    """ Using deformation transfer for triangle meshes (Sumner & Popovic)
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.126.6553&rep=rep1&type=pdf
    Apply the expression of a source identity to a target identity
    All meshes must share a common topology
    
    (params):
        source_neutral (Mesh): The source identity in neutral expression
        source_expression (Mesh): The source identity with target expression
        target_neutral (Mesh): The identity of the target with neutral expression
    
    (returns):
        (Mesh): The target identity with the source expression transferred onto it
    """
    
    # Get the number of vertices and faces
    n_faces = source_neutral.faces.shape[0]
    n_verts = source_neutral.vertices.shape[0]
    
    # Ensure that the meshes are in the same topology
    if not (check_topology_is_shared(source_neutral, source_expression) 
            and check_topology_is_shared(source_neutral, target_neutral)):
        raise RuntimeError('Meshes must share a common topology')
    
    print("Computing B Matrix")
    # B matrix
    B = np.zeros((n_faces * 3, 3))
    
    # Create the B matrix iterating over faces
    for f_idx in range(n_faces):
        
        # Get the source neutral vertices in this face
        a,b,c = source_neutral.faces[f_idx, :, 0]
        v1 = source_neutral.vertices[a, :]
        v2 = source_neutral.vertices[b, :]
        v3 = source_neutral.vertices[c, :]
        
        # v4 calculation
        cross = np.cross((v2 - v1), (v3 - v1))  
        v4 = v1 + cross/np.sqrt(np.linalg.norm(cross))
        
        # V matrix
        V = np.zeros((3,3))
        V[:,0] = v2 - v1
        V[:,1] = v3 - v1
        V[:,2] = v4 - v1
        
        # Get the source expression vertices in this face
        v1_ = source_expression.vertices[a, :]
        v2_ = source_expression.vertices[b, :]
        v3_ = source_expression.vertices[c, :]
        
        # v4 bar calculation
        cross_ = np.cross((v2_ - v1_), (v3_ - v1_))  
        v4_ = v1_ + cross/np.sqrt(np.linalg.norm(cross_))
        
        # V bar matrix
        V_ = np.zeros((3,3))
        V_[:,0] = v2_ - v1_
        V_[:,1] = v3_ - v1_
        V_[:,2] = v4_ - v1_
        
        # Q matrix calculation
        Q = V_ @ np.linalg.inv(V)
        QT = Q.T
        
        # Update B
        offset = f_idx * 3
        B[offset: offset+3, :] = QT
    
    print("Calculating A Matrix")
    A = np.zeros((n_faces * 3, n_faces + n_verts))
    for f_idx in range(n_faces):
        
        # Get the target neutral vertices in this face
        a,b,c = target_neutral.faces[f_idx, :, 0]
        v1 = target_neutral.vertices[a, :]
        v2 = target_neutral.vertices[b, :]
        v3 = target_neutral.vertices[c, :]
        
        # v4 calculation
        cross = np.cross((v2 - v1), (v3 - v1))  
        v4 = v1 + cross/np.sqrt(np.linalg.norm(cross))  
        
        # V matrix
        V = np.zeros((3,3))
        V[:,0] = v2 - v1
        V[:,1] = v3 - v1
        V[:,2] = v4 - v1
        
        V_inv = np.linalg.inv(V)

        # Update A
        offset = f_idx * 3
        for col in range(3):
            A[offset+col, a] = -(V_inv[0, col] + V_inv[1, col] + V_inv[2, col])
            A[offset+col, b] = V_inv[0, col]
            A[offset+col, c] = V_inv[1, col]
            A[offset+col, n_verts + f_idx] = V_inv[2, col]
            
    print("Setting up linear system")
    AT = A.T
    ATA = AT @ A
    ATB = AT @ B
    
    # Clear memory
    del(A)
    del(B)
    del(AT)
    
    print("Solving linear system")
    
    X = np.linalg.solve(ATA, ATB)
    # Clear memory
    del(ATA)
    del(ATB)
    
    new_verts = np.zeros_like(target_neutral.vertices)
    new_uvs = np.array(target_neutral.UVs)
    new_faces = np.array(target_neutral.faces)


    for v_idx in range(n_verts):
        new_verts[v_idx, :] = X[v_idx, :]
        
        
    # TODO: Update these via X
    new_normals = get_normals(new_verts, new_faces)
    
    # For some reason the new mesh need centering?
    target_centroid = np.mean(target_neutral.vertices, axis=0)
    new_centroid = np.mean(new_verts, axis=0)
    new_verts -= (new_centroid - target_centroid)
    
    return Mesh(new_verts, new_uvs, new_normals, new_faces)
        
    
    
        
        