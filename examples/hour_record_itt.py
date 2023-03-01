import numpy as np

from tt_sim.core.rider import Rider
from tt_sim.core.bike import Bike
from tt_sim.core.wind import Wind
from tt_sim.core.stage import Stage, get_default_stage
from tt_sim.core.simulation import Simulation, SimulationWithWPrimeBalance


rider = Rider(name="Bradley", mass=70, cda=0.196, cp = 440, w_prime = 19800)
bike = Bike(name="Track bike", mass=7, crr=0.0017)
wind = Wind()
stage_data = get_default_stage()
stage = Stage(stage_data=stage_data)

power_target = 440
power = power_target * np.ones(len(stage.distance))

power[10000:20000] = 300

sim = Simulation(rider=rider, bike=bike, wind=wind, stage=stage, power=power)
sim.solve_velocity_and_time()

print(sim.time[-1])


from scipy.interpolate import interp1d
from tt_sim.core.critical_power import CriticalPowerModel


def interpolate(x, y, xi, method="cubic"):
    y_interp = interp1d(x, y, kind=method, fill_value="extrapolate")
    return y_interp(xi)


seconds = np.arange(0, int(sim.time[-1] + 1))
# power_per_second = power_target * np.ones(len(seconds))

power_per_second = interpolate(sim.time, sim.power, seconds)
cpm = CriticalPowerModel(cp=rider.cp, w_prime=rider.w_prime)
w_prime_balance_per_second = cpm.w_prime_balance(power=power_per_second)
w_prime_balance = interpolate(seconds, w_prime_balance_per_second, sim.time)
print("final w_prime = {}".format(w_prime_balance[-1]))
print("min w_prime = {}".format(min(w_prime_balance)))

# using the sim with wprime balance


sim = SimulationWithWPrimeBalance(rider=rider, bike=bike, wind=wind, stage=stage, power=power)
sim.solve_velocity_and_time()

print("final w_prime = {}".format(sim.w_prime_remaining[-1]))
print("min w_prime = {}".format(min(sim.w_prime_remaining)))


import matplotlib.pylab as plt
plt.figure()
plt.plot(sim.time, sim.w_prime_remaining, label='dynamic')
# plt.plot(sim.time, w_prime_balance, label='static')
# plt.plot(sim.time, sim.tau)
plt.show()
