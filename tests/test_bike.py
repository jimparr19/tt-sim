from tt_sim.core.bike import Bike


def test_bike_to_json():
    bike = Bike(name="test", mass=10, crr=0.001)
    assert bike.json() == '{"name": "test", "mass": 10, "crr": 0.001}'
