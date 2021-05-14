#!/usr/bin/env python3

import sys
from multiple_divisor import player

test_cases_small = [
    ([], 4, []),
    ([2], 4, [2]),
    ([8], 4, [8]),
    ([5], 4, []),
    ([3], 4, []),
    ([2,3,6], 4, [2]),
    ([1,2,4,5,6,7], 3, [6]),
    ([1,2,3,4,6,7,9,10,11], 5, [10]),
    ([1,2,3,4,6,7,9,11], 5, []),
    ([1,2,3,4,5,6,7,9,11,12,13,14,15,16,17,18,19,20], 10, [2,5,20]),
    ([1,3,4,5,6,7,9,11,12,13,14,15,16,17,18,19,20], 10, []),
    ([1,3,4,5,6,9,11,12,13,14,15,16,17,18,19,20], 7, [14])
]

def range_except(cnt, remove):
    return list(filter(lambda x: not x in remove, range(1,cnt+1)))

test_cases_medium = [
    (range_except(30, [9]), 9, []),
    (range_except(35, [15]), 15, [30]),
    (range_except(40, [7]), 7, [21,35]),
    (range_except(40, [7,21,35]), 7, []),
    (range_except(45, [11]), 11, [22,33]),
    (range_except(45, [11,22,33]), 11, [44]),
    (range_except(45, [11,22,33,44]), 11, []),
    (range_except(50, [3,17]), 3, [39]),
    (range_except(50, [3,17,39]), 3, []),
]

test_cases_large = [
    (range_except(70, [17,23]), 23, [46,69]),
    (range_except(70, [17,23,46,69]), 23, []),
    (range_except(75, [31]), 31, [62]),
    (range_except(75, [31,62]), 31, []),
]

def run_tests(tests):
    for stones,last,winning in tests:
        print(f"A set of stones {stones}, last move {last}, possible winning moves {winning}")
        players_move = player(stones, last)
        if players_move in winning if len(winning) else not players_move:
            print("Correct answer:", players_move)
        else:
            print("Incorrect answer:", players_move)
            return False
    return True

def main():
    tests = {
            "small": test_cases_small,
            "medium": test_cases_medium,
            "large": test_cases_large,
    }
    if len(sys.argv) == 1:
        for name in tests:
            print("Running test", name)
            if run_tests(tests[name]):
                print("Passed.")
    else:
        name = sys.argv[1]
        if name in tests:
            if run_tests(tests[name]):
                print("Tests passed.")
        else:
            print("Unknown test", name)

"""
To run all tests, run the command
$ python3 multiple_divisor_tests.py

To run a test NAME, run the command
$ python3 multiple_divisor_tests.py NAME
"""
if __name__ == "__main__":
    main()