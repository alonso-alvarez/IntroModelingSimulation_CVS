import matplotlib.pyplot as plt
import numpy as np

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

def Plot_PerChamberDiscreteData( model, heartTime, time_array, field, label, init = 0 ):
	fontsize = 9

	Nchambers = len( model )

	fig, ax = plt.subplots( 2,3, figsize = (10,4)); irow = 0; icol = 0
	for ichamber in range( Nchambers ):
		ct_array = model[ichamber].__dict__[field]
		str0 = model[ichamber].name

		ax0 = ax[irow][icol]; 
		ax0.plot( time_array[init:] - time_array[init], ct_array[init:], label = str0 )
		ax0.grid( True )
		ax0.set_xlabel( r'Time [s]', fontsize = fontsize)
		ax0.set_ylabel( label, fontsize = fontsize)
		ax0.legend( fontsize = fontsize )

		icol += 1
		if icol == 3:
			icol = 0; irow +=1

	fig.tight_layout()
	plt.show()
	plt.close()
	return None

def Plot_JointDiscreteData( model, heartTime, time_array, field, label, init = 0 ):
	fontsize = 9

	Nchambers = len( model )

	fig, ax = plt.subplots( 1,2, figsize = (10,4)); irow = 0; icol = 0
	for ichamber in range( Nchambers ):
		ct_array = model[ichamber].pressure
		str0 = model[ichamber].name

		ax0 = ax[0]; 
		ax0.plot( time_array[init:] - time_array[init], ct_array[init:], label = str0 )
		ax0.grid( True )
		ax0.set_xlabel( r'Time [s]', fontsize = fontsize)
		ax0.set_ylabel( 'Pressure', fontsize = fontsize)
		ax0.legend( fontsize = fontsize )

		ct_array = model[ichamber].volume
		str0 = model[ichamber].name
		ax0 = ax[1]; 
		ax0.plot( time_array[init:] - time_array[init], ct_array[init:], label = str0 )
		ax0.grid( True )
		ax0.set_xlabel( r'Time [s]', fontsize = fontsize)
		ax0.set_ylabel( 'Volume', fontsize = fontsize)
		ax0.legend( fontsize = fontsize )


	fig.tight_layout()
	plt.show()
	plt.close()
	return None
