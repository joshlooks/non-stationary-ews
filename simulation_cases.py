import sys
import numpy as np
import os
from scipy.interpolate import interp1d
import errno

def gillespie_sir(N, beta_func, gamma, mu, initial_susceptible, initial_infected, max_time):
    # Initial conditions
    S = initial_susceptible
    I = initial_infected
    R = N - S - I
    
    # Arrays to store results
    times = np.zeros(N*3)
    susceptible = np.zeros(N*3)
    susceptible[0] = S
    infected = np.zeros(N*3)
    infected[0] = I
    recovered = np.zeros(N*3)
    recovered[0] = R
    cases = np.zeros(N*3)
    cases[0] = I
    C = I + 0
    t = 0
    ind = 0
    beta = beta_func(t)
    while t < max_time:
        # Calculate rates (transmission, symptom onset, recovery, birth and deaths)
        beta = beta_func(t)
        lambda_SI = beta * S * I / N
        lambda_IR = gamma * I
        lambda_birth = mu * N
        lambda_death_S = mu * S
        lambda_death_I = mu * I
        lambda_death_R = mu * R
        total_rate = (lambda_SI + lambda_IR + lambda_birth + lambda_death_S + lambda_death_I + lambda_death_R)
        
        if total_rate == 0:
            break
        
        # Calculate time step
        dt = np.random.exponential(1 / total_rate)
        t += dt
        ind += 1
    
        # Determine which event occurs
        rand = np.random.rand() * total_rate
        
        # Work out which event had happened
        if rand < lambda_SI:
            S -= 1
            I += 1
        elif rand < lambda_SI + lambda_IR:
            I -= 1
            C += 1
            R += 1
        elif rand < lambda_SI + lambda_IR + lambda_birth:
            S += 1
        else:
            rand_death = rand - (lambda_SI + lambda_IR + lambda_birth)
            if rand_death < lambda_death_S:
                S -= 1
            elif rand_death < lambda_death_S + lambda_death_I:
                I -= 1
            else:
                R -= 1
        
        # Append results
        times[ind] = t
        susceptible[ind] = S
        infected[ind] = I
        recovered[ind] = R
        cases[ind] = C
    
    return times[:ind+1], susceptible[:ind+1], infected[:ind+1], recovered[:ind+1], cases[:ind+1]

num = int(sys.argv[1])
sim_type = sys.argv[2]
script_dir = os.path.dirname(__file__)

# Constant Parameters
N = int(sys.argv[3])  # Total population
gamma = 1/14  # Recovery rate (1/gamma is the infectious period)
mu = 0.00003424657  # Birth and death rate

if sim_type == 'high':
    initial_susceptible = 0.4*N
    initial_infected = 0.005*N
    R_0 = 4
    beta_0 = R_0*(gamma+mu)
elif sim_type == 'low':
    initial_susceptible = 0.9*N
    initial_infected = 0.1*N
    beta_0 = 0.06
    R_0 = 0.06/(gamma+mu)
elif sim_type == 'highrand':
    initial_susceptible, initial_infected, _ = np.random.multinomial(N,[0.4,0.005,1-0.4-0.005])
    R_0 = 4
    beta_0 = R_0*(gamma+mu)
elif sim_type == 'lowrand':
    initial_susceptible, initial_infected, _ = np.random.multinomial(N,[0.9,0.1,0])
    beta_0 = 0.06
    R_0 = 0.06/(gamma+mu)

max_time = 250
sim_type = sys.argv[2]
script_dir = os.path.dirname(__file__)
betat = lambda x: beta_0

def sim():
    return gillespie_sir(N, betat, gamma, mu, initial_susceptible, initial_infected, max_time)

res_dict = {}
for i in range(100):
    res = sim()
    res_dict[i] = {'t':res[0],'s':res[1],'i':res[2],'r':res[3],'c':res[4]}

results_dir = os.path.join(script_dir,sim_type,f'{N}')
try:
    os.makedirs(results_dir)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

i = np.random.randint(100)
import pickle
fpath_dict = os.path.join(results_dir,f'{num}_{i}.pkl')
with open(fpath_dict, 'wb') as f:
    pickle.dump(res_dict, f)