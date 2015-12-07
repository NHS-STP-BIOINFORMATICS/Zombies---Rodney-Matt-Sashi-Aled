import scipy.integrate as sp
import numpy as np
import pylab as pl

#Set initial values for variables
#Populations
sus = 0.3
zom = 0.3
safe = 0.2
dead = 0.2

#Rates
found = 0.5
hide = 0.7
natural_death = 0.1
zm = 0.2
gtf = 0.4
zfa = 0.2

#Either/or
car1 = 0
car2 = 0


#Create array for this stupid library
starting_values_array = (sus,zom,safe,dead)

#Create time points array
t_initial = 0
t_final = 10
t_step = 1
timepoints_array = np.arange(t_initial,t_final+t_step,t_step)
#print timepoints_array

#Produce array of differential equations
#Here are the differential equations
def diff_eqn_func(sva,timepoints_array):
    dSusc = (found*sva[2]) - (sva[0]*hide) - (sva[0]*natural_death) - (sva[0]*sva[1]*zm) - (car1*sva[0]*sva[1]) - (car2*sva[0]*sva[1])
    dSafe = (hide*sva[0]) - (found*sva[2]) - (natural_death*sva[2])
    dDead = (natural_death*sva[2]) + (natural_death*sva[0]) + (zm*sva[0]*sva[1]) + (zfa*sva[1]) + (gtf*zom*sva[0])
    dZom = (car1*sva[0]*sva[1]) + (car2*sva[0]*sva[1]) - (zfa*sva[1]) - (gtf*sva[1]*sva[0])
    
    
    #Create array
    sva = np.zeros((4))
    sva[0] = dSusc
    sva[1] = dZom
    sva[2] = dSafe
    sva[3] = dDead
    
    #print sva 
    return sva
    
#Solve differential equations
results_of_model = sp.odeint(diff_eqn_func,starting_values_array,timepoints_array)
#print results_of_model    

#Plots
pl.plot(results_of_model[:,0], '-bs', label='Susceptible')
pl.plot(results_of_model[:,1], '-ro', label='Zombies')
pl.plot(results_of_model[:,2], '-go', label='Safe')
pl.plot(results_of_model[:,3], '-ys', label='Dead')

pl.legend(loc = 0)
pl.title("Thing")
pl.xlabel("Time")
pl.ylabel("Dudes")
pl.savefig("2.5-SIS-high.png", dpi=900)
pl.show()
