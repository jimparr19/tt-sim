import pytest
import numpy as np

from tt_sim.core.rider import Rider, TeamRider
from tt_sim.core.bike import Bike
from tt_sim.core.wind import Wind
from tt_sim.core.stage import Stage, get_default_stage
from tt_sim.core.simulation import Simulation, TeamSimulation, SimulationWithWPrimeBalance

@pytest.fixture
def rider():
    return Rider(name='Bradley', mass=70, cda=0.196)

@pytest.fixture
def bike():
    return Bike(name='Track bike', mass=7, crr=0.0017)


@pytest.fixture
def wind():
    return Wind()

@pytest.fixture
def stage():
    stage_data = get_default_stage()
    return Stage(stage_data=stage_data)

def test_hour_record(rider, bike, wind, stage):    
    power = 440 * np.ones(len(stage.distance))
    sim = Simulation(rider=rider, bike=bike, wind=wind, stage=stage, power=power)
    sim.solve_velocity_and_time()
    assert abs(sim.time[-1] - 3600) < 1

def test_hour_record_with_head_wind(rider, bike, stage):
    wind = Wind(direction=0, speed=10)
    power = 440 * np.ones(len(stage.distance))
    sim = Simulation(rider=rider, bike=bike, wind=wind, stage=stage, power=power)
    sim.solve_velocity_and_time()
    assert (sim.time[-1] - 3600) > 60

def test_hour_record_with_tail_wind(rider, bike, stage):
    wind = Wind(direction=180, speed=10)
    power = 440 * np.ones(len(stage.distance))
    sim = Simulation(rider=rider, bike=bike, wind=wind, stage=stage, power=power)
    sim.solve_velocity_and_time()
    assert (sim.time[-1] - 3600) < -60

def test_team_time_trial(bike, wind, stage):
    team_rider = TeamRider(name='Bradley', mass=70, cda=0.196, pull_duration=30, leading_power=440)
    team_rider.n_riders = 1
    team_rider.position = 0
    sim = TeamSimulation(riders=[team_rider], bike=bike, wind=wind, stage=stage)
    sim.solve_velocity_and_time()
    assert abs(sim.time[-1] - 3600) < 1

def test_hour_record_with_w_prime_balance(rider, bike, wind, stage):    
    power = 440 * np.ones(len(stage.distance))
    sim = SimulationWithWPrimeBalance(rider=rider, bike=bike, wind=wind, stage=stage, power=power)
    sim.solve_velocity_and_time()
    assert abs(sim.time[-1] - 3600) < 1

if __name__ == '__main__':
    import pytest
    pytest.main([__file__])