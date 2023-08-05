
#ifndef ACMCONFIG_H
#define ACMCONFIG_H

#define EXCITATION_TYPE (2)

#define NULL_D_AXIS_CURRENT_CONTROL -1
#define MTPA -2 // not supported

#define NUMBER_OF_STEPS 107561
#define DOWN_SAMPLE 1
#define CONTROL_STRATEGY NULL_D_AXIS_CURRENT_CONTROL
#define SENSORLESS_CONTROL FALSE
#define SENSORLESS_CONTROL_HFSI FALSE
#define VOLTAGE_CURRENT_DECOUPLING_CIRCUIT FALSE
#define SATURATED_MAGNETIC_CIRCUIT FALSE
#define INVERTER_NONLINEARITY FALSE
#define CL_TS (5e-05)
#define CL_TS_INVERSE (20000)
#define TS_UPSAMPLING_FREQ_EXE 0.25
#define TS_UPSAMPLING_FREQ_EXE_INVERSE 4

#define VL_TS          (0.0002)
#define PL_TS VL_TS
#define SPEED_LOOP_CEILING (4)

#define CLARKE_TRANS_TORQUE_GAIN (1.5) // consistent with experiment
#define AINV2PINV (0.816496581) // = 1/sqrt(1.5) power-invariant to aplitude-invariant (the dqn vector becomes shorter to have the same length as the abc vector)
#define PINV2AINV (1.22474487)

#define MACHINE_DYNAMICS SM_Dynamics

#define PMSM_NUMBER_OF_POLE_PAIRS          4
#define PMSM_RESISTANCE                    0.152
#define PMSM_D_AXIS_INDUCTANCE             0.00046600000000000005
#define PMSM_Q_AXIS_INDUCTANCE             0.00046600000000000005
#define PMSM_PERMANENT_MAGNET_FLUX_LINKAGE 0.023331
#define PMSM_SHAFT_INERTIA                 1.6000000000000003e-05
#define PMSM_RATED_CURRENT_RMS             12.8
#define PMSM_RATED_POWER_WATT              400
#define PMSM_RATED_SPEED_RPM               3000

#define LOAD_INERTIA                       0.16
#define LOAD_TORQUE                        0.0
#define VISCOUS_COEFF                      7e-05

#define PMSM_RATED_TORQUE ( PMSM_RATED_POWER_WATT / (PMSM_RATED_SPEED_RPM/60.0*2*3.1415926) )
#define PMSM_TORQUE_CONSTANT ( PMSM_RATED_TORQUE / (PMSM_RATED_CURRENT_RMS*1.414) )
#define PMSM_BACK_EMF_CONSTANT ( PMSM_TORQUE_CONSTANT / 1.5 / PMSM_NUMBER_OF_POLE_PAIRS )
#define PMSM_BACK_EMF_CONSTANT_mV_PER_RPM ( PMSM_BACK_EMF_CONSTANT * 1e3 / (1.0/PMSM_NUMBER_OF_POLE_PAIRS/2/3.1415926*60) )

#define CURRENT_KP (1.46398)
#define CURRENT_KI (326.18)
#define CURRENT_KI_CODE (CURRENT_KI*CURRENT_KP*CL_TS)
#define SPEED_KP (0.0160203)
#define SPEED_KI (74.3572)
#define SPEED_KI_CODE (SPEED_KI*SPEED_KP*VL_TS)

#define SWEEP_FREQ_MAX_FREQ 200
#define SWEEP_FREQ_INIT_FREQ 2
#define SWEEP_FREQ_VELOCITY_AMPL 500
#define SWEEP_FREQ_CURRENT_AMPL 1
#define SWEEP_FREQ_C2V FALSE
#define SWEEP_FREQ_C2C FALSE

#define SPEED_LOOP_PID_PROPORTIONAL_GAIN 0.00121797
#define SPEED_LOOP_PID_INTEGRAL_TIME_CONSTANT (1/312.3)
#define SPEED_LOOP_PID_DIREVATIVE_TIME_CONSTANT 0
#define SPEED_LOOP_LIMIT_NEWTON_METER (1*PMSM_RATED_TORQUE)
#define SPEED_LOOP_LIMIT_AMPERE (1*1.414*PMSM_RATED_CURRENT_RMS)

#define CURRENT_LOOP_PID_PROPORTIONAL_GAIN 9.2363 // (CL_TS_INVERSE*0.1*PMSM_D_AXIS_INDUCTANCE) // 9.2363
#define CURRENT_LOOP_PID_INTEGRAL_TIME_CONSTANT (1/352.143)
#define CURRENT_LOOP_PID_DIREVATIVE_TIME_CONSTANT 0
#define CURRENT_LOOP_LIMIT_VOLTS 48
#define DATA_FILE_NAME "../dat/demo-closedLoop-500-1000-137-345.dat"
#define PC_SIMULATION TRUE



#define MACHINE_TS         (CL_TS*TS_UPSAMPLING_FREQ_EXE) //1.25e-4 
#define MACHINE_TS_INVERSE (CL_TS_INVERSE*TS_UPSAMPLING_FREQ_EXE_INVERSE) // 8000

#endif
