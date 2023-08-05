# Non-rigid iterative closest point on meshes in 1-1 vertex correspondance
# For best results, apply rigid ICP first then call this code


import numpy as np 

from Mesh.Mesh import Mesh
from Mesh.Graph import MeshGraph
from Mesh.Utils import get_normals
from IO.wobj_loader import mesh_2_wobj, wobj_2_mesh
from sklearn.neighbors import NearestNeighbors
from scipy import sparse

ALPHA_SCHEDULE = [70, 10, 5, 2, 1, 0.5, 0.1]#, 0.002, 0.001]
BETA = 80
CHANGE_THRESHOLD = 0.01
MAX_ITERS = 10
NORMAL_THRESHOLD = 0.65
USE_NORMALS = False

class Transform:
    
    """ This class keeps track of all the [Xi: 0<i<n] locally affine transformations """
    
    def __init__(self, n_vertices):
        self.n_vertices = n_vertices
        self.X = np.zeros((4*n_vertices, 3))
        for i in range(n_vertices):
            self.X[4*i:(4*i)+3,:] = np.eye(3)
            
    def apply_transform(self, verts):
        
        """ Applies X to the vertices """
        
        assert verts.shape[0] == self.n_vertices, 'Must give %s vertices, gave %s'%(self.n_vertices, verts.shape[0])
        
        assert verts.shape[1] == 4, "Vertices must be in homogenous form"
        
        transformed = np.ones_like(verts)
        
        for i in range(self.n_vertices):
            
            X_i = self.X[4*i:(4*i)+4].T  # 3 by 4 transform 
            v_ = X_i @ verts[i]          # 3x4 @ 4x1 -> 3x1
            transformed[i,:] = np.array([v_[0], v_[1], v_[2], 1.0])
            
        return transformed
    
    def apply_to_normals(self, norms):
        
        for i in range(self.n_vertices):
            X_i = self.X[4*i:(4*i)+3]  # 3 by 3 transform excluding the translation 
            norms[i] = np.linalg.inv(X_i) @ norms[i]
            norms[i] /= np.linalg.norm(norms[i])
        return norms
        
    
    def __len__(self):
        
        return self.n_verts
    
    def __getitem__(self, idx):
        
        return self.X[4*idx:(4*idx)+4].T
    
    def get_change(self, old_x):
        
        return np.linalg.norm(self.X - old_x)
    
def get_d_loss(tr_verts, fi_verts, weights=None):
    
    """ Gets the E_d loss between transfomed vertices and the corresponding fixed vertices"""
    
    assert tr_verts.shape[0] == fi_verts.shape[0]
    # Handle uniform weighting
    if weights is None:
        weights = np.ones(tr_verts.shape[0])
    
    # Homogenous -> world if present
    tr_verts = tr_verts[:, 0:3]
    fi_verts = fi_verts[:, 0:3]
    
    norms = np.linalg.norm(tr_verts-fi_verts, axis=1)
    norms *= weights
    
    return np.sum(norms)

def get_s_loss(graph, transform, gamma):
    
    """ Gets the E_s (stiffness) loss """
    G = np.diag([1.0,1.0,1.0,gamma])
    count = 0
    for i in graph.edges:
        for j in graph.edges[i]:
            count += np.linalg.norm((transform[i]-transform[j])@G)
    return count

def get_correspondance(fl_verts, fi_verts):    
    
    """
    Gets the corresponding vertices of the fixed mesh given 
    the transformed target mesh 
    
    """    
    nn = NearestNeighbors(n_neighbors=1).fit(fi_verts)
    dist, idx = nn.kneighbors(fl_verts)
    return fi_verts[idx].reshape(-1,4), idx
    

def construct_node_arc_matrix(faces, n_vertices):
    
    """ Builds the node arc incidence matrix for the given graph
        (returns)
            node-arc incidence matrix
            n_edges (int): The number of unique ordered edges 
            
    """
    edges = []
    
    # TODO: Test this
    for face in faces:
        # Every edge should be from lowest index to highest
        sort = face
        edges.append(tuple([sort[0], sort[1]]))
        edges.append(tuple([sort[0], sort[2]]))
        edges.append(tuple([sort[1], sort[2]]))
        
        
    # Remove duplicates
    edges = set(edges)
    n_edges = len(edges)
    print("Number of edges = %s"%(n_edges))
    
    # Template of the matrix
    #M = sparse.lil_matrix((n_edges, n_vertices), dtype='float32')
    M = np.zeros((n_edges, n_vertices), dtype='float32')
    
    # -1 for source +1 for sink
    for idx, edge in enumerate(edges):
        i,j = edge
        M[idx, i] = -1
        M[idx, j] = 1
        
    return M, n_edges

def NRICP(floating, fixed, fl_landmarks=None, fi_landmarks=None, verbose=False):
    
    """ Perform non-rigid ICP to register floating mesh to fixed 
    
        (params):
            floating (Mesh): The mesh to be aligned
            fixed (Mesh): The target mesh that will not change
            (fl_landmarks) (list): The floating landmarks of the form
                [(idx, a ,b)] where idx is the index of the triangle in the face
                and a and b barycentric coordinates 
            (fi_landmarks) (list): Same as fl_landmarks but for the fixed mesh
            verbose (bool): If to print debugging information
    """
    
    # Get the vertices and convert to homogenous coordinates
    fl_verts = floating.vertices
    fi_verts = fixed.vertices
    
    n_vertices = fl_verts.shape[0]
    n_vertices_target = fi_verts.shape[0]
    
    fl_verts = np.concatenate((fl_verts, np.ones((fl_verts.shape[0],1), dtype='float32' )), axis=1)
    fi_verts = np.concatenate((fi_verts, np.ones((fi_verts.shape[0],1), dtype='float32' )), axis=1)
    
    # Initalise the transforms
    transform = Transform(fl_verts.shape[0])
    
    # ---------------------------- Landmarks ------------------------------#
    if verbose:
        print("Processing landmarks")
    
    # Prepare the landmarks, they now must map single vertices in the source 
    # to points on the surface of the target
    
    if (fi_landmarks is not None) and (fl_landmarks is not None): 
    
        fi_landmark_points = []
        fl_landmark_indices = []
        for i in range(len(fi_landmarks)):
            fl_land, fi_land = fl_landmarks[i], fi_landmarks[i]
            
            fl_id, fl_a, fl_b = fl_land
            fi_id, fi_a, fi_b = fi_land
            
            # First the floating landmark, we want the closest vertex only
            a,b,c = floating.faces[fl_id,:,0]
            fl_c = 1-(fl_a+fl_b)
            
            # Smallest barycentric corresponds to closest
            if fl_a < fl_c and fl_a < fl_b:
                fl_landmark_indices.append(a)
            
            elif fl_b < fl_a and fl_b < fl_c:
                fl_landmark_indices.append(b)
            
            elif fl_c < fl_a and fl_c < fl_b:
                fl_landmark_indices.append(c)
            
            # Now we do fixed landmarks, here we want the 3D point
            a,b,c = fixed.faces[fi_id,:,0]
            va,vb,vc = fixed.vertices[a], fixed.vertices[b], fixed.vertices[c]
            
            fi_point = (fi_a * va) + (fi_b *vb) +((1- fi_a - fi_b) *  vc)
            fi_landmark_points.append(fi_point)
            
        # Vectorise
        fi_landmark_points = np.array(fi_landmark_points)
        fl_landmark_indices = np.array(fl_landmark_indices)

    # -------------------- Loop over stiffness ------------------------ #

    G = np.float32(np.diag([1.0,1.0,1.0,1.0]))
    
    if verbose:
        print("Computing node arc matrix")
    
    graph = MeshGraph(floating)
    M, n_edges = construct_node_arc_matrix(floating.faces[:,:,0], n_vertices)
    M = sparse.csr_matrix(M)
    G = sparse.csr_matrix(G)
    
    MG = sparse.kron(M,G)
    
    for alpha in ALPHA_SCHEDULE:

        if verbose:
            print("Using stiffness %s"%(alpha))
        
        # Keep track of changes in the transform
        change = np.inf
        n_iter = 0 # Early stop if too many iterations
        
        while change > CHANGE_THRESHOLD:
            
            
                        
            # 2-step algorithm, first is to get correspondance then optimal X
            transformed = transform.apply_transform(fl_verts)
            t_norms = transform.apply_to_normals(floating.normals)
            # Get the corresponances
            corresponances, idx = get_correspondance(fl_verts, fi_verts)
            norm_corr = fixed.normals[idx]
            
            if verbose:
                print('D loss: ', get_d_loss(transformed, corresponances))
                print('Stiffness loss: ', get_s_loss(graph, transform, 1.0))

            
            # TODO: Weights might not always be uniform
            weights = np.float32(np.ones((n_vertices,)))
            
            # Adjust weights by comparing normals
            if USE_NORMALS:
                
                for n_weight in range(n_vertices):
                    
                    target_norm = norm_corr[n_weight]
                    new_norm = t_norms[n_weight]
                    
                    cos_theta = target_norm.dot(new_norm.T)
                    theta = np.arccos(cos_theta)
                    if theta > NORMAL_THRESHOLD:
                        weights[n_weight] = 0
                    
            
            W = np.float32(np.diag(weights))
            
            # Start computing the matricies we need
            B = np.zeros((4 * n_edges + n_vertices, 3), dtype=np.float32)
            D = np.zeros((n_vertices, n_vertices*4), dtype=np.float32)
            U = corresponances

            
            for i in range(n_vertices):
                D[i, 4*i:4*i + 4] = fl_verts[i]
                
            B[4 * n_edges: (4 * n_edges + n_vertices), :] = (W @ U)[:, 0:3]
            
            D = sparse.csr_matrix(D)
            
            if verbose:
                print("Computing ATA")
                
            W = sparse.csr_matrix(W)
            A = sparse.vstack([alpha * MG, W@D])  
            
            if (fi_landmarks is not None) and (fl_landmarks is not None): 
                
                UL = fi_landmark_points
                DL = BETA * D[fl_landmark_indices]
                A = sparse.vstack([A, DL])
                B = np.vstack([B, UL])
            
            if verbose:
                print("Solving")
            X = sparse.linalg.spsolve(A.T.dot(A),A.T.dot(B))
            
            #print(X, transform.X)
            change = np.linalg.norm(X-transform.X)
            transform.X = X
            if n_iter > MAX_ITERS:
                break
            n_iter += 1
            
    out_faces = floating.faces
    out_uvs = floating.UVs
    out_normals = floating.normals 
    
    out_vertices = transform.apply_transform(fl_verts)[:, 0:3]
    return Mesh(out_vertices, out_uvs, out_normals, out_faces), transform
            
            
    
