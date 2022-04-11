# MPM Assessment 2

**Deadline: 4pm BST Friday 22nd October 2021**

## Task description

In this exercise you will use **Pandas, Flask and Docker **to create a tool to process tide gauge data in `.csv` format into a cloud compatible form.

The `tideReadings.csv` file contains sea level readings (in m) recorded over 15 minute windows at tide gauges around the UK for the week of Monday 20th September 2021. The columns are:

- `dateTime`: The date and time for which the reading is valid.
- `stationName`: The human readable tide gauge name.
- `tideValue`: the tide gauge reading in metres (relative to mean sea level at Newlyn).

The `stations.csv` file contains some relevant information on the tide gauge stations. The columns are:

- `stationName`: The human readable tide gauge name.
- `stationReference` The Environment Agency short code for the station
- `stationURL` the Environment Agency REST API URL for the station, which can be called to access more information if needed.

### Workflow

You are strongly recommended to work using a code editor such as VS Code, rather than trying to work in Jupyter notebooks and copying material back and forth. The entire repository should be uploaded to GitHub before the submission deadline. For this we recommend using either:
1. A `git` based GUI such as GitHub Desktop
2. The source control tab in VS Code
3. The `git` tool on the command line. If no additional files have been created, then this can be achieved by running:
  ```
  git add -u
  git commit
  git push -u origin main
  ```
  If you have created additional files to be submitted (e.g. additional code tests) then these should be staged using commands such as `git add test_process.py` before committing. 

### Problem Specification

You must:

1. [45 marks] Write appropriate Python code to complete the methods of class `Reader` in `process.py`. See the docstrings in each method for details of key functionality required, although other methods or functions can be added if appropriate. This 
2. [45 marks] Write Python code in `app.py` to serve a REST API for the data in the two `.csv` files. See the `API.rst` file for a description of required paths and responses. You may either use Flask, or builtin Python modules, and may add additional classes or functions as needed, to the `process.py` and `app.py` files, or to new Python files.
3. [10 marks] Update the `Dockerfile` to correctly serve your `app.py` on the container's port 80, so that the command sequence
```bash
  docker build --tag tides:latest
  docker run -it -p8888:80 tides:latest
```
  allows a user to connect to `http://localhost:8888/station/json?stationName=Newlyn` and see a response listing the tide data for the Newlyn station.

### Mark scheme

Marks will be awarded for each part of the assesment completed, independent of the other parts of the assessment. The primary source of marks will be functionality provided in line with the `process.py` docstrings and `API.rst` description, with robustness (both to user error & data errors) and maintainability (with features such as code tests and clarity of code) also key considerations. Although all Python code should be PEP8 compliant, marks will not be lost for time or memory inefficiency, unless particularly egregious.



## Supplement

**Since “from” is a python keyword, all “from” and “to” in this project are replaced with “t_from” and “t_to”**



