from tt_sim.core.wind import Wind

def test_head_wind():
    wind = Wind(speed=10, direction=180)
    assert wind.head_wind(0) == -10

def test_tail_wind():
    wind = Wind(speed=10, direction=0)
    assert wind.head_wind(0) == 10

if __name__ == '__main__':
    import pytest
    pytest.main()