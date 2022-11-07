import numpy as np
import time
from tt_sim.core.rider import TeamRider
from tt_sim.core.bike import Bike
from tt_sim.core.wind import Wind
from tt_sim.core.stage import Stage, read_csv
from tt_sim.core.simulation import TeamSimulation

from collections import namedtuple

RiderStats = namedtuple("RiderStats", ["mass", "cp", "w_prime", "pull_lb", "pull_ub"])

bevin_stats = RiderStats(74.6, 6.0, 20.1, 60, 90)  # all-rounder
de_marchi_stats = RiderStats(69.5, 6.3, 17.3, 60, 90)  # climber
einhorn_stats = RiderStats(73.7, 4.7, 25.7, 30, 45)  # sprinter
froome_stats = RiderStats(67.5, 5.6, 14.3, 45, 60)  # GC
goldstein_stats = RiderStats(60.6, 5.4, 18.2, 30, 45)  # puncheur
hagen_stats = RiderStats(63.3, 6.1, 16.1, 30, 45)  # climber
impey_stats = RiderStats(70.5, 5.3, 17.8, 60, 90)  # all-rounder
woods_stats = RiderStats(62.0, 6.2, 14.9, 30, 45)  # climber

leading_power_cp_factor = 1.3
cda = 0.22

bevin = TeamRider(
    name="Bevin",
    mass=bevin_stats.mass,
    cda=cda,
    pull_duration=(bevin_stats.pull_ub + bevin_stats.pull_ub) / 2,
    leading_power=bevin_stats.mass * bevin_stats.cp * leading_power_cp_factor,
    cp=bevin_stats.mass * bevin_stats.cp,
    w_prime=bevin_stats.w_prime * 1000,
)

de_marchi = TeamRider(
    name="De Marchi",
    mass=de_marchi_stats.mass,
    cda=cda,
    pull_duration=(de_marchi_stats.pull_ub + de_marchi_stats.pull_ub) / 2,
    leading_power=de_marchi_stats.mass * de_marchi_stats.cp * leading_power_cp_factor,
    cp=de_marchi_stats.mass * de_marchi_stats.cp,
    w_prime=de_marchi_stats.w_prime * 1000,
)
einhorn = TeamRider(
    name="Einhorm",
    mass=einhorn_stats.mass,
    cda=cda,
    pull_duration=(einhorn_stats.pull_ub + einhorn_stats.pull_ub) / 2,
    leading_power=einhorn_stats.mass * einhorn_stats.cp * leading_power_cp_factor,
    cp=einhorn_stats.mass * einhorn_stats.cp,
    w_prime=einhorn_stats.w_prime * 1000,
)
froome = TeamRider(
    name="Froome",
    mass=froome_stats.mass,
    cda=cda,
    pull_duration=(froome_stats.pull_ub + froome_stats.pull_ub) / 2,
    leading_power=froome_stats.mass * froome_stats.cp * leading_power_cp_factor,
    cp=froome_stats.mass * froome_stats.cp,
    w_prime=froome_stats.w_prime * 1000,
)
goldstein = TeamRider(
    name="Goldstein",
    mass=goldstein_stats.mass,
    cda=cda,
    pull_duration=(goldstein_stats.pull_ub + goldstein_stats.pull_ub) / 2,
    leading_power=goldstein_stats.mass * goldstein_stats.cp * leading_power_cp_factor,
    cp=goldstein_stats.mass * goldstein_stats.cp,
    w_prime=goldstein_stats.w_prime * 1000,
)
hagen = TeamRider(
    name="Hagen",
    mass=hagen_stats.mass,
    cda=cda,
    pull_duration=(hagen_stats.pull_ub + hagen_stats.pull_ub) / 2,
    leading_power=hagen_stats.mass * hagen_stats.cp * leading_power_cp_factor,
    cp=hagen_stats.mass * hagen_stats.cp,
    w_prime=hagen_stats.w_prime * 1000,
)
impey = TeamRider(
    name="Impey",
    mass=impey_stats.mass,
    cda=cda,
    pull_duration=(impey_stats.pull_ub + impey_stats.pull_ub) / 2,
    leading_power=impey_stats.mass * impey_stats.cp * leading_power_cp_factor,
    cp=impey_stats.mass * impey_stats.cp,
    w_prime=impey_stats.w_prime * 1000,
)
woods = TeamRider(
    name="Woods",
    mass=woods_stats.mass,
    cda=cda,
    pull_duration=(woods_stats.pull_ub + woods_stats.pull_ub) / 2,
    leading_power=woods_stats.mass * woods_stats.cp * leading_power_cp_factor,
    cp=woods_stats.mass * woods_stats.cp,
    w_prime=woods_stats.w_prime * 1000,
)

# baseline
riders = (impey, einhorn, de_marchi, woods, hagen, bevin, goldstein, froome)

for rider in riders:
    rider.n_riders = len(riders)

# # alternative 1
# riders = (woods, de_marchi, hagen, froome, impey, bevin, einhorn, goldstein)

# # alternative 2
# riders = (hagen, de_marchi, bevin, einhorn, froome, goldstein, woods, impey)

bike = Bike(name="Slick", mass=7, crr=0.0017)
wind = Wind()
# wind = Wind(speed=3, direction=225)
stage_data = read_csv(
    file_path="./data",
    file_name="La-Vuelta-2022---Stage-1-TTT.csv",
)
stage = Stage(stage_data)


if __name__ == "__main__":
    start_time = time.time()
    sim = TeamSimulation(riders=riders, bike=bike, wind=wind, stage=stage)
    sim.solve_velocity_and_time()
    print(f"elapsed time = {time.time() - start_time}")

    print(f"race time = {sim.time[-1]}")
    print(f"race time = {sim.time[-1]/60}")

# import matplotlib

# matplotlib.use("MACOSX")
# import matplotlib.pyplot as plt


from scipy.interpolate import interp1d

from tt_sim.core.critical_power import CriticalPowerModel


def interpolate(x, y, xi, method="linear"):
    y_interp = interp1d(x, y, kind=method, fill_value="extrapolate")
    return y_interp(xi)


# plt.figure()
# plt.subplot(4, 1, 1)

seconds = np.arange(0, int(sim.time[-1] + 1))
for rider_index, rider in enumerate(riders):
    power_per_second = interpolate(sim.time, sim.power[rider_index], seconds)
    cpm = CriticalPowerModel(cp=rider.cp, w_prime=rider.w_prime)
    w_prime_balance_per_second = cpm.w_prime_balance(power=power_per_second)
    w_prime_balance = interpolate(seconds, w_prime_balance_per_second, sim.time)
#     plt.plot(sim.stage.distance, w_prime_balance, label=rider.name)

print(f"elapsed time = {time.time() - start_time}")
# plt.legend()

# plt.subplot(4, 1, 2)
# for rider_index, rider in enumerate(riders):
#     plt.plot(sim.stage.distance, sim.power[rider_index], label=rider.name)
# plt.ylabel("power")
# plt.legend()

# plt.subplot(4, 1, 3)
# plt.plot(sim.stage.distance, sim.velocity * (60*60)/1000)
# plt.ylabel("velocity")
# plt.legend()

# plt.subplot(4, 1, 4)
# plt.plot(sim.stage.distance, sim.stage.elevation)
# plt.ylabel("elevation")
# plt.show()
