# Non-rigid iterative closest point on meshes in 1-1 vertex correspondance
# For best results, apply rigid ICP first then call this code

# Algorithm implimentation of https://www.researchgate.net/publication/200172513_Optimal_Step_Nonrigid_ICP_Algorithms_for_Surface_Registration
# Sparse idea from 
# Schedules for training from https://github.com/shubhamag/non_rigid_icp/blob/master/nicp_meshes.py
# As well as weighting points by the normal relative to the K nearest neighbours

import numpy as np 

from PyFaceGen.Mesh.Mesh import Mesh
from PyFaceGen.Mesh.Graph import MeshGraph
from PyFaceGen.Mesh.Utils import get_normals
from PyFaceGen.IO.wobj_loader import mesh_2_wobj, wobj_2_mesh
from sklearn.neighbors import NearestNeighbors
from scipy import sparse
from sksparse.cholmod import cholesky_AAt

ALPHA_SCHEDULE = [50,35,20,15, 7,3,2,]#1]#, 0.5]#, 0.1]#, 0.05]
BETA_SCHEDULE = [15,14, 3, 2, 0.5, 0,0]# ,0]#,0]#,0]#, 0.05]
CHANGE_THRESHOLD = 0.01
NORMAL_THRESHOLD = 0.32  # The lower this value the more verticies are ignored
USE_NORMALS = True
K = 30
FIX_NORMALS = False
DISCARD = 10 # Discard all matches that are worse than this

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
            count += np.linalg.norm((transform[4*i: 4*i + 4, :]-transform[4*j: 4*j + 4, :]).T @ G)
    return count

def get_correspondance(fl_verts, fi_verts):    
    
    """
    Gets the corresponding vertices of the fixed mesh given 
    the transformed target mesh 
    
    """    
    nn = NearestNeighbors(n_neighbors=1).fit(fi_verts)
    dist, idx = nn.kneighbors(fl_verts)
    return fi_verts[idx].reshape(-1,4), idx
    

def construct_MG(faces, n_vertices, gamma):
    
    """ Builds the knoeneker product MG of node arc incidence matrix for the given graph
    with the diagonal matrix [1,1,1,gamma]
        (returns)
            node-arc incidence matrix
            n_edges (int): The number of unique ordered edges 
            
    """
    edges = []
    
    # TODO: Test this
    for face in faces[:,:,0]: # Workimg on positions
        # Every edge should be from lowest index to highest
        sort = np.sort(face)
        edges.append(tuple([sort[0], sort[1]]))
        edges.append(tuple([sort[0], sort[2]]))
        edges.append(tuple([sort[1], sort[2]]))
        
        
    # Remove duplicates
    edges = set(edges)
    n_edges = len(edges)
    print("Number of edges = %s"%(n_edges))
    
    # Template of the matrix
    M = sparse.lil_matrix((n_edges, n_vertices), dtype='float32')
    #M = np.zeros((n_edges, n_vertices), dtype='float32')
    
    # -1 for source +1 for sink
    for idx, edge in enumerate(edges):
        i,j = edge
        M[idx, i] = -1
        M[idx, j] = 1
        
    G = np.diag([1, 1, 1, gamma]).astype(np.float32)
        
    return sparse.kron(M,G), n_edges

def NRICP(floating, fixed, fl_landmarks=None, fi_landmarks=None, verbose=False, mask=None):
    
    """ Perform optimal step non-rigid ICP to register floating mesh to fixed 
        (Amberg & Romdhani)
        https://www.researchgate.net/publication/200172513_Optimal_Step_Nonrigid_ICP_Algorithms_for_Surface_Registration
    
        (params):
            floating (Mesh): The mesh to be aligned
            fixed (Mesh): The target mesh that will not change
            (fl_landmarks) (list): The floating landmarks of the form
                [(idx, a ,b)] where idx is the index of the triangle in the face
                and a and b barycentric coordinates 
            (fi_landmarks) (list): Same as fl_landmarks but for the fixed mesh
            verbose (bool): If to print debugging information
            mask (list of int): The indices of vertices not to be transformed
    """
    
    # Decide if we are using landmarks
    if (fi_landmarks is not None) and (fl_landmarks is not None):
        USE_LANDMARKS = True
    else:
        USE_LANDMARKS = False
    
    # Get the vertices
    fl_verts = floating.vertices
    fi_verts = fixed.vertices
    
    n_vertices = fl_verts.shape[0]
    n_vertices_target = fi_verts.shape[0]
    
    # Convert to homogenous coordinates
    fl_verts = np.concatenate((fl_verts, np.ones((fl_verts.shape[0],1), dtype='float32' )), axis=1)
    fi_verts = np.concatenate((fi_verts, np.ones((fi_verts.shape[0],1), dtype='float32' )), axis=1)
    
    # Initalise the transforms
    transform = np.zeros((4*n_vertices, 3))
    
    for i in range(n_vertices):
        transform[4*i:(4*i)+3,:] = np.eye(3)
    
    # M kron G
    MG, n_edges = construct_MG(floating.faces, n_vertices, 1)   
    
    # For correspondances
    nn = NearestNeighbors(n_neighbors=1, algorithm='kd_tree').fit(fi_verts[:,0:3])
    knn = NearestNeighbors(n_neighbors=K).fit(fi_verts[:,0:3])
    
    # D matrix
    D = sparse.lil_matrix((n_vertices,n_vertices*4), dtype=np.float32)
    for i in range(n_vertices):
        D[i, 4*i:(4*i)+4] = fl_verts[i,:]
    
    
    # ---------------------------- Landmarks ------------------------------#
    if verbose:
        print("Processing landmarks")
    
    # Prepare the landmarks, they now must map single vertices in the source 
    # to points on the surface of the target
    
    if USE_LANDMARKS:
    
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
            va,vb,vc = fi_verts[a, 0:3], fi_verts[b, 0:3], fi_verts[c, 0:3]
            
            fi_point = (fi_a * va) + (fi_b *vb) +((1- fi_a - fi_b) *  vc)
            fi_landmark_points.append(fi_point)
            
        # Vectorise
        fi_landmark_points = np.array(fi_landmark_points)
        fl_landmark_indices = np.array(fl_landmark_indices)
        
        UL = fi_landmark_points

    # ----------------------- Loop over stiffness --------------------------- #
    
    graph = MeshGraph(floating)
    
    for epoch , alpha in enumerate(ALPHA_SCHEDULE):

        beta = BETA_SCHEDULE[epoch]
        if beta == 0:
            USE_LANDMARKS = False
        
        MAX_ITERS = 5
        if alpha < 25:
            MAX_ITERS = 3
        
        if verbose:
            print("Using stiffness %s"%(alpha))
        
        # Keep track of changes in the transform
        change = np.inf
        n_iter = 0 # Early stop if too many iterations
        
        
        # ------------------ Loop until convergence ------------------------- #
        while change > CHANGE_THRESHOLD:
            
            weights = np.ones((n_vertices,1))
            
            transformed = D @ transform
            
            dist, idx = nn.kneighbors(transformed[:,0:3])
            idx = idx.squeeze()   # https://github.com/saikiran321/nonrigid_icp/blob/master/nricp.py does this and it helps
            correspondance = fi_verts[idx, 0:3]
            
            # Discard any poor matches
            weights[np.where(dist>DISCARD)] = 0 
            
            # If using normals for weighting
            if USE_NORMALS and alpha < 3:
                # Only do it for low stiffness to overcome poor initial registration
                dists = np.zeros(fl_verts.shape[0])
                norms = get_normals(transformed , floating.faces)
                dist_k, idx_k = knn.kneighbors(transformed)
                for i in range(fl_verts.shape[0]):
                    n = norms[i]
                    k_corr = fi_verts[idx_k[i], 0:3] # This gives the KNN of the point
                    diff = fl_verts[i, 0:3] - k_corr # This gets the direction of each KNN relative to the point
                    # We look at the difference in angle between the lines to near points and the normal
                    cosine_difference = np.cross(diff, n) # On a flat surface this should alway be orthogonal
                    
                    filtr = np.linalg.norm(cosine_difference, axis=1) < 0.001 # The larger this is the more orthogonal n is to nearby points
                    if np.sum(filtr) > 0:
                        match = np.mean(k_corr[filtr], axis=0)
                    else:
                        match = 0
                    dists[i] = np.linalg.norm(match-fl_verts[i,0:3])
            
                ma, mi = np.min(transformed, axis=0), np.max(transformed, axis = 0)
                max_dist = np.linalg.norm(ma-mi)
                weights[np.where(dists>NORMAL_THRESHOLD * max_dist)[0]] = 0
            
            if mask is not None:
                # Exclude vertices in the mask by setting their weight to 0
                for idx in mask:
                    weights[idx] = 0
                    
            # Weighted match matrix
            U = weights * correspondance
            
            # A,B,U and D Directly from the paper
            A = sparse.vstack([alpha * MG, D.multiply(weights)])
            A = sparse.csr_matrix(A)
            
            B = sparse.lil_matrix((4 * n_edges + n_vertices, 3), dtype=np.float32)
            B[4 * n_edges: (4 * n_edges +n_vertices), :] = U
            B = sparse.csr_matrix(B)
            
            if USE_LANDMARKS:
                # Landmark terms + weighting
                DL = sparse.lil_matrix((UL.shape[0], 4*n_vertices))
                for count, l_idx in enumerate(fl_landmark_indices):
                    DL[count, 4*l_idx: 4*l_idx + 4] = fl_verts[l_idx,:] * beta                    
            
                A = sparse.csr_matrix(sparse.vstack([A, DL]))
                B = sparse.csr_matrix(sparse.vstack([B, beta * UL]))
            
            # This seems to be the only way of solving without lots of RAM    
            factor = cholesky_AAt(A.T)
            X = factor(A.T.dot(B)).toarray()
            
            change = np.linalg.norm(X-transform)
            transform = X
            n_iter += 1
            if n_iter > MAX_ITERS: # Early stop
                break
            
            if verbose:
                print('Change: ' , change)
                print('D loss: ', get_d_loss(D@transform, correspondance))
                print('S loss: ', get_s_loss(graph, transform, 1.0))
                
                if USE_LANDMARKS:
                    print('L loss: ', get_d_loss((D@transform)[fl_landmark_indices, :], UL))
                    print('Loss: ', get_d_loss(D@transform, correspondance) + alpha * get_s_loss(graph, transform, 1.0) + beta * get_d_loss((D@transform)[fl_landmark_indices, :], UL))
                
                else:
                    print('Loss: ', get_d_loss(D@transform, correspondance) + alpha * get_s_loss(graph, transform, 1.0))
    
    # Copy face and UV information from the ols mesh        
    out_faces = floating.faces
    out_uvs = floating.UVs
    out_normals = floating.normals
    
    out_vertices = D @ transform
    
    centroid = np.mean(out_vertices, axis=0)
    for i in range(n_vertices):
        
        # Apply the transform to the normals
        
        n = out_normals[i, :] # 3x1
        x = transform[4*i:(4*i)+3,:] # 3x3 no translation
        n_ = np.linalg.inv(x).T @ n
        n_ /= np.linalg.norm(n_)
        
        # If we are told to, try to flip some incorrect normals
        if FIX_NORMALS:
            
            # TODO: Fix backface issues
            # We'll look at the nearest neighbours and if more
            # than a certain ratio are opposite in direction we flip
            pass
        
        out_normals[i, :] = n_
    return Mesh(out_vertices, out_uvs, out_normals, out_faces), transform
            
            
    
