import os

import pandas as pd
import numpy as np

from typing import NamedTuple, List, Union

from scipy.signal import butter
from scipy.signal import filtfilt
from scipy.interpolate import interp1d

from geographiclib.geodesic import Geodesic


class FilterConfigData(NamedTuple):
    gain: float
    offset: float
    frequency: float


class StageData(NamedTuple):
    name: str
    latitude: List[float]
    longitude: List[float]
    elevation: List[float]
    distance: List[float]
    heading: List[float]


def read_csv(file_path: str, file_name: str) -> StageData:
    data = pd.read_csv(os.path.join(file_path, file_name))
    latitude = data.latitude.tolist()
    longitude = data.longitude.tolist()
    heading = compute_heading(latitude, longitude)

    return StageData(
        name=file_name.split(".")[0],
        latitude=latitude,
        longitude=longitude,
        distance=data.distance.tolist(),
        elevation=data.elevation.tolist(),
        heading=heading,
    )


def compute_heading(latitude: List[float], longitude: List[float]) -> List[float]:
    heading = [0] * len(latitude)
    for i in range(len(latitude) - 1):
        geodesic = Geodesic.WGS84.Inverse(
            latitude[i], longitude[i], latitude[i + 1], longitude[i + 1]
        )
        if geodesic["azi1"] < 0:
            heading[i] = geodesic["azi1"] + 360
        else:
            heading[i] = geodesic["azi1"]
    return heading


def get_default_stage(name: str = "Default Track", s_step: float = 1) -> StageData:
    # default track
    distance = np.arange(0, 54526, s_step).tolist()
    elevation_gain = 0
    elevation = np.linspace(0, elevation_gain, len(distance)).tolist()
    latitude = np.linspace(0, 0, len(distance)).tolist()
    longitude = np.linspace(0, 0, len(distance)).tolist()
    heading = np.linspace(0, 0, len(distance)).tolist()
    stage_data = StageData(
        name=name,
        latitude=latitude,
        longitude=longitude,
        distance=distance,
        elevation=elevation,
        heading=heading,
    )
    return stage_data


class Stage:
    def __init__(self, stage_data=None, s_step=1):
        self.name = stage_data.name
        self.s_step = s_step
        self.distance: np.ndarray = np.arange(
            stage_data.distance[0], stage_data.distance[-1], s_step
        )
        self.elevation: np.ndarray = self._low_pass_filter(
            np.array(stage_data.distance),
            np.array(stage_data.elevation),
            self.distance,
            s_step,
            config=FilterConfigData(gain=1, offset=0, frequency=0.005),
        )
        self.latitude: np.ndarray = self._interpolate(
            stage_data.distance, stage_data.latitude, self.distance
        )
        self.longitude: np.ndarray = self._interpolate(
            stage_data.distance, stage_data.longitude, self.distance
        )
        self.gradient: np.ndarray = self._compute_gradient(
            self.distance, self.elevation
        )
        self.heading: np.ndarray = self._interpolate(
            stage_data.distance, stage_data.heading, self.distance
        )

    @staticmethod
    def _compute_gradient(
        x: Union[List[float], np.ndarray], y: Union[List[float], np.ndarray]
    ) -> np.ndarray:
        return np.gradient(y, x)

    @staticmethod
    def _interpolate(
        x: Union[List[float], np.ndarray],
        y: Union[List[float], np.ndarray],
        xi: Union[List[float], np.ndarray],
        method: str = "cubic",
    ) -> np.ndarray:
        y_interp = interp1d(x, y, kind=method, fill_value="extrapolate")
        return y_interp(xi)

    def _low_pass_filter(
        self,
        x: np.ndarray,
        y: np.ndarray,
        xi: np.ndarray,
        s_step: float,
        config: FilterConfigData,
    ) -> np.ndarray:
        [b, a] = butter(2, 2 * config.frequency * s_step)
        yi = self._interpolate(x, y * config.gain + config.offset, xi)
        y_mod = filtfilt(b, a, yi)
        return y_mod

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name} with distance step of {self.s_step}m>"
