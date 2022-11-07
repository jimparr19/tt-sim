import numpy as np

from tt_sim.core.rider import Rider
from tt_sim.core.bike import Bike
from tt_sim.core.wind import Wind
from tt_sim.core.stage import Stage, read_csv
from tt_sim.core.simulation import Simulation


rider = Rider(name="Bradley", mass=70, cda=0.196)
bike = Bike(name="Track bike", mass=7, crr=0.0017)
wind = Wind()

stage_data = read_csv(
    file_path="./data",
    file_name="Tour-de-France-2020---Stage-20-ITT.csv",
)
stage = Stage(stage_data)

power_target = 440
power = power_target * np.ones(len(stage.distance))

sim = Simulation(rider=rider, bike=bike, wind=wind, stage=stage, power=power)
sim.solve_velocity_and_time()

print(sim.time[-1])


from scipy.interpolate import interp1d
from tt_sim.core.critical_power import CriticalPowerModel


def interpolate(x, y, xi, method="cubic"):
    y_interp = interp1d(x, y, kind=method, fill_value="extrapolate")
    return y_interp(xi)


seconds = np.arange(0, int(sim.time[-1] + 1))
power_per_second = power_target * np.ones(len(seconds))
cpm = CriticalPowerModel(cp=rider.cp, w_prime=rider.w_prime)
w_prime_balance_per_second = cpm.w_prime_balance(power=power_per_second)
w_prime_balance = interpolate(seconds, w_prime_balance_per_second, sim.time)
print("min w_prime = {}".format(min(w_prime_balance)))


import matplotlib

matplotlib.use("MACOSX")
import matplotlib.pyplot as plt

plt.figure()
plt.plot(sim.time, sim.power)
plt.show()