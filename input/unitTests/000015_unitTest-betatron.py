# Here is where the initial conditions of the electron probe are defined
# This filename is the input parameter of the eProbe.py file

simulation_name = 'QUASI3D'
shape = 'single'
iterations = 100000
mode = 0
fname = "000015_unitTest-betatron.npz"
debugmode = True

# Probe centered at the following initial coordinates (in c/w_p):
x_c = 2.0 # Start within region of field
y_c = 2.0
xi_c = -12.3 #Makes Z = 39.7 since t0= 51.9948 for 000010

# Initial momentum
px_0 = 0 # Make sure it goes towards the screen!
py_0 = 0
pz_0 = 3.202563076101742

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