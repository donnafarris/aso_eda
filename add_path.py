"""
code to add path
"""
import sys


def add_dir_to_path(filepath="."):
    """add directory filepath to path if not already there"""

    if filepath not in sys.path:
        sys.path.append(filepath)

# just run it w/o INEM block
# add "this" directory to path
add_dir_to_path(".")