# Here is where the initial conditions of the electron probe are defined
# This filename is the input parameter of the eProbe.py file
#
# This input file is for testing the field data for a0 = 4 sim (sim ID 000067)
# This 000028 file fixes errors from 1/19 presentation

simulation_name = 'QUASI3D'
shape = 'single'
iterations = 100000
mode = 0
fname = "000028_testing.npz"
debugmode = True

# Probe centered at the following initial coordinates (in c/w_p):
x_c = 7 # Start within region of field
y_c = 2 # Off-center to avoid center of bubble?
xi_c = -7

# Initial momentum
px_0 = 100 # Make sure it goes towards the screen!
py_0 = 0
pz_0 = 0

# Screen Parameters (Assume infinite in y and z)
x_s = 500

# Shape Parameters (Radius or Side Length)
s1 = 1 # In y
s2 = 1 # In xi

# Densities
ydensity = 1
xidensity = 1
xdensity = 1 # Probe width - 1 single layer
resolution = None