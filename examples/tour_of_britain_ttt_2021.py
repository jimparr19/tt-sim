import numpy as np

from tt_sim.core.rider import TeamRider
from tt_sim.core.bike import Bike
from tt_sim.core.wind import Wind
from tt_sim.core.stage import Stage, read_csv
from tt_sim.core.simulation import TeamSimulation

# specify pull duration for each rider (assume 30s)
pull_duration = 30

# specify initial rider order
rider1 = TeamRider(
    name="Bradley1",
    mass=70,
    cda=0.196,
    pull_duration=pull_duration,
    leading_power=370,
    cp=300,
    w_prime=19800,
)
rider2 = TeamRider(
    name="Bradley2",
    mass=70,
    cda=0.196,
    pull_duration=pull_duration,
    leading_power=400,
    cp=370,
    w_prime=19800,
)

rider3 = TeamRider(
    name="Bradley3",
    mass=70,
    cda=0.196,
    pull_duration=120,
    leading_power=390,
    cp=360,
    w_prime=19800,
)
riders = (rider1, rider2, rider3)

for rider in riders:
    rider.n_riders = len(riders)

bike = Bike(name="Track bike", mass=7, crr=0.0017)
wind = Wind()

stage_data = read_csv(
    file_path="./data",
    file_name="Tour-of-Britain-2021---Stage-3-TTT.csv",
)
stage = Stage(stage_data)

sim = TeamSimulation(riders=riders, bike=bike, wind=wind, stage=stage)
sim.solve_velocity_and_time()

print(f"race time = {sim.time[-1]}")

import matplotlib

matplotlib.use("MACOSX")
import matplotlib.pyplot as plt


from scipy.interpolate import interp1d

from tt_sim.core.critical_power import CriticalPowerModel


def interpolate(x, y, xi, method="linear"):
    y_interp = interp1d(x, y, kind=method, fill_value="extrapolate")
    return y_interp(xi)


plt.figure()
plt.subplot(3, 1, 1)

seconds = np.arange(0, int(sim.time[-1] + 1))
for rider_index, rider in enumerate(riders):
    power_per_second = interpolate(sim.time, sim.power[rider_index], seconds)
    cpm = CriticalPowerModel(cp=rider.cp, w_prime=rider.w_prime)
    w_prime_balance_per_second = cpm.w_prime_balance(power=power_per_second)
    w_prime_balance = interpolate(seconds, w_prime_balance_per_second, sim.time)
    plt.plot(sim.time, w_prime_balance, label=rider.name)

plt.legend()

plt.subplot(3, 1, 2)
for rider_index, rider in enumerate(riders):
    plt.plot(sim.time, sim.power[rider_index], label=rider.name)
plt.ylabel("power")
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(sim.time, sim.stage.elevation)
plt.ylabel("elevation")

plt.show()
