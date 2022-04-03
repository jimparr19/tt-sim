import numpy as np

from tt_sim.core.rider import Rider, TeamRider
from tt_sim.core.bike import Bike
from tt_sim.core.wind import Wind
from tt_sim.core.stage import Stage
from tt_sim.core.simulation import Simulation, Environment, get_purmutations

from collections import deque

environment = Environment()

# specify initial rider order
riders = [
    TeamRider(
        name="Bradley1", mass=70, cda=0.196, pull_duration=200, position=0, n_riders=3, cp=300, w_prime=19800
    ),
    TeamRider(
        name="Bradley2", mass=70, cda=0.196, pull_duration=200, position=1, n_riders=3
    ),
    TeamRider(
        name="Bradley3", mass=70, cda=0.196, pull_duration=200, position=2, n_riders=3
    ),
]

bike = Bike(name="Track bike", mass=7, crr=0.0017)
wind = Wind()
stage = Stage(name="Hour record track")

# specify leading power and then each rider matches this velocity
leading_power = 440

# (or specify a target power for each rider when leading?)

# specify pull duration for each rider (assume 30s)
pull_duration = 30

# 1. Get an estimate for the race duration (leading rider at leading power but full cda)
rider = Rider(name=riders[0].name, mass=riders[0].mass, cda=riders[0].cda)
sim = Simulation(
    rider=rider,
    bike=bike,
    wind=wind,
    stage=stage,
    power=leading_power * np.ones(len(stage.distance)),
)
sim.solve_velocity_and_time()
t_guess = sim.time[-1]

# 2. get purmutation for each time step
t_step = 1
time_permutations, position_permutaions = get_purmutations(riders, t_guess, t_step)
print(len(position_permutaions), len(time_permutations))

# 3. solve for each rider in each time step 
v0 = 1
velocity = np.zeros(len(stage.distance))
time = np.zeros(len(stage.distance))
velocity[0] = v0
max_g_long = 4
max_velocity = 30
for step in range(1, len(stage.distance)):
    t = time[step - 1]
    permutation_index = np.argmin(np.abs(time_permutations - t))
    lead_rider_index = position_permutaions[permutation_index][0]
    v = velocity[step - 1]
    vw = wind.head_wind(stage.heading[step])
    r_gradient = stage.gradient[step]
    velocity_target = velocity[step - 1]
    for rider_index, rider in enumerate(riders):
        rider_position = position_permutaions[permutation_index][rider_index]
        rider.set_position(rider_position)
        f_drag = 0.5 * environment.air_density * rider.draft_cda * (v + vw) ** 2
        f_gravity = (
            (rider.mass + bike.mass) * environment.gravity * np.sin(np.arctan(r_gradient))
        )
        f_rolling = (
            (bike.crr * rider.mass)
            * environment.gravity
            * np.cos(np.arctan(r_gradient))
        )
        if (rider_index == 0) & (lead_rider_index == 0):
            f_tyre = leading_power / v
            g_long = min(
                max_g_long, (f_tyre - f_drag - f_gravity - f_rolling) / (rider.mass + bike.mass)
            )
            dv = (g_long / v) * stage.s_step
            dt = (1 / v) * stage.s_step
            rider.time.append(t + dt)
            rider.velocity.append(min(v + dv, max_velocity))
            rider.power.append(leading_power)
            velocity_target = rider.velocity[-1]
        else:
            dt = (1 / velocity_target) * stage.s_step
            rider.time.append(t + dt)
            rider.velocity.append(velocity_target)
            rider.power.append((f_drag + f_gravity + f_rolling) * velocity_target)

    time[step] = riders[lead_rider_index].time[-1]      
    velocity[step] = riders[lead_rider_index].velocity[-1] 

print(time[-1])

import matplotlib
matplotlib.use('MACOSX')
import matplotlib.pyplot as plt

# plt.figure()
# plt.plot(riders[0].time, riders[0].power)
# plt.plot(riders[1].time, riders[1].power)
# plt.show()

# a) during lead out solve for distance given time and power for lead rider and solve for power given velcity and time for other riders
# b) after leadout - solve for distance and power given velocity and time for lead rider

# what happends during gradient - max power needs to be applied rather than match velcoity?

from scipy.interpolate import interp1d

from tt_sim.core.critical_power import CriticalPowerModel

def interpolate(x, y, xi, method="linear"):
    y_interp = interp1d(x, y, kind=method, fill_value="extrapolate")
    return y_interp(xi)

plt.figure()

seconds = np.arange(0, int(sim.time[-1] + 1))
for rider in riders:
    power_per_second = interpolate(rider.time, rider.power, seconds)
    cpm = CriticalPowerModel(cp=rider.cp, w_prime=rider.w_prime)
    w_prime_balance_per_second = cpm.w_prime_balance(power=power_per_second)
    w_prime_balance = interpolate(seconds, w_prime_balance_per_second, sim.time)
    plt.plot(sim.time, w_prime_balance, label=rider.name)

plt.legend()
plt.show()
