from canvasapi import Canvas
import glob
import tempfile
import os
import pandas as pd

# functions
def get_submission_data(canvas_assignment):
    
    headings = ['user_id', 'graded_at', 'submitted_at']
    stats_overall = []
    # get submission data for each student's assignment
    submissions = canvas_assignment.get_submissions()
    for submission in submissions:

        submission_stats = [int(submission.user_id)]
        try:
            submission_stats.append(submission.graded_at)
        except:
            print("could not retrieve grading time")
        try:
            submission_stats.append(submission.submitted_at)
        except:
            print("could not retrieve submission time")
        stats_overall.append(submission_stats)
    # format as pandas df, ensure datetime cooperation
    grade_status = pd.DataFrame(stats_overall, columns = headings)
    with pd.option_context("future.no_silent_downcasting", True):
        grade_status = grade_status.fillna(pd.to_datetime('2000-01-01 00:00:01+00:00')).infer_objects(copy=False)
    for col in ["graded_at", "submitted_at"]:
        grade_status[col] = pd.to_datetime(grade_status[col])

    return grade_status

# MAIN
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

# get submission times from Canvas
submission_data = get_submission_data(assignment).set_index("user_id")

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

    # skip if graded after submission time
    if submission_data.loc[canvas_id, "graded_at"] > submission_data.loc[canvas_id, "submitted_at"]:
        print("{}'s current attempt has already been graded and uploaded, skipping.".format(canvas_id))
        continue

    print("Uploading grade and feedback for {} ...".format(canvas_id))
    submission.edit(submission={'posted_grade': score})
    f = tempfile.NamedTemporaryFile('w+')
    f.name = '{}_autograded.ipynb'.format(assignment_name)
    with open(source,'r') as fsource:
        f.write(fsource.read())
    f.seek(0)
    submission.upload_comment(f)
    f.close()
