#!/usr/bin/env python3
# %%
import random
import subprocess
import sys

import time

# %%
def simulate_game(deck, first_move, verbose=False):
    jump_size = first_move
    position = 0
    indices = []

    print_deck = deck.copy() + ["X"] * len(deck)

    while position < len(deck):
        if verbose:
            print(f"Taking {jump_size}: ", end="")
            print(print_deck[position : position + jump_size])
        position += jump_size

        if position <= len(deck): # change from < to <= to include last card
            indices.append(position - 1)
            jump_size = deck[position - 1]

    if position == len(deck) and jump_size == 1:
        return False, indices
    else:
        return True, indices


def subsequence_match(sup, sub):
    i = 0
    indices = []
    for j in range(len(sup)):
        if sup[j] == sub[i]:
            indices.append(j)
            i += 1
            if i == len(sub):
                return indices
    return False

def nums_to_str(nums):
    return " ".join(map(str, nums))

def str_to_nums(s):
    return list(map(int, s.split()))


# %%
def run_game(number_range, k, chooser_program=None, arranger_program=None, server_data=None, seed=None):
    if not server_data:
        server_data = dict()

    server_data["v_numbers"] = []
    server_data["vc_numbers"] = []
    server_data["vc_indices"] = []
    server_data["outcome"] = ""
    server_data["win_indices"] = []

    cards = list(range(1, number_range + 1)) + list(range(2, number_range + 1))
    if seed is not None:
        random.seed(seed)
    random.shuffle(cards)
    cards = [1] + cards
    v_numbers, vc_numbers = cards[:k], cards[k:]
    v_numbers.sort()
    vc_numbers.sort()

    server_data["v_numbers"] = v_numbers
    server_data["vc_numbers"] = vc_numbers

    # call chooser
    args = ["choose", nums_to_str(v_numbers), nums_to_str(vc_numbers)]
    if chooser_program is not None:
        start_time = time.time()
        S = subprocess.run([chooser_program] + args, text=True, capture_output=True).stdout
        end_time = time.time()
        if end_time - start_time > 120:
            print("[game.py] Chooser took too long to respond")
            print("Arranger wins by default")
            server_data["outcome"] = "Arranger wins by default (timeout)"
            return -2
    else:
        S = input(args)


    try:
        S = str_to_nums(S)
    except ValueError:
        print("[game.py] Invalid input from chooser: formatting")
        print("Arranger wins by default")
        server_data["outcome"] = "Arranger wins by default (improper formatting)"
        return -2
    if sorted(S) != vc_numbers:
        print(S)
        print("[game.py] Invalid input from chooser: not a permutation of V^C")
        print("Arranger wins by default")
        server_data["outcome"] = "Arranger wins by default (invalid sequence)"
        return -2

    time.sleep(2)
    server_data["vc_numbers"] = S
    
    # call arranger
    args = ["arrange", nums_to_str(v_numbers), nums_to_str(S)]
    if arranger_program is not None:
        start_time = time.time()
        vp = subprocess.run([arranger_program] + args, text=True, capture_output=True).stdout
        end_time = time.time()
        if end_time - start_time > 120:
            print("[game.py] Arranger took too long to respond")
            print("Chooser wins by default")
            server_data["outcome"] = "Chooser wins by default (timeout)"
            return -1
    else:
        vp = input(args)

    try:
        vp = str_to_nums(vp)
    except ValueError:
        print("[game.py] Invalid input from arranger: formatting")
        print("Chooser wins by default")
        server_data["outcome"] = "Chooser wins by default (improper formatting)"
        return -1
    if sorted(vp) != sorted(cards):
        print(vp)
        print("[game.py] Invalid input from arranger: not a permutation of the deck")
        print("Chooser wins by default")
        server_data["outcome"] = "Chooser wins by default (invalid sequence)"
        return -1
    inds = subsequence_match(vp, S) 
    if not inds:
        print(S)
        print(vp)
        print("[game.py] Invalid input from arranger: S is not a subsequence of V'")
        print("Chooser wins by default")
        server_data["outcome"] = "Chooser wins by default (invalid sequence)"
        return -1

    time.sleep(2)
    server_data["v_numbers"] = vp
    server_data["vc_indices"] = inds
    
    time.sleep(2)
    for i in range(1, number_range + 1):
        outcome, indices = simulate_game(vp, i, verbose=False)
        if outcome:
            print(f"Chooser wins with {i}")
            server_data["outcome"] = "Chooser wins with " + str(i)
            server_data["win_indices"] = indices
            simulate_game(vp, i, verbose=True)
            return i
    print("Arranger wins")
    _, indices = simulate_game(vp, 1, verbose=False)
    server_data["outcome"] = "Arranger wins"
    server_data["win_indices"] = indices
    return 0


# %%
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python game.py <k> <chooser_program> <arranger_program>")
        exit(1)
    elif len(sys.argv) > 4:
        seed = sys.argv[4]
    else:
        seed = None

    x = run_game(8, int(sys.argv[1]), sys.argv[2], sys.argv[3], seed=seed)

    if x > 0:
        exit(0)
    else:
        exit(1)
