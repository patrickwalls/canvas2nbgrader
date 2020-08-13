from glob import glob
import os
import shutil
import pandas as pd

assignment = input('Enter assignment name: ')
if not os.path.isdir(os.path.join('submissions',assignment)):
    print('Cannot find folder {}'.format(os.path.join('submissions',assignment)))
    exit()
os.makedirs(os.path.join('returned',assignment),exist_ok=True)
for old_file in glob(os.path.join('returned',assignment,'*')):
    os.remove(old_file)

for student in glob(os.path.join('autograded','*')):
    canvas_id = os.path.basename(student)
    file = glob(os.path.join('submissions',assignment,'*_{}_*'.format(canvas_id)))
    if file:
        students_submitted.append(canvas_id)
        source = os.path.join('autograded',canvas_id,assignment,assignment + '.ipynb')
        destination = os.path.join('returned',assignment,os.path.basename(file[0]))
        shutil.copyfile(source,destination)

grades = pd.read_csv('grades.csv')
grades = grades[grades['assignment'] == assignment]
grades = grades[['assignment','student_id','raw_score']]
grades.columns = ['assignment','canvas_id','total']

os.makedirs(os.path.join('grades'),exist_ok=True)
grades.to_csv(os.path.join('grades',assignment + '.csv'),index=False)
