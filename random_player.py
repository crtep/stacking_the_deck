#! /usr/bin/env python3

import sys
import random

def choose(v: list, vc: list) -> list:
    """
    Edit me! The Chooser should return a list of numbers `s` which is a 
    permutation of `vc`.
    """
    random.shuffle(vc)
    s = vc
    return s


def arrange(v: list, s: list) -> list:
    """
    Edit me! The Arranger should return a list of numbers `vp` which is a
    permutation of `v + s` containing `s` as a subsequence.
    """
    random.shuffle(v)
    vp = s + v

    return vp


def nums_to_str(nums):
    return " ".join(map(str, nums))

def str_to_nums(s):
    return list(map(int, s.split()))

if __name__ == "__main__":
    try:
        v, s = sys.argv[2], sys.argv[3]
        v, s = str_to_nums(v), str_to_nums(s)
    except ValueError:
        print(f"[{sys.argv[0]}] Invalid input: formatting")
        sys.exit(1)
    except IndexError:
        print(f"[{sys.argv[0]}] Invalid input: not enough arguments")
        print("Usage: random_chooser.py [choose|arrange] <v> <s>")
        sys.exit(1)
    
    if sys.argv[1] == "choose":
        action = choose(v, s)
    elif sys.argv[1] == "arrange":
        action = arrange(v, s)
    else:
        print(f"[{sys.argv[0]}] Invalid input: first argument must be 'choose' or 'arrange'")
        sys.exit(1)

    print(nums_to_str(action))