#!/usr/bin/env python3

"""
Load test data from dist into Python data structures.
"""

import argparse
import os
import sys
import typing

import edq.util.json

THIS_DIR: str = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
DATA_DIR: str = os.path.join(THIS_DIR, 'testdata')

ASSIGNMENTS_FILE: str = 'assignments.json'
COURSES_FILE: str = 'courses.json'
GROUPSETS_FILE: str = 'groupsets.json'
SUBMISSIONS_FILE: str = 'submissions.json'
USERS_FILE: str = 'users.json'

DATA_FILES: typing.List[str] = [
    USERS_FILE,
    COURSES_FILE,
    ASSIGNMENTS_FILE,
    GROUPSETS_FILE,
    SUBMISSIONS_FILE,
]

def load_test_data(data_dir = DATA_DIR) -> typing.Tuple[typing.Dict[str, typing.Dict[str, typing.Any]], ...]:
    """
    Load data from a base dir.
    All collections will be converted to a dict, keyed by the item's short name (`short-name`).
    The same short name is used to cross-reference items in this dataset.
    Returns (matches order of DATA_FILES): users, courses, assignments, groups, submissions.
    """

    results = []

    for filename in DATA_FILES:
        path = os.path.join(data_dir, filename)
        items = edq.util.json.load_path(path)

        mapped_items = {}
        for item in items:
            key = item['short-name']
            if (key in mapped_items):
                raise ValueError(f"Found duplicate key ('{key}') in data file: '{path}'.")

            mapped_items[key] = item

        results.append(mapped_items)

    return tuple(results)

def main():
    args = _get_parser().parse_args()

    dataset = load_test_data(data_dir = args.data_dir)
    for (i, filename) in enumerate(DATA_FILES):
        print(f"{filename}: {len(dataset[i])} items.")

    return 0

def _get_parser():
    parser = argparse.ArgumentParser(description = __doc__.strip())

    parser.add_argument('--data-dir', dest = 'data_dir',
        action = 'store', type = str, default = DATA_DIR,
        help = 'The directory with test data to load (default: %(default)s).')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
