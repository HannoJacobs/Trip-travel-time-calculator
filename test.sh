#!/bin/sh

set -e

# run all tests standard way
pytest tests/ -v

# showing output:
# pytest tests/ -v -rP

# only one test:
# pytest tests/ -v -rP -k test_fp
