from canvasapi import Canvas
import glob
import tempfile
import os
import hashlib
import json
import pandas as pd

# globals
API_URL = "https://ubc.instructure.com"
UPLOAD_LOG = "upload_log.csv"
UPLOAD_LOG_COLUMN_NAMES = ["canvas_id", "assignment_name", "file_upload_hash"]

# functions
def open_upload_log():
    try:
        upload_history = pd.read_csv(UPLOAD_LOG)
    except FileNotFoundError:
        upload_history = pd.DataFrame(columns=UPLOAD_LOG_COLUMN_NAMES)
    return upload_history.set_index(UPLOAD_LOG_COLUMN_NAMES[0:2])

def parse_notebook_as_dict(path):
    file = open(path)
    json_dict = json.load(file)
    file.close()
    for index, cell_dict in enumerate(json_dict["cells"]):
        # cell outputs aren't necessary for the hash comparison and could slow things down
        if "outputs" in cell_dict.keys():
            cell_dict.pop("outputs")
        # execution times must be removed for the comparison
        if "execution" in cell_dict["metadata"].keys():
            json_dict["cells"][index]["metadata"].pop("execution")

    return json_dict

def sha256(string):
    return hashlib.sha256(string.encode("utf-8")).hexdigest()

# Main
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

upload_history = open_upload_log()

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

    try:
        previous_upload_hash = upload_history.loc[(canvas_id, assignment_name), UPLOAD_LOG_COLUMN_NAMES[2]]
    except KeyError:
        previous_upload_hash = 0

    source_dict = parse_notebook_as_dict(source)
    source_hash = sha256(str(source_dict))

    if (source_hash == previous_upload_hash):
        print("{}'s autograded notebook is the same as the previously uploaded notebook, skipping.".format(canvas_id))
        continue
    upload_history.loc[(canvas_id, assignment_name), UPLOAD_LOG_COLUMN_NAMES[2]] = source_hash
    
    print("Uploading grade and feedback for {} ...".format(canvas_id))
    submission.edit(submission={'posted_grade': score})
    f = tempfile.NamedTemporaryFile('w+')
    f.name = '{}_autograded.ipynb'.format(assignment_name)
    with open(source,'r') as fsource:
        f.write(fsource.read())
    f.seek(0)
    submission.upload_comment(f)
    f.close()

    # update UPLOAD_LOG after every submission
    upload_history.to_csv(UPLOAD_LOG)
