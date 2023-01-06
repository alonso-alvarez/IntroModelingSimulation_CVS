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
	Nchambers = len( model )
	#Plot_PerChamberData( model, heartTime, field = 'compliance' )

	Ncycles = 1
	maxIter = 250

	#for ichamber in range( Nchambers ):
		#keys = list( model[ichamber].inletQ.keys() )
		#print( keys, model[ichamber].inletQ[keys[0]](1,0) )
		#print( model[ichamber].pressure[-1])
	#exit()

	AE = np.zeros( ( Nchambers,Nchambers ) )
	BE = np.zeros( ( Nchambers ))

	print( BE )

	exit()

	time_array = np.arange( 0, Ncycles*heartTime[0], dt*heartTime[0] )
	for iterT in range( 1,len( time_array) ):
		p_lasttime = [ model[ichamber].pressure[-1] for ichamber in range( Nchambers )]
		error = 1.e8
		noiter = 0

		while erro > 1.e-1 and noiter < maxiter:
			p_iterk = p_lasttime.copy()
			noiter += 1

			## montar sistema

		print( pressurek )
		pass



	del( model )
	exit()


	param = call_globalVariables( case = 0 )

	#Aux_PlotLVComplianceFunction( param )  # Plot LeftVentricle compliance function

	NCycles : int = 10

	Rmi, Rao, Rsa = param[0:3]
	Clv, Csa = param[3:5]
	Pla, Psv = param[5:7]
	T, dt    = param[7:]

	time_array = np.arange(0, NCycles*T,dt*T)
	psa_array  = np.zeros_like( time_array )
	plv_array  = np.zeros_like( time_array )

	plv_array[ 0 ] = 5
	psa_array[ 0 ] = 80

	maxiter = 250

	## Systemic arterial tree
	for i in range( 1,len(time_array) ):
		plv_new = plv_array[ i - 1 ]; psa_new = psa_array[ i - 1 ]; erro = 1.e8

		noiter = 0
		while erro > 1.e-1 and noiter < maxiter:
			plv = plv_new; psa = psa_new
			noiter += 1

			coef_11 = Clv( time_array[i]) + dt * max( Pla - plv, 0 )/Rmi + dt * max( plv - psa, 0 )/Rao
			coef_12 = -dt * max( plv - psa, 0 )/Rao
			coef_21 = -dt * max( plv - psa, 0 )/Rao
			coef_22 = Csa + dt * max( plv - psa, 0 )/Rao + dt * 1./Rsa

			det = coef_11 * coef_22 - coef_12 * coef_21 

			b_1 = Clv( time_array[i-1] )*plv_array[ i - 1 ] + dt * max( Pla - plv, 0 ) * Pla / Rmi
			b_2 = Csa * psa_array[ i - 1 ] + dt * Psv / Rsa

			plv_new = ( coef_22 * b_1 - coef_12 * b_2 )/det
			psa_new = ( coef_11 * b_2 - coef_21 * b_1 )/det 

			erro = np.sqrt( ( plv_new - plv )**2 + ( psa_new - psa )**2 )

		psa_array[ i ] = psa_new
		plv_array[ i ] = plv_new 

	Aux_PressureData( NCycles, time_array, [ plv_array,psa_array ])

	# Computing volumes
	vlv_array = [ 0.027 + Clv(time_array[i])*plv_array[i] for i in range(len(time_array)) ]
	vsa_array = [ 0.825 + Csa*psa_array[i] for i in range(len(time_array)) ]

	#Aux_PressureData( NCycles, time_array, [vlv_array,vsa_array])

	#Aux_PressureData( NCycles, vlv_array, [plv_array] )





	#pdata =  [ psa_array, plv_array ]
	#print( pdata)

	#Aux_PlotSystemicSystem( NCycles, time_array, qsa_array, psa_array )




	


