# Here is where the initial conditions of the electron probe are defined
# This filename is the input parameter of the eProbe.py file
#
# This input file is for testing the field data for a0 = 4 sim (sim ID 000067)

simulation_name = 'QUASI3D'
shape = 'single'
iterations = 100000
mode = 0
fname = "000025_testing.npz"
debugmode = True

# Probe centered at the following initial coordinates (in c/w_p):
x_c = 7 # Start within region of field
y_c = 0
xi_c = -11 

# Initial momentum
px_0 = 0 # Make sure it goes towards the screen!
py_0 = 0
pz_0 = 100

# Screen Parameters (Assume infinite in y and z)
x_s = 500

# Shape Parameters (Radius or Side Length)
s1 = None # In y
s2 = None # In xi

# Densities
ydensity = 1
xidensity = 1
xdensity = 1 # Probe width - single layer
resolution = None