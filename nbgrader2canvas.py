from canvasapi import Canvas
import glob
import tempfile
import os

API_URL = "https://ubc.instructure.com"
with open("token.txt","r") as f:
    API_KEY = f.read()
canvas = Canvas(API_URL, API_KEY)

canvas_course_id = input('Canvas course ID: ')
canvas_course_id = int(canvas_course_id)
canvas_assignment_id = input('Canvas assignment ID: ')
canvas_assignment_id = int(canvas_assignment_id)
assignment_name = input('Assignment name: ')

course = canvas.get_course(canvas_course_id)
assignment = course.get_assignment(canvas_assignment_id)

with open('grades.csv') as f:
    lines = f.readlines()
    lines = [line for line in lines if line.split(',')[0] == assignment_name]

for line in lines:
    items = line.split(',')
    canvas_id = int(items[3])
    try:
        submission = assignment.get_submission(canvas_id)
    except:
        print('Could not find assignment for {}'.format(canvas_id))
        continue
    source = glob.glob(os.path.join("autograded",str(canvas_id),assignment_name,assignment_name + ".ipynb"))
    if len(source) == 0:
        print('Could not find autograded notebook for {}'.format(canvas_id))
        continue
    else:
        source = source[0]
    score = float(items[7])
    print("Uploading grade and feedback for {} ...".format(canvas_id))
    submission.edit(submission={'posted_grade': score})
    f = tempfile.NamedTemporaryFile('w+')
    f.name = '{}_autograded.ipynb'.format(assignment_name)
    with open(source,'r') as fsource:
        f.write(fsource.read())
    f.seek(0)
    submission.upload_comment(f)
    f.close()
