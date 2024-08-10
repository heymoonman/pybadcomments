[![tests](https://github.com/M-Moon/pybadcomments/actions/workflows/python-package.yml/badge.svg?branch=main)](https://github.com/M-Moon/pybadcomments/actions/workflows/python-package.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://black.readthedocs.io/en/stable/_static/license.svg)](https://github.com/M-Moon/pybadcomments/blob/main/LICENSE)

# PyBadComments Linter

A Python code linter designed to find banned words/phrases in Python comments and raise a warning.

A list of words and phrases can be supplied to the library in its pyproject.toml configuration and it will search
any given files for those words in the comments and raise a warning, pointing to the exact line and
offending word that has caused the warning. It uses regex and will match the exact characters in the
strings provided, including any whitespace.

It can be installed as a pre-commit hook to allow for pre-commit linting.

## References
Inspired and aided by [tryceratops](https://github.com/guilatrova/tryceratops)

## Testing
### Samples

Sample files for testing on can be provided in the 'samples' folder. These files act like real Python scripts upon which the linter can be run to test for banned words.

Feel free to add any sample files needed to test unique cases.

### Testing code without a sample file

It is possible to provide Python code as a string and test upon that in test files.

[WIP] Need to ensure the code is setup to allow this.
