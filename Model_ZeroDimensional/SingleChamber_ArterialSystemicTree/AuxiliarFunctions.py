import matplotlib.pyplot as plt
import numpy as np

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


def Aux_PlotSystemicSystem( NCycles, time_array, qsa_array, psa_array ):
	fontsize = 9
	LastCycle = ( NCycles - 1 )*int( len( time_array )/NCycles )

	fig, ax = plt.subplots(1,2,figsize =(10,4))
	
	ax0 = ax[0]; ax2 = ax0.twinx();
	ax0.plot( time_array, psa_array ); ax0.grid(True)
	ax2.plot( time_array, qsa_array, color = 'red'); ax2.grid(True)
	ax0.set_xlabel('Time [s]', fontsize = fontsize )
	ax0.set_ylabel(r'$p_{sa}$ [mmHg]', fontsize = fontsize, color = 'blue')
	ax2.set_ylabel(r'$Q_{L}$ [cm$^3$/s]', fontsize = fontsize, color = 'red' )

	ax0 = ax[1]; ax2 = ax0.twinx();
	ax0.plot( time_array[LastCycle:], psa_array[LastCycle:]); ax0.grid(True)
	ax2.plot( time_array[LastCycle:], qsa_array[LastCycle:], color = 'red'); ax2.grid(True)
	ax0.set_xlabel('Time [s]', fontsize = fontsize )
	ax0.set_ylabel(r'$p_{sa}$ [mmHg]', fontsize = fontsize, color = 'blue')
	ax2.set_ylabel(r'$Q_{L}$ [cm$^3$/s]', fontsize = fontsize, color = 'red' )

	fig.tight_layout()
	plt.show()
	plt.close()

	return None