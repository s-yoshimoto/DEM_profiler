#import libraries
import rasterio
import numpy as np
import matplotlib.pyplot as plt
import math
import argparse
import os
import shutil

def main(file_name, step, x1, y1, x2, y2):
    output_dir = "output"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    # Process 2,3
    with rasterio.open(file_name) as src:
        band = src.read(1)
        # change to numpy
        band_np = np.array(band)
        # clip seelevel value -32768 -> 0
        band_np[band_np == -32768] = 0 
        # plot with colormap
        plt.figure()
        plt.imshow(band_np, cmap='jet')
        plt.colorbar()
        plt.savefig(f"{output_dir}/altitude_image.png")

        # interpolate_func = get_value_with_floor_clip
        interpolate_func = get_value_with_bilinear_interpolation

        #start_point=np.array([3600, 1200])
        #end_point=np.array([1200, 4800])
        start_point=np.array([y1, x1])
        end_point=np.array([y2, x2])

        xsteps = np.linspace(start_point[1], end_point[1], step)
        ysteps = np.linspace(start_point[0], end_point[0], step)

        # get profiling data
        profile = []
        for x, y in zip(xsteps, ysteps):
            elevation = interpolate_func(band_np, x, y)
            profile.append(elevation)
        
        # plot image
        plt1 = plt.figure(figsize=(20,5))
        plt1.tight_layout()
        ax = plt1.subplots(1, 2, gridspec_kw={'width_ratios': [1, 3]})
        ax[0].imshow(band_np, cmap='jet')
        ax[0].plot([start_point[1], end_point[1]], [start_point[0], end_point[0]], color="black", marker="o", label="profile cut")
        ax[1].plot(profile, label="profile cut")
        ax[1].grid(axis='x')
        ax[1].grid(axis='y')
        ax[1].set_ylabel("altitude(m)")
        ax[1].legend()
        plt1.savefig(f"{output_dir}/profile_cut_image.png")

        

# interpolation functions
# simple function for debug
def get_value_with_floor_clip(data: np.array, x: float, y: float) -> float:
    return data[math.floor(y), math.floor(x)]

def get_value_with_bilinear_interpolation(data: np.array, x: float, y: float) -> float:
    x_0 = math.floor(x) 
    y_0 = math.floor(y)
    x_1 = x_0 + 1
    y_1 = y_0 + 1
    # clip border
    x_1 = min(data.shape[1]-1, x_1)
    y_1 = min(data.shape[0]-1, y_1)
    m = x - x_0
    n = y - y_0
    # x interpolation (x_1 - j_0 = 1)
    x_int_y0 = m * data[y_0, x_0] + (1-m) * data[y_0, x_1]
    x_int_y1 = m * data[y_1, x_0] + (1-m) * data[y_1, y_1]
    # y interpolation
    return n * x_int_y0 + (1-n) * x_int_y1

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Profiling geo image')
    parser.add_argument("--tif", default="srtm_65_04.tif", help="tif file name")
    parser.add_argument("--step", type=int, default=100, help="profiler resolution step")
    parser.add_argument("--x1", type=int, default=1200, help="profiling start position x")
    parser.add_argument("--y1", type=int, default=3600, help="profiling start position x")
    parser.add_argument("--x2", type=int, default=4800, help="profiling end position x")
    parser.add_argument("--y2", type=int, default=1200, help="profiling end position x")
    args = parser.parse_args()
    main(args.tif, args.step, args.x1, args.y1, args.x2, args.y2)
