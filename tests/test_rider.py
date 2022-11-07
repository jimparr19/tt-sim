import pytest
from tt_sim.core.rider import Rider, TeamRider

def test_team_rider_rider_distance():
    assert TeamRider(name='test', mass=70, cda=0.2)
    assert TeamRider(name='test', mass=70, cda=0.2, rider_distance=1)
    with pytest.raises(ValueError):
        TeamRider(name='test', mass=70, cda=0.2, rider_distance=10)


def test_team_rider_draft_cda():
    test_rider = TeamRider(name='test', mass=70, cda=0.2)
    with pytest.raises(ValueError):
        test_rider.draft_cda
        test_rider.position
    test_rider.n_riders = 8
    with pytest.raises(ValueError):
        test_rider.draft_cda
    test_rider.position = 1
    assert test_rider.draft_cda
    assert test_rider.draft_cda < test_rider.cda

def test_rider_to_json():
    rider = Rider(name='test', mass=70, cda=0.2, cp=400, w_prime=20000)
    assert rider.json() == '{"name": "test", "mass": 70, "cda": 0.2, "cp": 400, "w_prime": 20000}'

if __name__ == '__main__':
    pytest.main()