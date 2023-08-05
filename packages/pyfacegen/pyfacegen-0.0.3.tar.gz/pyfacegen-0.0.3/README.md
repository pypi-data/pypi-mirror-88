A python library for several functions used in generating realistic facial meshes. Including:

Mesh: A simple mesh class consisting of vertices and faces
IO: Read/write of .obj and .ply files
Alignment: Rigid ICP and non-rigid ICP
Other: Deformation transfer

Installation instructions

create and activate a virtual environment

run the following comands (using anaconda)

$ conda install numpy matplotlib scikit-learn scikit-image
 
install scikit-sparse with conda using
$ conda install -c conda-forge scikit-sparse 

if using .ply files install pyassimp using pip
$ pip install pyassimp

To verify installation use
$ python tests.py
