import numpy as np

from tt_sim.core.rider import Rider
from tt_sim.core.bike import Bike
from tt_sim.core.wind import Wind
from tt_sim.core.stage import Stage, read_csv
from tt_sim.core.simulation import SimulationBikeChange


first_rider = Rider(name="Lander", mass=64, cda=0.22, cda_climb=0.3)
first_bike = Bike(name="Warp TT", mass=8.2, crr=0.003)

second_rider = Rider(name="Lander", mass=64, cda=0.3, cda_climb=0.3)
second_bike = Bike(name="Sultura", mass=6.47, crr=0.003)

wind = Wind()

# stage_data = read_csv(
#     file_path="./data",
#     file_name="Tour-de-France-2020---Stage-20-ITT.csv",
# )
stage_data = read_csv(
    file_path="./data",
    file_name="Tour-de-France-2023---Stage-16-ITT.csv",
)

stage = Stage(stage_data)

power_target = 370
power = power_target * np.ones(len(stage.distance))

# bike_change_distances = np.linspace(25000, 37000, 40)
bike_change_distances = np.linspace(10000, 23000, 40)
stage_time = np.zeros(len(bike_change_distances))
for i, bike_change_distance in enumerate(bike_change_distances):
    sim = SimulationBikeChange(
        first_rider=first_rider,
        first_bike=first_bike,
        second_rider=second_rider,
        second_bike=second_bike,
        wind=wind,
        stage=stage,
        power=power,
        bike_change_distance=bike_change_distance,
    )

    sim.solve_velocity_and_time()
    print(sim.time[-1])
    stage_time[i] = sim.time[-1]


import matplotlib
matplotlib.use("MACOSX")
import matplotlib.pyplot as plt

start_indx = np.argmin(np.abs(sim.stage.distance - bike_change_distances[0]))
end_index = np.argmin(np.abs(sim.stage.distance - bike_change_distances[-1]))

plt.figure()
plt.subplot(2, 1, 1)
plt.plot(sim.stage.distance[start_indx:end_index] / 1000, sim.stage.elevation[start_indx:end_index], '-')
plt.xlim((bike_change_distances[0]/1000, bike_change_distances[-1]/1000))
plt.ylabel('Elevation (m)')
plt.subplot(2, 1, 2)
plt.plot(bike_change_distances / 1000, stage_time, '.-')
plt.xlabel('Bike change distance (km)')
plt.ylabel('Race time (s)')
plt.show()

