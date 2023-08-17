# DEM_profiler

## how to run
0. clone this repository
```bash
git clone https://github.com/s-yoshimoto/DEM_profiler.git
cd DEM_profiler
```
1. if you have poetry
```bash
poetry install
```
or if you want to use pip (not tested)
```bash
pip install -r requirementx.txt
```

2. download dataset
```bash
./download.sh
```

3. run profiler_script
```bash
poerty run python profiler.py
or
# if you use pip
python profiler.py
```
then you get following images in output directory
- altitude_image.png : visualized elevation map
- profile_cut_image.png : profiling cut image

## File Description
- profiler.ipynb: for quick code test
- profiler.py: for deploying script code