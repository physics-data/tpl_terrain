#!/usr/bin/env python3

from scipy.interpolate import griddata
import json
import sys
import math
import numpy as np

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
    [lon_deg, lon_min, lat_deg, lat_min] = stations[k]
    coords.append([
        lat_deg + lat_min / 60,
        lon_deg + lon_min / 60,
    ])
    data_point.append(v)

grid = np.mgrid[
    lat_range[0]:lat_range[1]:RESOLUTION, 
    lon_range[0]:lon_range[1]:RESOLUTION, 
]
flat = grid.reshape(2, -1).T
(_, height, width) = grid.shape = grid.shape

interpolated = None
if not vector_mode:
    interpolator = RBFInterpolator(coords, data_point)
    interpolated = interpolator(flat).reshape((height, width))
else:
    # TODO: finish
    pass

# print(interpolated_flat)
# shape = (2, height, width) if vector_mode else (height, width)
# interpolated = interpolated_flat.T.reshape(shape)
# if vector_mode:
#     interpolated = np.transpose(interpolated, (1, 2, 0))
# print(interpolated)
