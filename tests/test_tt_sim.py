import numpy as np

from tt_sim import __version__

from tt_sim.core.rider import Rider
from tt_sim.core.bike import Bike
from tt_sim.core.wind import Wind
from tt_sim.core.stage import Stage
from tt_sim.core.simulation import Simulation


def test_version():
    assert __version__ == '0.1.0'


def test_hour_record():
    rider = Rider(name='Bradley', mass=70, cda=0.2)
    bike = Bike(name='Track bike', mass=7)
    wind = Wind()
    stage = Stage(name='Hour record track')
    
    power = 440 * np.ones(len(stage.distance))
    
    sim = Simulation(rider=rider, bike=bike, wind=wind, stage=stage, power=power)
    t = sim.solve_velocity_and_time()

