# Here is where the initial conditions of the electron probe are defined
# This filename is the input parameter of the eProbe.py file

simulation_name = 'QUASI3D'
shape = 'rectangle'
# dt = 0.005, 150000
iterations = 500000
mode = -1
fname = "animation.npz"

# Probe centered at the following initial coordinates (in c/w_p):
x_c = -2.4 # Start within region of field
y_c = 0
xi_c = -14.5

# Initial momentum
px_0 = 110 # Make sure it goes towards the screen!
py_0 = 0
pz_0 = 0

# Screen Distances (from z-axis of plasma cell, in mm):
#x_s = [100, 200, 300, 400, 500] # Only 5
x_s = [10, 50, 100, 250, 500]

# Shape Parameters (Radius or Side Length, in c/w_p):
s1 = 0.8 # In y
s2 = 7.5 # In xi
s3 = 1 # In x

# Densities
xdensity = 0 #Not used
ydensity = 32
xidensity = 30
resolution = 0.5
