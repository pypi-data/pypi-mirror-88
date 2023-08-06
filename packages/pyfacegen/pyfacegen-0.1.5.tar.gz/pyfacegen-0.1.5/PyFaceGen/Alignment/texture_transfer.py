# Imports

import numpy as np
import matplotlib.pyplot as plt
import PIL.Image as Image
import time
from sklearn.neighbors import KNeighborsRegressor


from PyFaceGen.Mesh.Mesh import Mesh
from PyFaceGen.Mesh.Utils import TriangleTester, MultiTriangleTester
from PyFaceGen.IO.wobj_loader import wobj_2_mesh, mesh_2_wobj

class AlbedoPCA:
    
    def __init__(self, path):
        
        self.model = np.load(path)
        
        self.mu = self.model['MU']
        
        b,g,r = self.mu[:,:,0], self.mu[:,:,1], self.mu[:,:,2]
        self.mu = np.stack((r,g,b), axis=2)
        
        self.PC = self.model['PC']
        b,g,r = self.PC[:,:,0,:], self.PC[:,:,1,:], self.PC[:,:,2,:] 
        self.PC[:,:,0,:] = r
        self.PC[:,:,1,:] = g
        self.PC[:,:,2,:] = b
        
        self.s_mu = self.model['specMU']
        
        b,g,r = self.s_mu[:,:,0], self.s_mu[:,:,1], self.s_mu[:,:,2]
        self.s_mu = np.stack((r,g,b), axis=2)
        
        self.s_PC = self.model['specPC']
        b,g,r = self.s_PC[:,:,0,:], self.s_PC[:,:,1,:], self.s_PC[:,:,2,:] 
        self.s_PC[:,:,0,:] = r
        self.s_PC[:,:,1,:] = g
        self.s_PC[:,:,2,:] = b
        
        
        
    def get_diffuse_tex(self, weights):
        
        return self.mu + self.PC.dot(weights)
    
    def get_diffuse_tex_one_weight(self, idx, weight):
        
        return self.mu + weight*self.PC[:,:,:,idx]
    
    def get_spec_tex(self, weights):
        
        return self.s_mu + self.s_PC.dot(weights)
    
    def get_spec_tex_one_weight(self, idx, weight):
        
        return self.s_mu + weight*self.s_PC[:,:,:,idx]

class Excluder:
    
    """ This class determines if a texel should be excluded from the projections 
        using lines 
    """
    
    def __init__(self):
        
        self.lines=[]
        
    def add_line(self, slope, intercept, exclude_side):
        
        """ Adds a line used to exclude texels 
            (params):
                slope (float): The slope of the line
                intercept (float): The y intercept of the line
                exclude_side (+-1): Which side of the line to exclude. +1 means above, -1 below
        """
        
        self.lines.append([slope, intercept, exclude_side])
        
    def add_line_points(self, u1,v1,u2,v2, exclude_side):
        
        slope = (u2-u1)/(v2-v1)
        intercept = u2 - slope*v2
        
        print(slope, intercept)
        
        self.add_line(slope, intercept, exclude_side)
        
    def should_exclude(self, u,v):
        
        for line in self.lines:
            # Get y(x) for the given line
            Y = line[0]*u + line[1]
            diff = v-Y # Positive if point is above the line
            diff *= line[2] # Now positive if we want to exclude the point
            
            if diff>0:
                return True
        return False    
        
    def test(self, image):
        
        """ Shows an example of which texels are excluded from a given texture"""
        
        for v in range(image.height):
            for u in range(image.width):
                if self.should_exclude(u,v):
                    image.putpixel((v,u), (0,0,255))
                    
        plt.imshow(image)
        plt.show()

def project_texture_to_3d(mesh, texture_map, excluder=None):
    
    """ This code projects the UV space into 3 dimensions and provides an
        estimate correspondance between 3D pos and color
        (params): 
            mesh (Mesh): The mesh for which we project UVs
            texture_map: The texture
    """
    
    # Any uv not inside a face can just not be projected
    
    projections = []
    colours = []
    pix_coords = []
    
    
    # Get and scale the UVs to the image
    UVs = np.array(mesh.UVs)
    UVs[:,0] *= texture_map.width - 1
    UVs[:,1] *= texture_map.height - 1
    
    for i,face in enumerate(mesh.faces):
        
        # Iterate over the faces
        a,b,c = face
        uva, uvb, uvc = UVs[a], UVs[b], UVs[c]
        pa, pb, pc = mesh.vertices[a], mesh.vertices[b], mesh.vertices[c]
        
        # Get the bounding box of this triangle in UV space
        min_u = int(round(min(uva[0], uvb[0], uvc[0])))
        max_u = int(round(max(uva[0], uvb[0], uvc[0])))
        min_v = int(round(min(uva[1], uvb[1], uvc[1])))
        max_v = int(round(max(uva[1], uvb[1], uvc[1])))
        
        
        # To catch the triangles the are go across patches in UV space we set a limit on triangle size
        
        if max_u - min_u > 0.2*texture_map.width or max_v - min_v > 0.2*texture_map.height:
            continue
        
        # The vertices of the triangle in uv space
        x = np.round(uva)
        y = np.round(uvb)
        z = np.round(uvc)
        
        width = max_u - min_u + 1
        height = max_v - min_v + 1
        
        # Initialise the triangle tester for this face
        tester = MultiTriangleTester(x,y,z,width,height)
        
        # Get all points for testing
        P = np.zeros((height, width, 2))
        for j,u in enumerate(range(min_u, max_u+1)):
            for k,v in enumerate(range(min_v, max_v+1)):
                P[k,j] = np.array([u,v])
                
        is_in, w_a, w_b, w_c = tester.test(P)
        if np.isscalar(is_in):
            # Prevents runtime error when only 1 pixel is considered
            continue
            
        for j, u in enumerate(range(min_u, max_u+1)):  # +1 so inclusive
            for k, v in enumerate(range(min_v, max_v+1)): 
                
                if excluder is not None:
                    if excluder.should_exclude(u, texture_map.height-v):
                        continue
                    
                try:
                    if is_in[k,j]:
                        
                        position = w_a[k,j] * pa + w_b[k,j] * pb + w_c[k,j] * pc
                        color = texture_map.getpixel((u,texture_map.height-v))
                        
                        projections.append(position)
                        colours.append(color)
                        pix_coords.append(np.array([u,texture_map.height-v]))
                        
                except:
                    print(is_in)
                    raise
                    
        if i % 1000 ==0:
            
            print('%s out of %s'%(i, mesh.faces.shape[0]))
    return np.array(projections), np.array(colours), np.array(pix_coords)



def transfer_texture(source_mesh, target_mesh, source_texture, target_texture_size, plot=True):
    
    """ Transfers the source texture to the target texture using KNN given 2 meshes as 
        closely aligned as possible
        (params):
            source_mesh (Mesh): The mesh corresponding to the known texture
            target_mesh (Mesh): The mesh corresponding to the desired texture
            source_texture (PIL Image): The known texture
            target_texture_size (2-Tuple): The size of the output target texture (width, height)
    """
    
    # Create a blank
    target_texture = Image.new('RGB', target_texture_size)
    
    # First project each texel in the target texture to 3D space
    t_pos, t_tex, t_coords = project_texture_to_3d(target_mesh, target_texture) 
    
    # Then project the source texels
    s_pos, s_tex, s_coords = project_texture_to_3d(source_mesh, source_texture)
    
    # Now fit a KNN regressor to the source mesh to produce a color map in 3D space
    model = KNeighborsRegressor()
    model.fit(s_pos, s_tex)
    
    # Use this map to estimate the target texels from their 3D projection
    t_tex = model.predict(t_pos)
    
    for i in range(t_coords.shape[0]):
        # Set the texel to its predicted value in the texture
        coord = t_coords[i]
        u,v = coord
        colour = t_tex[i]
        r,g,b = colour
        r = int(r)
        g = int(g)
        b = int(b)
        target_texture.putpixel((u,v),(r,g,b))
   
    if plot:
        plt.imshow(target_texture)
        plt.show()
    
    return target_texture

def main(plot=True):
    
    """ Specifically for AlbedoMM --> rig """
    
    # Load textures
    rig_texture = Image.open('C:\\Users\\jacks\\OneDrive\\Documents\\MRES\\Project\\Summer - Corrective Blendshapes\\ObjRenderer\\data\\male_diffuse.png')
    mm_texture = Image.open('D:\\Data\\FLAME_Topology\\Albedo\\FLAME_DIFFUSE.png')

    # Load objects
    rig_mesh = wobj_2_mesh('C:/Users/jacks/OneDrive/Documents/PhD/Expression Wrapping/blendshapes/transferred_with_uvs/blend_0.obj')
    lyhm_mesh = wobj_2_mesh('C:/Users/jacks/OneDrive/Documents/PhD/Expression Wrapping/rigid_target.obj')
    
    # Define the texels we do not want to project
    exclude = Excluder()
    exclude.add_line_points(2600,4096, 4096, 1300,1)
    exclude.add_line_points(0,740, 670, 0,-1)
    exclude.add_line_points(4096,770, 4096-660, 0,1)
    
    # ONLY USE THIS LINE AS A TEST, DO NOT RUN WITH THE REST
    #exclude.test(rig_texture)
    
    # Load the Albedo MM for transfer
    # https://github.com/waps101/AlbedoMM
    mm = AlbedoPCA('D:/Data/FLAME_Topology/Albedo/albedoModel2020_FLAME_albedoPart.npz')
    
    # PIL Image format
    mm_texture = Image.fromarray(np.uint8(255*mm.mu))
    plt.imshow(mm_texture)
    plt.show()
    
    # Project every texel from the target image into 3D space
    print('Projecting target texture')
    start = time.time()
    t_pos, t_tex, t_coords = project_texture_to_3d(rig_mesh, rig_texture, exclude) 
    print('Took %s s'%(time.time() - start))  
    
    # Project every texel from the source image into 3D space
    print('Projecting source texture')
    start = time.time()
    s_pos, s_tex, s_coords = project_texture_to_3d(lyhm_mesh, mm_texture)
    print('Took %s s'%(time.time() - start))
    
    # Fit a KNN regressor to predict albedo from 3D position, trained on the source image
    print('Fitting Model')
    start = time.time()
    model = KNeighborsRegressor()
    model.fit(s_pos, s_tex)
    print('Took %s s'%(time.time() - start))
    
    # Predict the target texels albedo value from its projection in 3D space using the KNN regeressor
    t_tex = model.predict(t_pos)
    
    for i in range(t_coords.shape[0]):
        # Set the texel to its predicted value in the texture
        coord = t_coords[i]
        u,v = coord
        colour = t_tex[i]
        r,g,b = colour
        r = int(r)
        g = int(g)
        b = int(b)
        rig_texture.putpixel((u,v),(r,g,b))
   
    if plot:
        plt.imshow(rig_texture)
        plt.show()
        
    # TODO: Where should we put the output textures
    mean = np.array(rig_texture.getdata(), dtype='uint8').reshape((rig_texture.height, rig_texture.width, 4))[:,:,0:3]
    np.save('textures/mean.npy', mean)
    
    # Now we want to transfer the principal components of the model
    PC = np.zeros((rig_texture.height, rig_texture.width,3,mm.PC.shape[-1]), dtype='uint8')
    for i in range(mm.PC.shape[-1]):
        
        print(np.max(mm.PC[:,:,:,i]), np.min(mm.PC[:,:,:,i]))
        
        rig_texture = Image.open('C:\\Users\\jacks\\OneDrive\\Documents\\MRES\\Project\\Summer - Corrective Blendshapes\\ObjRenderer\\data\\male_diffuse.png')
        mm_texture = Image.fromarray(np.uint8(255*(mm.mu+mm.PC[:,:,:,i])))
        plt.imshow(mm_texture)
        plt.show()
        print('Projecting source texture')
        
        start = time.time()
        s_pos, s_tex, s_coords = project_texture_to_3d(lyhm_mesh, mm_texture)
        
        print('Took %s s'%(time.time() - start))
        
        
        print('Fitting Model')
        
        start = time.time()
        model = KNeighborsRegressor()
        model.fit(s_pos, s_tex)
        
        print('Took %s s'%(time.time() - start))
        
        
            
        t_tex = model.predict(t_pos)
        
        for j in range(t_coords.shape[0]):
            
            coord = t_coords[j]
            u,v = coord
            
            colour = t_tex[j]
            r,g,b = colour
            r = int(r)
            g = int(g)
            b = int(b)
            rig_texture.putpixel((u,v),(r,g,b))

        plt.imshow(rig_texture)
        plt.show()
        
        pc = np.array(rig_texture.getdata()).reshape(rig_texture.height, rig_texture.width, 4)[:,:,0:3]
        plt.imshow(pc-mean)
        plt.show()
        PC[:,:,:,i] = pc-mean
    
    np.save('textures/pcs.npy',PC)
    
     
