setup:
	pip install -r requirements.txt

run:
	PYTHONPATH=./src python -m kw_checker

## Cleaning up the python compiled bytecodes
clear-pyc:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf