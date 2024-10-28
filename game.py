#!/usr/bin/env python3
# %%
import random
import subprocess
import sys

# %%
def simulate_game(deck, first_move, verbose=False):
    jump_size = first_move
    position = 0

    print_deck = deck.copy() + ["X"] * len(deck)

    while position < len(deck):
        if verbose:
            print(f"Taking {jump_size}: ", end="")
            print(print_deck[position : position + jump_size])
        position += jump_size

        if position < len(deck):
            jump_size = deck[position - 1]

    if position == len(deck) and jump_size == 1:
        return True
    else:
        return False


def subsequence_match(sup, sub):
    i = 0
    for j in range(len(sup)):
        if sup[j] == sub[i]:
            i += 1
            if i == len(sub):
                return True
    return False

def nums_to_str(nums):
    return " ".join(map(str, nums))

def str_to_nums(s):
    return list(map(int, s.split()))


# %%
def run_game(number_range, k, chooser_program=None, arranger_program=None):
    cards = list(range(1, number_range + 1)) + list(range(2, number_range + 1))
    random.shuffle(cards)
    cards = [1] + cards
    v_numbers, vc_numbers = cards[:k], cards[k:]
    v_numbers.sort()
    vc_numbers.sort()

    # call chooser
    args = ["choose", nums_to_str(v_numbers), nums_to_str(vc_numbers)]
    if chooser_program is not None:
        S = subprocess.run([chooser_program] + args, text=True, capture_output=True).stdout
    else:
        S = input(args)


    try:
        S = str_to_nums(S)
    except ValueError:
        print("[game.py] Invalid input from chooser: formatting")
        print("Arranger wins by default")
        return -2
    if sorted(S) != vc_numbers:
        print(S)
        print("[game.py] Invalid input from chooser: not a permutation of V^C")
        print("Arranger wins by default")
        return -2
    
    # call arranger
    args = ["arrange", nums_to_str(v_numbers), nums_to_str(S)]
    if arranger_program is not None:
        vp = subprocess.run([arranger_program] + args, text=True, capture_output=True).stdout
    else:
        vp = input(args)

    try:
        vp = str_to_nums(vp)
    except ValueError:
        print("[game.py] Invalid input from arranger: formatting")
        print("Chooser wins by default")
        return -1
    if sorted(vp) != sorted(cards):
        print(vp)
        print("[game.py] Invalid input from arranger: not a permutation of the deck")
        print("Chooser wins by default")
        return -1
    if not subsequence_match(vp, S):
        print(S)
        print(vp)
        print("[game.py] Invalid input from arranger: S is not a subsequence of V'")
        print("Chooser wins by default")
        return -1
    
    for i in range(1, number_range + 1):
        if simulate_game(vp, i, verbose=False):
            print(f"Chooser wins with {i}")
            print(simulate_game(vp, i, verbose=True))
            return i
    print("Arranger wins")
    return 0

# %%
if __name__ == "__main__":
    x = run_game(8, int(sys.argv[1]), sys.argv[2], sys.argv[3])

    if x > 0:
        exit(0)
    else:
        exit(1)