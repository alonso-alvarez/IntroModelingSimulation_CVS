import matplotlib.pyplot as plt
import numpy as np


def Plot_PerChamberCompliance( model, heartTime ):
	fontsize = 9

	Nchambers = len( model )
	time_array = np.linspace( 0, heartTime[0], 200 )

	fig, ax = plt.subplots( 2,3, figsize = (10,4))
	irow = 0; icol = 0
	for ichamber in range( Nchambers ):
		ct_array = [ model[ichamber].compliance( t0 ) for t0 in time_array ]
		str0 = model[ichamber].name

		ax0 = ax[irow][icol]; 
		ax0.plot( time_array, ct_array, label = str0 )
		ax0.grid( True )
		ax0.set_xlabel( r'Time [s]', fontsize = fontsize)
		ax0.set_ylabel( r'Compliance [cm$^3$/mmHg]', fontsize = fontsize)
		ax0.legend( fontsize = fontsize )

		icol += 1
		if icol == 3:
			icol = 0; irow +=1

	fig.tight_layout()
	plt.show()
	plt.close()
	return None


def Plot_PerChamberData( model, heartTime, field ):
	fontsize = 9

	Nchambers = len( model )
	time_array = np.linspace( 0, heartTime[0], 200 )

	fig, ax = plt.subplots( 2,3, figsize = (10,4))
	irow = 0; icol = 0
	for ichamber in range( Nchambers ):
		#ct_array = [ model[ichamber].compliance( t0 ) for t0 in time_array ]
		ct_array = [ model[ichamber].__dict__[field]( t0 ) for t0 in time_array ]
		str0 = model[ichamber].name

		ax0 = ax[irow][icol]; 
		ax0.plot( time_array, ct_array, label = str0 )
		ax0.grid( True )
		ax0.set_xlabel( r'Time [s]', fontsize = fontsize)
		ax0.set_ylabel( r'Compliance [cm$^3$/mmHg]', fontsize = fontsize)
		ax0.legend( fontsize = fontsize )

		icol += 1
		if icol == 3:
			icol = 0; irow +=1

	fig.tight_layout()
	plt.show()
	plt.close()
	return None


def Aux_PlotLVEjectionFunction( param ):
	FlowProfile = param[2]
	time_array = np.linspace(0,1,200)
	LVq0_array = [ FlowProfile( i0 ) for i0 in time_array ]
	fig = plt.figure()
	plt.plot( time_array, LVq0_array); plt.grid(True)
	plt.xlabel(r'Time [s]', fontsize = 9)
	plt.ylabel(r'Q [cm$^3$/s]', fontsize = 9)
	plt.show()
	plt.close()	
	return None