import json
from dataclasses import dataclass, asdict

@dataclass
class Bike:
    name: str
    mass: float
    crr: float = 0.003  # tyre rolling resistance coefficient

    def json(self):
        return json.dumps(asdict(self))
