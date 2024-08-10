# complaint.py

complaint_set_words = {"hate", "awful", "unreasonable"}


def in_line_complaint():
    x = 3 + 1  # hate this, awful use of hardcoded numbers and completely unreasonable
    return x


def docstring_complaint():
    """hate this, awful use of hardcoded numbers and completely unreasonable"""
    x = 3 + 1
    return x


def docstring_complaint_on_new_line():
    """
    hate this, awful use of hardcoded numbers and completely unreasonable"""
    x = 3 + 1
    return x
