# canvas2nbgrader

## Python scripts to connect Canvas submissions to nbgrader

1. Download Jupyter notebooks from Canvas.
2. Move notebooks into a folder named `submissions/{assignment_name}`. The assignment name must match the name in nbgrader.
3. Run `python canvas2nbgrader.py`. The result copies submissions to the submitted folder using student Canvas IDs.
4. Run `nbgrader autograde {assignment_name}` to grade notebooks.
5. Run `nbgrader export` to update the `grades.csv` file.
6. Run `python nbgrader2canvas.py` and enter the Canvas ID of the course and assignment (located in the URL of the assignment page). The script requires your Canvas token saved in a file called `token.txt`. The script uploads the grade and autograded notebook to Canvas for each student. The file `upload_log.csv` records which autograded notebooks have been uploaded so that you can run the script again and it will skip over the students whose autograded notebook has not changed.
