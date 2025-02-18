# Here is where the initial conditions of the electron probe are defined
# This filename is the input parameter of the eProbe.py file

simulation_name = 'QUASI3D'
shape = 'vline'
density = 10
iterations = 15000
mode = 0

# Probe centered at the following initial coordinates (in c/w_p):
x_c = -2.4 # Start within region of field
y_c = 0
xi_c = -8.2

# Initial momentum
px_0 = 100 # Make sure it goes towards the screen!
py_0 = 0
pz_0 = 1000 # Keep with comoving frame

# Screen Distances (from z-axis of plasma cell, in mm):
#x_s = [100, 200, 300, 400, 500] # Only 5
x_s = [10, 20, 100, 250, 50]

# Shape Parameters (Radius or Side Length, in c/w_p):
s1 = 0.3 # In y
s2 = 10 # In xi
s3 = 1 # In x
