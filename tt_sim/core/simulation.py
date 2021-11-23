import warnings

import numpy as np

from collections import deque


def get_purmutations(riders, duration, t_step):
    time = np.arange(0, duration, t_step)
    index = [i for i in range(len(riders))]
    permutations = []
    que = deque(index)
    lead_elapsed_time = 0
    for t in time:
        permutations.append(list(que))
        if (
            lead_elapsed_time >= riders[que[0]].pull_duration
        ):  # if greater than lead rider pull duration then switch
            que.rotate(-1)
            lead_elapsed_time = 0
        else:
            lead_elapsed_time += t_step
    return time, permutations


class Environment:
    def __init__(self, gravity=9.81, air_density=1.225):
        self.gravity = gravity
        self.air_density = air_density


class Simulation:
    def __init__(self, rider, bike, wind, stage, power):
        self.rider = rider
        self.bike = bike
        self.wind = wind
        self.stage = stage
        self.power = power
        self.max_g_long = 4
        self.max_velocity = 30  # m/s
        self.environment = Environment()
        self.mass = self.rider.mass + self.bike.mass
        self.time = np.zeros(len(self.stage.distance))
        self.velocity = np.zeros(len(self.stage.distance))

    def solve_velocity_and_time(self, v0=1):
        if self.stage.s_step / v0 > 2:
            warnings.warn(
                f"s_step={self.stage.s_step} is much larger than v0={v0}, please check convergence"
            )

        self.velocity[0] = v0
        for step in range(1, len(self.stage.distance)):
            t = self.time[step - 1]
            v = self.velocity[step - 1]
            vw = self.wind.head_wind(self.stage.heading[step])
            r_gradient = self.stage.gradient[step]
            f_drag = 0.5 * self.environment.air_density * self.rider.cda * (v + vw) ** 2
            f_gravity = (
                self.mass * self.environment.gravity * np.sin(np.arctan(r_gradient))
            )
            f_rolling = (
                (self.bike.crr * self.mass)
                * self.environment.gravity
                * np.cos(np.arctan(r_gradient))
            )
            f_tyre = self.power[step] / v
            g_long = min(
                self.max_g_long, (f_tyre - f_drag - f_gravity - f_rolling) / self.mass
            )
            dv = (g_long / v) * self.stage.s_step
            dt = (1 / v) * self.stage.s_step
            self.time[step] = t + dt
            self.velocity[step] = min(v + dv, self.max_velocity)

    def solve_velocity_and_time_ttt(self, v0=1):
        if self.stage.s_step / v0 > 2:
            warnings.warn(
                f"s_step={self.stage.s_step} is much larger than v0={v0}, please check convergence"
            )

        self.velocity[0] = v0
        for step in range(1, len(self.stage.distance)):
            t = self.time[step - 1]
            v = self.velocity[step - 1]
            vw = self.wind.head_wind(self.stage.heading[step])
            r_gradient = self.stage.gradient[step]
            f_drag = (
                0.5
                * self.environment.air_density
                * self.rider.draft_cda
                * (v + vw) ** 2
            )
            f_gravity = (
                self.mass * self.environment.gravity * np.sin(np.arctan(r_gradient))
            )
            f_rolling = (
                (self.bike.crr * self.mass)
                * self.environment.gravity
                * np.cos(np.arctan(r_gradient))
            )
            f_tyre = self.power[step] / v
            g_long = min(
                self.max_g_long, (f_tyre - f_drag - f_gravity - f_rolling) / self.mass
            )
            dv = (g_long / v) * self.stage.s_step
            dt = (1 / v) * self.stage.s_step
            self.time[step] = t + dt
            self.velocity[step] = min(v + dv, self.max_velocity)
