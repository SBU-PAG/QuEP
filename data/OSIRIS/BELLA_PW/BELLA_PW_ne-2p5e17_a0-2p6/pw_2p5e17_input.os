simulation
{
	algorithm = "quasi-3D",
    n0=2.5d17,
}

node_conf
{
	node_number(1:2) = 80, 8,  
	if_periodic(1:2) = .false., .false., 
}

grid
{
	nx_p(1:2) = 7600, 400,
	coordinates = "cylindrical",
	n_cyl_modes = 1,
}

time_step
{
	dt = 0.001,
	ndump = 2000,
}

restart
{
	ndump_fac = 5,
	if_restart = .false.,
    if_remold = .true.,
}

space
{
	xmin(1:2) = -9.0, 0.0, 
	xmax(1:2) = 9.0, 10.0, 
	if_move = .true., .false., 
}

time
{
	tmin = 0.0,
	tmax = 400,
}

el_mag_fld
{
	solver = "fei",
}

emf_bound
{
	type(1:2,1) = "lindman", "lindman", 
	type(1:2,2) = "axial", "open", 
}

emf_solver
{
	type = "dual",
	solver_ord = 2,
	n_coef = 16,
	weight_n = 10,
	weight_w = 0.3,
	filter_limit = 0.6,
	filter_width = 0.1,
	n_damp_cell = 10,
	filter_current = .true.,
	correct_current = .true.,
}

diag_emf
{
	ndump_fac = 1,
	ndump_fac_lineout = 1,
	ndump_fac_ene_int = 0, 
	reports = "e1_cyl_m", "e2_cyl_m", "e2_cyl_m, line, x1, 1", "e3_cyl_m", "b1_cyl_m", "b2_cyl_m", "b3_cyl_m",
}

particles
{
	num_species = 1,
    num_neutral= 0,
	interpolation = "linear",
}

species
{
	name = "electrons",
	num_par_max = 10000000,
	rqm = -1.0,
	num_par_x(1:2) = 2, 2, 
	num_par_theta = 8,
	add_tag = .false.,
	push_type = "standard",
}

profile
{
  density = 1,
  profile_type(1:2) = "piecewise-linear", "uniform",
  num_x = 2,
  x(1:2,1) = 9.0, 28.0,
  fx(1:2,1) = 0, 1,
}

spe_bound
{
  type(1:2,1) = "open", "open",
  type(1:2,2) = "open", "open",
}

diag_species
{
	ndump_fac = 1,
	ndump_fac_pha = 0,
	ndump_fac_raw = 2,
	ndump_fac_lineout = 0,
	raw_math_expr = "p1>10",
	reports = "charge_cyl_m", 
	phasespaces = "p1x1", "p1x2", 
	ps_np(1:3) = 512, 512, 512, 
	if_ps_p_auto(1:3) = .true., .true., .true., 
	ps_pmin(1) = 5,
}

zpulse
{
	a0 = 2.654,
    if_launch = .true.,
    omega0 = 83.474,
    pol_type=0,
    pol=0.0,
    
    lon_type = "gaussian",
	lon_fwhm = 3.001,
	lon_x0 = 0,
    lon_range = 18.008,
    
    per_type = "gaussian",
    per_w0 = 3.001,
    per_focus = 24,
}


current
{
}

smooth
{
}


