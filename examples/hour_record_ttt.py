from importlib.abc import SourceLoader
import numpy as np

from tt_sim.core.rider import Rider, TeamRider
from tt_sim.core.bike import Bike
from tt_sim.core.wind import Wind
from tt_sim.core.stage import Stage, get_default_stage
from tt_sim.core.simulation import TeamSimulationWithDropouts, Environment, get_purmutations

from collections import deque

environment = Environment()

# specify initial rider order
riders = [
    TeamRider(
        name="Bradley1",
        mass=70,
        cda=0.196,
        pull_duration=50,
        leading_power = 380,
        cp=300,
        w_prime=19800,
    ),
    TeamRider(
        name="Bradley2",
        mass=70,
        cda=0.196,
        pull_duration=20,
        leading_power = 380,
        cp=300,
        w_prime=19800,
    ),
    TeamRider(
        name="Bradley3",
        mass=70,
        cda=0.196,
        pull_duration=20,
        leading_power = 380,
        cp=300,
        w_prime=19800,
    ),
]

bike = Bike(name="Track bike", mass=7, crr=0.0017)
wind = Wind()
stage = Stage(get_default_stage())

for rider in riders:
    rider.n_riders = len(riders)

sim = TeamSimulationWithDropouts(riders=riders, bike=bike, wind=wind, stage=stage)
sim.solve_velocity_and_time()

import matplotlib.pylab as plt

from scipy.interpolate import interp1d

from tt_sim.core.critical_power import CriticalPowerModel


def interpolate(x, y, xi, method="linear"):
    y_interp = interp1d(x, y, kind=method, fill_value="extrapolate")
    return y_interp(xi)


plt.figure()

plt.subplot(3, 1, 1)
for rider_index, rider in enumerate(riders):
    plt.plot(sim.stage.distance, sim.power[rider_index], label=rider.name)

# seconds = np.arange(0, int(sim.time[-1] + 1))
# for rider_index, rider in enumerate(riders):
#     power_per_second = interpolate(sim.time, sim.power[rider_index], seconds)
#     cpm = CriticalPowerModel(cp=rider.cp, w_prime=rider.w_prime)
#     w_prime_balance_per_second = cpm.w_prime_balance(power=power_per_second)
#     w_prime_balance = interpolate(seconds, w_prime_balance_per_second, sim.time)
#     plt.plot(sim.time, w_prime_balance, label=rider.name)

# plt.legend()

print(f"n_riders finished = {sum([not rider.dropped for rider in sim.riders])}")

plt.subplot(3, 1, 2)
for rider_index, rider in enumerate(riders):
    plt.plot(sim.stage.distance, sim.w_prime_remaining[rider_index], label=rider.name)


plt.subplot(3, 1, 3)
plt.plot(sim.stage.distance, sim.stage.elevation)

plt.legend()
plt.show()
