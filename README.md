# canvas2nbgrader

## Python scripts to connect Canvas submissions to nbgrader

1. Download Jupyter notebooks from Canvas.
2. Move notebooks into a folder named `submissions/{assignment_name}`. The assignment name must match the name in nbgrader.
3. Run `python canvas2nbgrader.py`. The result copies submissions to the submitted folder using student Canvas IDs.
4. Run `nbgrader autograde {assignment_name}` to grade notebooks.
5. Run `nbgrader export` to update the `grades.csv` file.
6. Export and save Canvas gradebook as `grades/upload.csv`.
6. Run `python nbgrader2canvas.py`. The result produces the grades file for the assignment to upload to Canvas and a subfolder in the `returned` folder containing the graded notebooks (with the original Canvas filenames) to then zip and upload to Canvas.
