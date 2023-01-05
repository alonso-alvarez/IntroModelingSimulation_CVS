'''
Modelo simplificado não estacionário da circulação
- Disponível no cap 4.5 da referência Blanco (2011) - Introdução à modelagem e simulação...

Nesse modelo tratamos a circulação sanguínea descrevendo fluxo, volume e pressão como 
variáveis no tempo 


Autor: Alonso Alvarez
Date: Jan 04, 2023
'''
import numpy as np
from timeit import default_timer as timer

from InitializeGlobalParameters import *
from AuxiliarFunctions import *


if __name__ == "__main__":
	param = call_globalVariables( case = 0 )

	#Aux_PlotLVEjectionFunction( param )  # Plot LeftVentricle ejection function

	NCycles : int = 10

	R_sis, C_sa, QLeft, dt, T = param
	time_array = np.arange(0, NCycles*T,dt*T)
	psa_array  = np.zeros_like( time_array )
	qsa_array  = np.zeros_like( time_array )

	## Systemic arterial tree
	for i in range( 1,len(time_array) ):
		coef_1 = C_sa/dt + 1/R_sis
		coef_2 = C_sa/dt 
		qsa_array[ i ] = QLeft( time_array[i] )
		psa_array[ i ] = 1/coef_1 * ( qsa_array[ i ] + coef_2 * psa_array[ i - 1 ] ) # + p_sv/R_sis)

	Aux_PlotSystemicSystem( NCycles, time_array, qsa_array, psa_array )




	


