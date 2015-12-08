import scipy.integrate as sp
import numpy as np
import pylab as pl

#Set initial values for variables
#Populations
sus = 0.9
zom = 0.05
safe = 0.01
dead = 0

#Rates
found = 0.2
hide = 0.1
natural_death = 0.01
zm = 0.1
gtf = 0.2
zfa = 0.06

#Either/or
car1 = 0.2
car2 = 0.5


#Create array for this stupid library
starting_values_array = [sus,zom,safe,dead]

#Create time points array
t_initial = 0
t_final = 20
t_step = 1
timepoints_array = np.arange(t_initial,t_final+t_step,t_step)
#print timepoints_array

#Produce array of differential equations
#Here are the differential equations
def diff_eqn_func(sva,timepoints_array):
    dSusc = (found*sva[2]) - (sva[0]*hide) - (sva[0]*natural_death) - (sva[0]*sva[1]*zm) - ((car1*sva[0]*sva[1])/4) - ((car2*sva[0]*sva[1])*3/4)
    dSafe = (hide*sva[0]) - (found*sva[2]) - (natural_death*sva[2])
    dDead = (natural_death*sva[2]) + (natural_death*sva[0]) + (zm*sva[0]*sva[1]) + (zfa*sva[1]) + (gtf*zom*sva[0])
    dZom = ((car1*sva[0]*sva[1])/4) + ((car2*sva[0]*sva[1])*3/4) - (zfa*sva[1]) - (gtf*sva[1]*sva[0])
    
    
    #Create array
    sva = np.zeros((4))
    sva[0] = dSusc
    sva[1] = dZom
    sva[2] = dSafe
    sva[3] = dDead
    
    #print sva 
    return sva

    
def ODE(diff_eqn_func,starting_values_array,timepoints_array):
    '''
    Solve differential equation with inputs of starting values and timepoints
    '''
    starting_values_array = tuple(starting_values_array)
    results_of_model = sp.odeint(diff_eqn_func,tuple(starting_values_array),timepoints_array)
    return results_of_model   

#Solve differential equations
#results_of_model = sp.odeint(diff_eqn_func,tuple(starting_values_array),timepoints_array)
#print results_of_model[:,1]
results_of_model = ODE(diff_eqn_func,tuple(starting_values_array),timepoints_array)
#print results_of_model

#Eperimental results to fit to
exp_res_zom = [0.05,0.05694128 ,0.06347877,0.06958322,0.0752466,0.08047126,0.08526295,0.0896278,0.0935709,0.09709625,0.10020732,0.10290781,0.10520244,0.10709755,
               0.10860157,0.1097252,0.11048151,0.11088583,0.1109555,0.11070961,0.1101686]

#Plots
pl.plot(results_of_model[:,0], '-bs', label='Susceptible')
pl.plot(results_of_model[:,1], '-ro', label='Zombies')
pl.plot(results_of_model[:,2], '-go', label='Safe')
pl.plot(results_of_model[:,3], '-ys', label='Dead')

pl.legend(loc = 0)
pl.title("Population change over time")
pl.xlabel("Time")
pl.ylabel("Dudes")
pl.savefig("2.5-SIS-high.png", dpi=900)
pl.show()

def changeValues(change_var_loc,change_val):
    #new_results = []
    '''
    Input: variable to change
    Output: range of values from differential equations- which then put in to residuals calulation
    '''

    #print starting_values_array
    #print diff_eqn_func(starting_values_array,timepoints_array)
    starting_values_array[change_var_loc] = change_val
    #print starting_values_array
    #print diff_eqn_func(starting_values_array,timepoints_array)
    #new_results.append(diff_eqn_func(starting_values_array,timepoints_array))
    #print ODE(diff_eqn_func,starting_values_array,timepoints_array)
    return ODE(diff_eqn_func,starting_values_array,timepoints_array)
    
#0 is susceptible, 1 is zombies, 2 is safe, 3 is dead
#We are looking at the effects on the zombie population. Therefore we always want column 1 for comparison.

zomb_col = 1

'''
column_change = 0
new_value = 0.45

column_change = 1
new_value = 0.025

column_change = 2
new_value = 0.005
'''
#Necessary becuase of the way this has been implemented- requires changing
#otherwise variables referenced before assignment
column_change = 0
new_value = 0.9

#column_change = 1
#new_value = 0.05

#print changeValues(column_change,new_value)[:,zomb_col]
residuals_sq = ((changeValues(column_change,new_value)[:,zomb_col] - exp_res_zom)**2)
#print residuals_sq
sum_residuals_sq = sum(residuals_sq)
print sum_residuals_sq

