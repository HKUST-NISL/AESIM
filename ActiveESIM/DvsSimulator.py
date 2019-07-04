# Modify from source code: https://github.com/uzh-rpg/rpg_davis_simulator
import math
import numpy as np

class DvsSimulator:

    def __init__(self, initial_time, initial_values, C):
        assert(C > 0)
        self.C = C
        initial_values = self.safe_log(initial_values)
        assert(initial_values.shape[0] > 0)
        assert(initial_values.shape[1] > 0)
        self.height = initial_values.shape[0]
        self.width = initial_values.shape[1]
        self.reference_values = initial_values.copy()
        self.It_array = initial_values.copy()
        self.t = initial_time

    def make_event(self, x, y, ts, pol):
        e=[x, y, int(pol==True), ts]
        return e

    """ Log with a small offset to avoid problems at zero"""
    def safe_log(self,img):
        eps = 0.001
        return np.log(eps + img)

    def update(self, t_dt, img):
        It_dt_array = self.safe_log(img)
        assert(It_dt_array.shape == self.It_array.shape)

        delta_t = t_dt-self.t
        assert(delta_t > 0)

        current_events = []
        for u in range(self.width):
            for v in range(self.height):
                events_for_px = []
                It = self.It_array[v, u]
                It_dt = It_dt_array[v, u]
                previous_crossing = self.reference_values[v, u]

                tol = 1e-6
                if math.fabs(It-It_dt) > tol:

                    polarity = +1 if It_dt >= It else -1

                    list_crossings = []
                    all_crossings_found = False
                    cur_crossing = previous_crossing
                    while not all_crossings_found:
                        cur_crossing += polarity * self.C
                        if polarity > 0:
                            if cur_crossing > It and cur_crossing <= It_dt:
                                list_crossings.append(cur_crossing)
                            else:
                                all_crossings_found = True
                        else:
                            if cur_crossing < It and cur_crossing >= It_dt:
                                list_crossings.append(cur_crossing)
                            else:
                                all_crossings_found = True

                    for crossing in list_crossings:
                        te = self.t + (crossing-It) * delta_t / (It_dt-It)
                        events_for_px.append(self.make_event(u, v, te, polarity > 0))

                    current_events += events_for_px

                    if bool(list_crossings):
                        self.reference_values[v, u] = list_crossings[-1]

        self.It_array = It_dt_array.copy()
        self.t = t_dt

        return current_events