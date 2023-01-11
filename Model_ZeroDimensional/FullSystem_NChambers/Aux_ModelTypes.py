from Aux_TypeCompartments import *

def BuildModel_TwoChambers( ):
	heartTime	= [ 0.75, 0.30 ] 	## [ s ] : duration of heartbeat, systolic phase
	tauParam	= [ 0.15, 0.45 ]  ## [ s ] : constant for compliance of heart at systole, diastole
	dt = 0.01 * heartTime[ 0 ]

	CompLA = 0.00005 
	CompLV = [ 0.00003, 0.01460 ]  ## syst - dias
	CompSA = 0.00175
	CompSV = 0.00005

	VolumeLA = 0.0270
	VolumeLV = 0.0270
	VolumeSA = 0.8250
	VolumeSV = 0.0000

	ResistanceValveMit = 0.01 * 60 
	ResistanceValveAor = 0.01 * 60 
	ResistanceSys = 17.86 * 60

	InitialLA = 5
	InitialLV = 5
	InitialSA = 80
	InitialSV = 2

	model = []
	p1 = Compartment( id = 0, strName = 'LeftAtrium', dias_volume = VolumeLA, initialP = InitialLA ); 
	p1.setCompliance( compliance = ConstantFunction, param = [ CompLA ] )
	model.append( p1 )

	p1 = Compartment( id = 1, strName = 'LeftVentricle', dias_volume = VolumeLV, initialP = InitialLV ); 
	p1.setCompliance( compliance = CLV_model1, param = [ *CompLV, *tauParam, *heartTime ] )
	p1.setConnectivity( type = 'inlet',  id = 0, resistance = ValveResistance, param = [ ResistanceValveMit ])
	p1.setConnectivity( type = 'outlet', id = 2, resistance = ValveResistance, param = [ ResistanceValveAor ])
	model.append( p1 )

	p1 = Compartment( id = 2, strName = 'SistemicArterial', dias_volume = VolumeSA, initialP = InitialSA ); 
	p1.setCompliance( compliance = ConstantFunction, param = [ CompSA ] )
	p1.setConnectivity( type = 'inlet' , id = 1, resistance = ValveResistance, param = [ ResistanceValveAor ])
	p1.setConnectivity( type = 'inlet' , id = 3, resistance = ConstantResistance, param = [ ResistanceSys ])
	model.append( p1 )

	p1 = Compartment( id = 3, strName = 'SistemicVenous', dias_volume = VolumeSV, initialP = InitialSV ); 
	p1.setCompliance( compliance = ConstantFunction, param = [ CompSV ] )
	model.append( p1 )

	return model, heartTime, dt



def BuildModel_FullSixChambers( ):
	print(
	'''
	ZeroDimensional model of cardiovascular circulation

	Components: 
	- Left heart, right heart
	- Sistemic circulation: arterial and pulmonar
	- Pulmonar circulation: arterial and pulmonar
	All components are considered as compliant vessels
	Connections: 
	- RH -> PulmVenous -> PulmArterial --> LH -> SisArterial -> SisVenous -> RH
	- Valves for RH -> LH, LH -> Sistemic, Pulmonar -> RH
	- No valves for arterial <-> pulmonar 
	Parameters
	- Heartbeat: 0.75 seconds
	- Simulation time: 7.5 seconds
	- Discretization step: 0.01
	'''
	)

	heartTime	= [ 0.75, 0.30 ] 	## [ s ] : duration of heartbeat, systolic phase
	tauParam	= [ 0.12, 0.45 ]  ## [ s ] : constant for compliance of heart at systole, diastole
	dt = 0.01 * heartTime[ 0 ]

	CompSA = 0.00175 ## [cm3/mmHg] Compliance: Systemic arterial
	CompPA = 0.00412 ## [cm3/mmHg] Compliance: Pulmonar arterial
	CompSV = 1.75000 ## [cm3/mmHg] Compliance: Systemic venous
	CompPV = 0.08000 ## [cm3/mmHg] Compliance: Pulmonar venous
	CompLH = [ 0.00003, 0.01460 ]  # [cm3/mmHg] Parameters for compliance of left heart [min,max] values
	CompRH = [ 0.00020, 0.03650 ]  # [cm3/mmHg] Parameters for compliance of left heart [min,max] values

	VolumeSA = 0.8250	  ## [cm3] Volume at diastole (p = 0): Systemic arterial
	VolumePA = 0.0382		## [cm3] Volume at diastole (p = 0): Pulmonar arterial
	VolumeSV = 0.0000   ## [cm3] Volume at diastole (p = 0): Systemic venous
	VolumePV = 0.0000   ## [cm3] Volume at diastole (p = 0): Pulmonar venous
	VolumeLH = 0.0270   ## [cm3] Volume at diastole (p = 0): Left heart
	VolumeRH = 0.0270   ## [cm3] Volume at diastole (p = 0): Right heart

	ResistanceSys = 17.5 * 60 ## [ mmHg / ( cm3 s )] Systemic resistance
	ResistancePul = 1.79 * 60 ## [ mmHg / ( cm3 s )] Pulmonar resistance
	ResistanceValveMit = 0.01 * 60 ## [ mmHg / ( cm3 s )] Mitral valve resistance - LA -> LV
	ResistanceValveAor = 0.01 * 60 ## [ mmHg / ( cm3 s )] Aortic valve resistance - LV -> aorta
	ResistanceValveTri = 0.01 * 60 ## [ mmHg / ( cm3 s )] Tricuspid valve resistance - RA -> RV
	ResistanceValvePul = 0.01 * 60 ## [ mmHg / ( cm3 s )] Pulmonic valve resistance - RV -> pulmonary artery
	
	InitialRH = 2
	InitialPV = 5
	InitialPA = 8
	InitialLH = 5
	InitialSA = 80
	InitialSV = 2

	model = []
	p1 = Compartment( id = 0, strName = 'LeftHeart', dias_volume = VolumeLH, initialP = InitialLH ); 
	p1.setCompliance( compliance = CLV_model1, param = [ *CompLH, *tauParam, *heartTime ] )
	p1.setConnectivity( type = 'inlet' , id = 5, resistance = ValveResistance, param = [ ResistanceValveMit ])
	p1.setConnectivity( type = 'outlet', id = 1, resistance = ValveResistance, param = [ ResistanceValveAor ])
	model.append( p1 )

	p1 = Compartment( id = 1, strName = 'SistemicArterial', dias_volume = VolumeSA, initialP = InitialSA ); 
	p1.setCompliance( compliance = ConstantFunction, param = [ CompSA ] )
	p1.setConnectivity( type = 'inlet' , id = 0, resistance = ValveResistance, param = [ ResistanceValveAor ])
	p1.setConnectivity( type = 'outlet', id = 2, resistance = ConstantResistance, param = [ ResistanceSys ])
	model.append( p1 )

	p1 = Compartment( id = 2, strName = 'SistemicVenous', dias_volume = VolumeSV, initialP = InitialSV ); 
	p1.setCompliance( compliance = ConstantFunction, param = [ CompSV ] )
	p1.setConnectivity( type = 'inlet' , id = 1, resistance = ConstantResistance, param = [ ResistanceSys ])
	p1.setConnectivity( type = 'outlet', id = 3, resistance = ValveResistance, param = [ ResistanceValveTri ])
	model.append( p1 )

	p1 = Compartment( id = 3, strName = 'RightHeart', dias_volume = VolumeLH, initialP = InitialRH ); 
	p1.setCompliance( compliance = CLV_model1, param = [ *CompRH, *tauParam, *heartTime ] )
	p1.setConnectivity( type = 'inlet' , id = 2, resistance = ValveResistance, param = [ ResistanceValveTri ])
	p1.setConnectivity( type = 'outlet', id = 4, resistance = ValveResistance, param = [ ResistanceValvePul ])
	model.append( p1 )

	p1 = Compartment( id = 4, strName = 'PulmonarArterial', dias_volume = VolumePA, initialP = InitialPA ); 
	p1.setCompliance( compliance = ConstantFunction, param = [ CompPA ] )
	p1.setConnectivity( type = 'inlet' , id = 3, resistance = ValveResistance, param = [ ResistanceValvePul ])
	p1.setConnectivity( type = 'outlet', id = 5, resistance = ConstantResistance, param = [ ResistancePul ])
	model.append( p1 )

	p1 = Compartment( id = 5, strName = 'PulmonarVenous', dias_volume = VolumePV, initialP = InitialPV ); 
	p1.setCompliance( compliance = ConstantFunction, param = [ CompPV ] )
	p1.setConnectivity( type = 'inlet' , id = 4, resistance = ConstantResistance, param = [ ResistancePul ] )
	p1.setConnectivity( type = 'outlet', id = 0, resistance = ValveResistance, param = [ ResistanceValveMit ])
	model.append( p1 )


	return model, heartTime, dt