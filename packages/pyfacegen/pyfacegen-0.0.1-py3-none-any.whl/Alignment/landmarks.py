import numpy as np



def read_wrap_landmark(f_name):
    
    """ Reads a landmark file from wrap """
    
    # Get the data
    with open(f_name, 'r') as f:
        data = f.read()
    
    # Strip all irrelevant chars
    d_copy = ''
    for c in data:
        if c not in '[ ]':
            d_copy += c
    
    # Split into just numbers
    data = d_copy.split(',')
    
    # Convert into landmarks
    landmarks = []
    for i in range(len(data)//3):
        landmark = []
        landmark.append(int(data[3*i]))     # Index
        landmark.append(float(data[3*i+1])) # a
        landmark.append(float(data[3*i+2])) # b
        landmarks.append(landmark)
        
    return landmarks

def read_wrap_polys_to_vertex_mask(f_name, mesh):
    
    """ Convert a wrap polygon file to a vertex mask """
    
    
    mask = set([])
    face_pos = mesh.faces[:,:,0]
    with open(f_name, 'r') as f:
        for count, line in enumerate(f):
            line = line.strip()
            line = line.split(',')
            d = line[0]
            try:
                x = int(d)
                face = face_pos[x]
                a,b,c = face
                mask.add(a)
                mask.add(b)
                mask.add(c)
            finally:
                continue
            
    return list(mask)