#!/usr/bin/env python3

import json
import os
import sys

import requests
import yaml

# Globals

ASSIGNMENTS    = {}
DREDD_QUIZ_URL = 'https://dredd.h4x0r.space/quiz/cse-30341-fa26/'

# Utilities

def add_assignment(assignment, path=None):
    if path is None:
        path = assignment

    if assignment.startswith('reading') or assignment.startswith('project'):
        ASSIGNMENTS[assignment] = path

def print_results(results):
    for key, value in sorted(results.items()):
        if not key.lower().startswith('q'):
            continue

        try:
            print(f'{key.title():>8} {value:5.2f} / {results['points'][key]:5.2f}')
        except (KeyError, ValueError):
            if key in ('stdout', 'diff'):
                print(f'{key.title():>8}\n{value}')
            else:
                print(f'{key.title():>8} {value})')

    score  = results.get('score', 0)
    total  = results.get('value', 0)
    status = 'Success' if int(results.get('status', 1)) == 0 else 'Failure'
    grade  = score / total if (score > 0 and total > 0) else 0

    print('  ' + '-'*20)
    print(f'{"Score":>8} {score:5.2f} / {total:5.2f}')
    print(f'{"Grade":>8} {grade:5.2f} / {1.0:5.2f}')
    print(f'{"Status":>8} {status}')

# Submit Functions

def submit_quiz(assignment, path):
    answers = None

    for mod_load, ext in ((json.load, 'json'), (yaml.safe_load, 'yaml')):
        try:
            with open(os.path.join(path, 'answers.' + ext)) as stream:
                answers = mod_load(stream)
        except IOError:
            pass
        except Exception as e:
            print(f'Unable to parse answers.{ext}: {e}')
            return 1

    if answers is None:
        print('No quiz found (answers.{json,yaml})')
        return 1

    print(f'Checking {assignment} quiz ...')
    response = requests.post(DREDD_QUIZ_URL + assignment, data=json.dumps(answers), timeout=5)
    print_results(response.json())
    print()

    return int(response.json().get('status', 1))

# Main Execution

def main():
    # Add GitLab/GitHub branch
    for variable in ['CI_BUILD_REF_NAME', 'GITHUB_HEAD_REF']:
        try:
            add_assignment(os.environ[variable])
        except KeyError:
            pass

    # Add local git branch
    try:
        add_assignment(os.popen('git symbolic-ref -q --short HEAD 2> /dev/null').read().strip())
    except OSError:
        pass

    # Add current directory
    add_assignment(os.path.basename(os.path.abspath(os.curdir)), os.curdir)

    # For each assignment, submit quiz answers and program code
    if not ASSIGNMENTS:
        print('Nothing to submit!')
        sys.exit(1)

    exit_code = 0

    for assignment, path in sorted(ASSIGNMENTS.items()):
        if 'reading' in assignment or 'project' in assignment:
            exit_code += submit_quiz(assignment, path)

    sys.exit(exit_code)

if __name__ == '__main__':
    main()

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
