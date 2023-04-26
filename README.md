# PyBadComments Linter

A Python code linter designed to find banned words/phrases in Python comments and raise a warning.

A list of words can be supplied to the library in its pyproject.toml configuration and it will search
any given files for those words in the comments and raise a warning, pointing to the exact line and
offending word that has caused the warning.f

It can be installed as a pre-commit hook to allow for pre-commit linting.
