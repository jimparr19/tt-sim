import numpy as np
from dataclasses import dataclass


@dataclass
class Wind:
    speed: float = 0
    direction: float = 0  # (from north=0, east=90,  south=180, west=270)

    def head_wind(self, heading: float) -> float:
        alpha = self.direction - heading
        head_wind_speed = self.speed * np.cos(np.deg2rad(alpha))
        return head_wind_speed
