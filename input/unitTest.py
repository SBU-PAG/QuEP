# Initial conditions for sending a single electron through the back blowout regime of Quasi3D simulation
# useQuasi3D.py has only Mode 0 for EFields and BFields for optimal oscillation
# These conditions should produce a betatron wavelength of ~40 c/w_p

simulation_name = 'QUASI3D'
shape = 'single'
density = 1
fill = False
iterations = 100000

# Probe centered at the following initial coordinates:
x_c = 0.2 # Start within region of field
y_c = 0
xi_c = -12.3

# Initial momentum
px_0 = 0 # Make sure it goes towards the screen!
py_0 = 0
pz_0 = 20

# Screen Parameters (Assume infinite in y and z)
x_s = 5

# Shape Parameters (Radius or Side Length)
s1 = 0.5 # In y
s2 = 5 # In xi
