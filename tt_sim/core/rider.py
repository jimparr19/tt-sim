import json
from dataclasses import dataclass, asdict

drag_scaling_factors = {
    0.05: [
        [100.0],
        [97.6, 64.1],
        [97.2, 61.7, 51.7],
        [97.1, 61.2, 49.5, 45.9],
        [97.1, 61.1, 49.1, 43.9, 43.6],
        [97.1, 61.0, 48.9, 43.4, 41.7, 42.5],
        [97.0, 61.0, 48.8, 43.2, 41.2, 40.7, 41.9],
        [97.0, 61.0, 48.8, 43.2, 41.0, 40.2, 40.1, 41.5],
        [97.0, 61.0, 48.8, 43.2, 41.0, 40.1, 39.7, 39.8, 41.2],
    ],
    0.15: [
        [100.0],
        [98.0, 64.4],
        [97.7, 62.2, 52.2],
        [97.6, 61.8, 50.2, 46.6],
        [97.5, 61.7, 49.8, 44.7, 44.3],
        [97.5, 61.6, 49.7, 44.3, 42.6, 43.3],
        [97.5, 61.6, 49.6, 44.2, 42.2, 41.7, 42.7],
        [97.5, 61.6, 49.6, 44.1, 42.0, 41.3, 41.1, 42.3],
        [97.5, 61.6, 49.6, 44.1, 42.0, 41.1, 40.7, 40.8, 42.0],
    ],
    0.50: [
        [100.0],
        [98.7, 65.2],
        [98.4, 63.4, 53.6],
        [98.4, 63.4, 52.3, 48.6],
        [98.4, 63.4, 52.0, 47.1, 46.6],
        [98.4, 63.3, 51.9, 46.8, 45.2, 45.7],
        [98.4, 63.3, 51.9, 46.7, 44.9, 44.4, 45.2],
        [98.4, 63.3, 51.9, 46.7, 44.9, 44.1, 43.9, 44.8],
        [98.4, 63.3, 51.8, 46.7, 44.8, 44, 43.6, 43.6, 44.6],
    ],
    1.00: [
        [100.0],
        [99.2, 66.5],
        [99.1, 65.5, 55.6],
        [99.0, 65.3, 54.6, 51.1],
        [99.0, 65.2, 54.4, 50.0, 49.3],
        [99.0, 65.2, 54.4, 49.9, 48.4, 48.5],
        [99.0, 65.2, 54.3, 49.7, 48.1, 47.5, 48.1],
        [99.0, 65.2, 54.3, 49.7, 48.0, 47.4, 47.2, 47.8],
        [99.0, 65.2, 54.3, 49.7, 48.0, 47.3, 47.0, 46.9, 47.5],
    ],
    5.00: [
        [100.0],
        [99.9, 79.9],
        [99.9, 70.8, 63.1],
        [99.9, 70.8, 63.0, 61.1],
        [99.9, 70.8, 63.0, 61.0, 60.5],
        [99.9, 70.8, 63.0, 61.0, 60.4, 60.2],
        [99.9, 70.8, 63.0, 61.0, 60.4, 60.1, 60.1],
        [99.9, 70.8, 63.0, 61.0, 60.4, 60.1, 60.0, 60.1],
        [99.9, 70.8, 63.0, 61.0, 60.4, 60.1, 59.9, 60.0, 60.4],
    ],
}


@dataclass
class Rider:
    name: str
    mass: float
    cda: float
    cda_climb: float = 0.3
    cp: float = 380
    w_prime: float = 19800

    def json(self):
        return json.dumps(asdict(self))


@dataclass
class TeamRider(Rider):
    pull_duration: float = None
    leading_power: float = None
    rider_distance: float = 0.05 # should be in drag_scaling_factors.keys()
    dropped: bool = False # set to true if rider gets dropped

    def __post_init__(self):
        if self.rider_distance not in drag_scaling_factors.keys():
            raise ValueError(f'The rider_distance must be a value from {drag_scaling_factors.keys()}')

    @property
    def n_riders(self):
        return self._n_riders

    @n_riders.setter
    def n_riders(self, value):
        if value > 9:
            raise ValueError("The maximum number of riders is 9")
        self._n_riders = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        if hasattr(self, "n_riders"):
            if value > self.n_riders:
                raise ValueError(
                    "The position must be less or equal to the number of riders."
                )
        else:
            raise ValueError("The number of riders n_riders must be set.")
        self._position = value

    @property
    def draft_cda(self) -> float:
        if all(hasattr(self, attr) for attr in ["position", "n_riders"]):
            draft_factor = (
                drag_scaling_factors[self.rider_distance][self.n_riders - 1][
                    self.position
                ]
                / 100
            )
            return self.cda * draft_factor
        else:
            raise ValueError(
                f"You must set n_riders and position to calculate the draft_cda."
            )