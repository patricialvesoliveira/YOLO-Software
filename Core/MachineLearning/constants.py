# Constants used in Core and libraries
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

TRAINING_LOCATION = dir_path+'/Files/training_data.txt'
CACHED_LOCATION = dir_path+'/Files/cached_features.txt' 
SHAPE = {'SPIKES':0, 'CURVED': 1, 'LOOPS': 2, 'STRAIGHT':3, 'RECT':4}
SHAPE_ARRAY = ['SPIKES', 'CURVED', 'LOOPS', 'STRAIGHT', 'RECT']