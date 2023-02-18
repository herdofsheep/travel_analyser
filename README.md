# travel_analyser
analyser of travel data. 
Follow the instuctions below for setting up and running the travel_analyser- the output
is in the form of a .csv file in the .outputs folder. 
If you would like to try processing other files, make sure the excel file you want to process exists in the `.data` folder and
pass its name to `data_parser.process_data("file_name here")` within the `main()` function in process_tavel_data.py.

### First time running travel_analyser:
Use pipenv to handle dependencies and keep a consistent python environment across machines.
Requires [pip](https://pip.pypa.io/en/stable/installation/) and [python](https://www.python.org/downloads/) to be installed.

`pip install pipenv`
`pipenv install`
`pipenv --python <PYTHON 3 DIRECTORY>`
(use `whereis python3` to find python directory.)
eg. `pipenv --python /usr/bin/python3`

    then...

### New session:

`pipenv shell`
`export PYTHONPATH=$PYTHONPATH:$PWD`
`travel_analyser_service/process_travel_data.py`

### Testing:

`pipenv shell`
`export PYTHONPATH=$PYTHONPATH:$PWD`
`pytest`

## Set up pre-commit hooks:

Before committing to the travel_analyser repo, please run `pre-commit install`.
See [here](https://pre-commit.com/#usage) for more info and help if pre-commit is not installed on your machine.

## What I would like to cover given more time:

[Click here for info about extending and improving the project, given more time](/docs/EXTENSION_AND_FLAWS.md)
