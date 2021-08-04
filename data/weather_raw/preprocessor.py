#!/usr/bin/env python3

from scipy.interpolate import griddata, RBFInterpolator, Rbf
import scipy.linalg as linalg
import json
import sys
import math
import numpy as np
import rbf_grid_eval

cnt = 0
def div_free_rbf(coords, data, epsilon = 1):
    coords = np.array(coords)
    def kernel(x1, x2, epsilon = 1):
        delta = x2 - x1
        x = delta[0]
        y = delta[1]
        gaussian = math.exp(- epsilon * (x ** 2 + y ** 2))

        return np.array([
            [
                -(4 * (epsilon ** 2) * (y ** 2) - 2 * epsilon) * gaussian,
                4 * (epsilon ** 2) * gaussian,
            ],
            [
                4 * (epsilon ** 2) * gaussian,
                -(4 * (epsilon ** 2) * (x ** 2) - 2 * epsilon) * gaussian,
            ],
        ])

    # Solve equations
    b = np.array(data).reshape(-1)
    A = np.zeros((len(coords) * 2, len(coords) * 2), dtype="float64")
    for idx, x in enumerate(coords):
        for ridx, rx in enumerate(coords):
            kn = kernel(x, rx, epsilon)
            A[idx * 2:idx * 2 + 2, ridx * 2:ridx * 2 + 2] = kn
    solved = linalg.solve(A, b)
    cs = solved.reshape(2, -1).T

    return cs


RESOLUTION = 0.0002

lon_range = [116, 116.75]
lat_range = [39.65, 40.4]

def parse(fd):
    result = {}
    for line in fd.readlines():
        [station, data] = line.split(' ')
        result[station] = float(data)
    return result

stations = json.load(open("./stations.json"))
print("Reading from " + sys.argv[1])
data = parse(open(sys.argv[1]))

vector_mode = len(sys.argv) > 2
if vector_mode:
    angle = parse(open(sys.argv[2]))
    new_data = {}
    for k, v in data.items():
        theta = angle[k] * math.pi / 180
        vector = [v * math.cos(theta), v * math.sin(theta)]
        new_data[k] = vector
    data = new_data

angle = None

data_point = []
coords = []

for k, v in data.items():
    [lat_deg, lat_min, lon_deg, lon_min] = stations[k]
    coords.append([
        lat_deg + lat_min / 60,
        lon_deg + lon_min / 60,
    ])
    data_point.append(v)

interpolated = None
if not vector_mode:
    grid = np.mgrid[
        lat_range[0]:lat_range[1]:RESOLUTION, 
        lon_range[0]:lon_range[1]:RESOLUTION, 
    ]
    interpolated = griddata(coords, data_point, grid)
    print(interpolated)
else:
    epsilon = 100
    cs = div_free_rbf(coords, data_point, epsilon)
    interpolated = rbf_grid_eval.eval_grid(
        lat_range[0], lat_range[1], RESOLUTION, 
        lon_range[0], lon_range[1], RESOLUTION, 
        np.array(coords), cs, epsilon
    )
    print(interpolated)
    print(np.max(interpolated))
    

# print(interpolated_flat)
# shape = (2, height, width) if vector_mode else (height, width)
# interpolated = interpolated_flat.T.reshape(shape)
# if vector_mode:
#     interpolated = np.transpose(interpolated, (1, 2, 0))
# print(interpolated)

