# travel_analyser
analyser of travel data

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
`python3 travel_analyser/process_travel_data.py`

### Testing:

`pipenv shell`
`export PYTHONPATH=$PYTHONPATH:$PWD`
`pytest`

## Set up pre-commit hooks:

Before committing to the travel_analyser repo, please run `pre-commit install`.
See [here](https://pre-commit.com/#usage) for more info and help if pre-commit is not installed on your machine.

