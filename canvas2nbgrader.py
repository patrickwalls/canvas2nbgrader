from glob import glob
import os
import shutil
import pandas as pd

assignment = input('Enter assignment name: ')
if not os.path.isdir(os.path.join('submissions',assignment)):
    print('Cannot find folder {}'.format(os.path.join('submissions',assignment)))
    exit()
files = glob(os.path.join('submissions',assignment,'*'))
os.makedirs(os.path.join('submitted'),exist_ok=True)

for file in files:
    filename = os.path.basename(file)
    filename_parts = filename.split('_')
    if filename_parts[1].lower() == 'late':
        canvas_id = filename_parts[2]
    else:
        canvas_id = filename_parts[1]
    destination = os.path.join('submitted',canvas_id,assignment)
    os.makedirs(destination,exist_ok=True)
    for old_file in glob(os.path.join(destination,'*')):
        os.remove(old_file)
    shutil.copyfile(file,os.path.join(destination,assignment + '.ipynb'))
