'''Object Detection script-->Using AEGEAN algorithm (https://github.com/PaulHancock/Aegean)
Input: Cleaned FITS image of whole data set
Output: Data file of the parameters of objects found in image
NOTE: Run in normal python, DO NOT RUN WITHIN CASA, it won't work.
Written by A. Tetarenko'''

# Import modules
# Make sure aegean tree of directories in path so you can import it
import sys
sys.path.append('/home/ubuntu/Aegean')
import aegean

from AegeanTools.catalogs import save_catalog
import numpy as np
from multiprocessing import cpu_count
import re
import os


# set path to where output is to be stored-->need to set up file system so have data and data_products directory
# in this path
path_dir = sys.argv[-1]
# path_dir='/home/ubuntu/'

param_file = sys.argv[-2]


def run_aegean(tables, cellSize):
    '''Open Aegean object file and read in source parameters
    '''

    ra_list = []
    dec_list = []
    maj_list = []
    min_list = []
    pos_list = []
    src_list = []

    with open(tables) as f:
        lines = f.readlines()
    for i in range(1, len(lines)):
        lin_split = lines[i].split('\t')
        src_list.append(lin_split[0])
        ra_list.append(lin_split[4])  # string
        dec_list.append(lin_split[5])  # string
        maj_list.append(float(lin_split[14]) / cellSize)  # pix
        min_list.append(float(lin_split[16]) / cellSize)  # pix
        pos_list.append(float(lin_split[18]))  # deg
    return(src_list, ra_list, dec_list, maj_list, min_list, pos_list)

###########################################################
# USER INPUT SECTION--> read in from parameters file
###########################################################
sys.path.append(os.path.join(path_dir, "AstroCompute_Scripts/"))
from utils import load_json,convert_param_format

data_params = load_json(param_file)
#to convert txt param file to dictionary do this,
#data_params = convert_param_format(param_file, to="dict")

# Target name.
target = data_params["target"]
# Date of observation.
obsDate = data_params["obsDate"]
# Observation frequency.
refFrequency = data_params["refFrequency"]
# Length of time bins (H,M,S)
intervalSizeH = data_params["intervalSizeH"]
intervalSizeM = data_params["intervalSizeM"]
intervalSizeS = data_params["intervalSizeS"]
# Label for casa output directories and files.
label = target + '_' + refFrequency + '_' + obsDate + '_'
outputPath = \
    os.path.join(path_dir, 'data_products/images_' + target + '_' + refFrequency +
                 '_' + str(intervalSizeH) + 'hours' + str(intervalSizeM) + 'min' +
                 str(intervalSizeS) + 'sec/')
fits_file = os.path.join(outputPath, label + 'whole_dataset.fits')
out_file0 = os.path.join(outputPath, label + 'whole_dataset_aegean.txt')
tab_file = os.path.join(outputPath, label + 'whole_dataset_objdet_comp.tab')
catalog_input_name = os.path.join(outputPath, label + 'whole_dataset_objdet.tab')
# aegean parameters
seed = data_params["seed"]
flood = data_params["flood"]
tele = data_params["tele"]
cellSize_string = data_params["cellSize"]
cellSize_list = re.findall('\d+|\D+', cellSize_string)
cellSize = float(cellSize_list[0] + cellSize_list[1] + cellSize_list[2])

###########################################################
# END OF USER INPUT SECTION
###########################################################


# use Aegean object detection algorithm--> import as module
sources = []

# get latitude for telescope
lat = aegean.scope2lat(tele)
# adding SMA and NOEMA to list
if lat == None:
    if tele == 'SMA':
        lat = 19.8243
    elif tele == 'NOEMA':
        lat = 44.6339
    else:
        #lat_string=raw_input('Enter latitude of telescope-->')
        lat = data_params["lat"]

out_file = open(out_file0, 'w')

print 'Running Aegean Object Detection -->'
detections = aegean.find_sources_in_image(fits_file,
                                          outfile=out_file,
                                          hdu_index=0,
                                          rms=None,
                                          max_summits=None,
                                          innerclip=seed,
                                          outerclip=flood,
                                          cores=cpu_count(),
                                          rmsin=None,
                                          bkgin=None, beam=None,
                                          doislandflux=False,
                                          nonegative=not False,
                                          nopositive=False,
                                          mask=None, lat=lat, imgpsf=None)
out_file.flush()
out_file.close()
if len(detections) == 0:
    raise Exception('No sources detected by Aegean. Please check your inputs.')
sources.extend(detections)
# write detected source info to file
if len(sources) > 0:
    save_catalog(catalog_input_name, sources)

# print detected sources fro user to choose from
src_l, ra_l, dec_l, maj_l, min_l, pos_l = run_aegean(tab_file, cellSize)
print 'Number of Objects Detected is ', len(src_l)
print 'Objects Detected-->'
print 'Object, RA, DEC'
for i in range(0, len(src_l)):
    print src_l[i], ra_l[i], dec_l[i]
