#!/usr/bin/env python3

import os
import sys

# Functions

def run_and_extract(cmd):
    grade  = 0.0
    status = 'Failure'
    for line in os.popen(cmd):
        if 'Grade' in line:  grade  = line.split()[1]
        if 'Status' in line: status = line.split()[1]
        print(line, end='')
    return float(grade), status == 'Success'

# Main Execution

def main():
    quiz_grade, quiz_status = run_and_extract('make -sk test-quiz')
    prog_grade, prog_status = run_and_extract('make -sk test-program')
    success = (quiz_status and prog_status)

    print('Grade Summary ...')
    print('    Quiz {:4.2f} /  0.50'.format(0.5*quiz_grade))
    print(' Program {:4.2f} /  0.50'.format(0.5*prog_grade))
    print('   Total {:4.2f} /  1.00'.format(0.5*quiz_grade + 0.5*prog_grade))
    print('  Status {}'.format('Success' if success else 'Failure'))

    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
