import numpy as np

class Compartment:
	def ConstantFunction( ): pass
	def CLV_model1( ): pass
	def ValveResistance( ): pass
	def ConstantResistance( ): pass

	def __init__( self, id, strName, dias_volume, initialP ):
		self.id : int = id
		self.name : str = strName
		self.dias_volume : float = dias_volume
		self.pressure = [ initialP ] #.append( initialP )
		self.volume = [ dias_volume ]
		self.inletQ = {}
		self.outletQ = {}
		self.compliance = lambda t: compliance(t, param = [0.])
		self.source = lambda t: ConstantFunction( t, [0.] )

	def setCompliance( self, compliance, param ):
		self.compliance = lambda t: compliance(t, param = param)

	def setSource( self, type, source, param ):
		if type == 'inlet':
			self.inletQ[ id ] = lambda pi: resistance( param[1], pi, param = param )
		elif type == 'outlet':
			self.outletQ[ id ] = lambda pi: resistance( pi, param[1], param = param )

	def setConnectivity( self, type, id, resistance, param ):
		if type == 'inlet':
			self.inletQ[ id ] = lambda pi, pj: resistance( pj, pi, param = param )
		elif type == 'outlet':
			self.outletQ[ id ] = lambda pi, pj: resistance( pi, pj, param = param )

	def appendPressure( self, pressure, time ):
		self.pressure.append( pressure )
		self.volume.append( self.dias_volume + pressure * self.compliance( time ) )


##############################################################################
##############################################################################

def ConstantFunction( time, param ):
	return param[0]

def CLV_model1( time, param ):
	'''
	Compliance function described in p.82 
	'''
	CompLV_min, CompLV_max = param[ 0:2 ]
	tauS, tauD   = param[ 2:4 ]
	heartT, sysT = param[ 4:6 ]

	t0 = np.mod( time,heartT )
	if t0 < sysT:
		exp0 = ( 1 - np.exp( -t0/tauS ))/( 1 - np.exp( -sysT/tauS ))
		CLV = CompLV_max * ( CompLV_min / CompLV_max )**exp0
	else:
		exp0 = ( 1 - np.exp( -(t0 - sysT)/tauD ))/( 1 - np.exp( -( heartT - sysT)/tauD ))
		CLV = CompLV_min * ( CompLV_max / CompLV_min )**exp0

	return CLV

def ValveResistance( pi, pj, param ):
	return max( pi - pj, 0. )/param[0]

def ConstantResistance( pi, pj, param ):
	return 1./param[0]