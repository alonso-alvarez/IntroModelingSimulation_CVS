import numpy as np

######
# Set the simulation case and parameters 
#
def call_globalVariables( case = 0 ):
	R_sis = 1.0716e3 				# [mmHg/(cm3/s)] 	Sistemic resistance
	C_sa  = 0.00175  				# [cm3/mmHg]     	Compliance of arterial system
	QLeft = SpikeLeftFlow 	# Left heart ejection function
	T     = 7.5e-1
	dt    = 1.e-2    				# [ dt = 0.01*T ]	Time step in seconds - depends on heart period T

	return R_sis, C_sa, QLeft, dt, T


######
# Ejection functions
def SpikeLeftFlow( time ):
	T_period = 0.75 # seconds
	Q_max = 0.46    # cm3/s
	T_max = 0.12  	# seconds
	T_sys = 0.30 		# seconds 

	t0 = np.mod( time, T_period )
	if t0 < T_max:
		q0 = Q_max/T_max * t0
	elif t0 < T_sys:
		q0 = Q_max * ( T_sys - t0 )/( T_sys - T_max )
	else:
		q0 = 0

	return q0