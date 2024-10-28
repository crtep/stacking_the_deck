# Stacking the Deck

Write a program to play *Stacking the Deck*.


When you are the **chooser**, your program will called as follows:
```
./team_name.py choose <v> <vc>
```
where `<v>` are the cards in $V$ and `<vc>` are the remaining cards ($V^C$, 
i.e., the complement of $V$). Your program should return a permutation
of $V^C$.


When you are the **arranger**, your program will be called as follows:
```
./team_name.py arrange <v> <s>
```
where `<v>` are the cards in $V$ and `<s>` are the cards in $S$. Your program
should return a permutation of $V \sqcup S$ which has $S$ as an ordered
subsequence.


Your program will receive lists of cards as numbers separated by spaces, and
should print its output in to `stdout` in the same format.


If you want to write your program in Python, you can do so by modifying
`random_player.py`. Otherwise, please make reasonable efforts to ensure that
your program can be compiled and run on an Intel Mac. (Send it in early if 
you're in doubt.) Please submit your by 4 p.m. on Thursday, Nov. 7 to
```python
[f"{username}@nyu.edu" for username in ["carterteplica", "xl5279"]]
```


Happy hacking!

Carter and Rubben