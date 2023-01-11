'''
Modelo simplificado não estacionário da circulação
- Disponível no cap 4.5 da referência Blanco (2011) - Introdução à modelagem e simulação...

Nesse modelo tratamos a circulação sanguínea descrevendo fluxo, volume e pressão como 
variáveis no tempo 


Autor: Alonso Alvarez
Date: Jan 2023
'''
import numpy as np
from timeit import default_timer as timer

from Aux_ModelTypes import *
from Post_PlotQuantities import *

if __name__ == "__main__":

	model, heartTime, dt = BuildModel_FullSixChambers( )
	#model, heartTime, dt = BuildModel_TwoChambers( )
	Nchambers = len( model )
	Plot_PerChamberData( model, heartTime, field = 'compliance' )

	Ncycles = 50
	maxIter = 250

	time_array = np.arange( 0, Ncycles*heartTime[0], dt )

	for iterT in range( 1,len( time_array) ):
		p_lasttime = [ model[ichamber].pressure[-1] for ichamber in range( Nchambers )]
		p_currentiter = p_lasttime.copy()

		error = 1.e8; noiter = 0; t0 = time_array[ iterT ]
		while error > 1.e-1 and noiter < maxIter:
			p_lastiter = p_currentiter.copy(); noiter += 1
			AE = np.zeros( ( Nchambers,Nchambers ) ); BE = np.zeros( ( Nchambers ))

			for irow in range( Nchambers ):
				AE[ irow,irow ] = model[ irow ].compliance( t0 )
				BE[ irow ] = model[ irow ].compliance( time_array[ iterT - 1 ] )*p_lasttime[ irow ]
				#BE[ irow ] = BE[ irow ] + dt * model[ irow ].source( t0 )

				keys = list( model[ irow ].inletQ.keys() )
				for icol in keys:
					inletJ = model[ irow ].inletQ[ icol ]( p_lastiter[irow], p_lastiter[icol] )
					AE[ irow,irow ] = AE[ irow,irow ] + dt * inletJ
					AE[ irow,icol ] = AE[ irow,icol ] - dt * inletJ 

				keys = list( model[ irow ].outletQ.keys() )
				for icol in keys:
					outletJ = model[ irow ].outletQ[ icol ]( p_lastiter[irow], p_lastiter[icol] )
					AE[ irow,irow ] = AE[ irow,irow ] + dt * outletJ
					AE[ irow,icol ] = AE[ irow,icol ] - dt * outletJ

			p_currentiter = np.linalg.solve( AE,BE )
			error = np.linalg.norm( p_currentiter - p_lastiter )

		for irow in range( Nchambers ):
			model[ irow ].appendPressure( p_currentiter[ irow ], time_array[ iterT ] )		

	Plot_PerChamberDiscreteData( model, heartTime, time_array, init = ( Ncycles - 3 )*100, field = 'pressure', label = 'Pressure [mmHg]')
	Plot_PerChamberDiscreteData( model, heartTime, time_array, init = ( Ncycles - 3 )*100, field = 'volume', label = r'Volume [cm$^3$]')

	Plot_JointDiscreteData( model, heartTime, time_array, init = ( Ncycles - 1 )*100, field = 'volume', label = r'Volume [cm$^3$]')
	del( model, AE, BE  )
