import numpy as np

from tt_sim.core.rider import Rider
from tt_sim.core.bike import Bike
from tt_sim.core.wind import Wind
from tt_sim.core.stage import Stage
from tt_sim.core.simulation import Simulation


rider = Rider(name='Bradley', mass=70, cda=0.196)
bike = Bike(name='Track bike', mass=7, crr=0.0017)
wind = Wind()
stage = Stage(name='Hour record track')

power = 440 * np.ones(len(stage.distance))

sim = Simulation(rider=rider, bike=bike, wind=wind, stage=stage, power=power)
sim.solve_velocity_and_time()

print(sim.time[-1])