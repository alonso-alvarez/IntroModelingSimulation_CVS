import numpy as np

######
# Set the simulation case and parameters 
#
def call_globalVariables( case = 0 ):
	## Resistances
	Rmi = 0.01 * 60  			# Mitral valve resistance [ mmHg/(cm3*s)]
	Rao = 0.01 * 60  			# Aortic valve resistance [ mmHg/(cm3*s)]
	Rsa = 17.86* 60				# Sistemic (arterial) resistance [ mmHg/(cm3*s)]

	## Compliances
	Clv = LeftVentricleCompliance
	Csa = 0.00175					# Sistemic (arterial) compliance [ cm3/mmHg ]

	## Boundary data
	Pla = 5.0 						# Left atrium pressure
	Psv = 2.0 						# Terminal pressure (venous system)

	## Time data
	T   = 0.75 						# Heart rate period [ s ]
	dt  = 0.01 						# Time step for temporal integration

	return Rmi, Rao, Rsa, Clv, Csa, Pla, Psv, T, dt

def LeftVentricleCompliance( time ):
	T_period = 0.75
	T_sys = 0.005 * 60 # seconds

	CLVD = 0.0146 	# cm3/mmHg
	CLVS = 0.000003 # cm3/mmHg

	tauS = 0.0025 * 60 	# seconds
	tauD = 0.0075 * 60  # seconds
	
	t0 = np.mod( time,T_period )
	if t0 < T_sys:
		exp0 = ( 1 - np.exp( -t0/tauS ))/( 1 - np.exp( -T_sys/tauS ))
		CLV = CLVD * ( CLVS / CLVD )**exp0
	else:
		exp0 = ( 1 - np.exp( -(t0 - T_sys)/tauD ))/( 1 - np.exp( -(T_period - T_sys)/tauD ))
		CLV = CLVS * ( CLVD / CLVS )**exp0

	return CLV


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