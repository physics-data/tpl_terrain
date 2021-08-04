#!/usr/bin/env python3

from PIL import Image
import numpy as np
import json
import gzip

def read():
    print("Reading terrain...")
    terrain_raw = Image.open('./data/terrain.tif')
    terrain_data = np.array(terrain_raw)

    print("Reading terrain metadata...")
    terrain_raw = Image.open('./data/terrain.tif')
    terrain_metadata = json.load(open('./data/terrain.metadata.json'))

    print("Reading wind...")
    wind = json.load(gzip.open('./data/wind.json.gz'))
    print("Reading precipitation...")
    precipitation = json.load(gzip.open('./data/precipitation.json.gz'))

    return {
        "terrain": {
            "metadata": terrain_metadata,
            "data": terrain_data,
        },
        "wind": wind,
        "precipitation": precipitation,
    }


if __name__ == "__main__":
    print(read())
