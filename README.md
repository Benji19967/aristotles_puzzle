# Aristotle's Puzzle

## Resources

- https://jtp.io/2017/01/12/aristotle-number-puzzle.html

## Rules

- There are 19 slots arranged in a Hexagonal shape:

```
  # # #
 # # # #
# # # # #
 # # # # 
  # # # 
```

- There are 19 pieces, numbered from 1 through 19
- The goal is to place all the pieces such that the sum of the pieces along each 
horizontal line and along each diagonal line is 38. That makes 15 lines that all need 
to add up to 38.

## Representing the board

- We can represent the board as a simple array of size 19. The indexes of the array 
then represent the following slots on the board.

```
    00  01  02
  03  04  05  06
07  08  09  10  11
  12  13  14  15
    16  17  18
```

## A valid board

A valid board needs to satifsy the following equations:

```
b[0] + b[1] + b[2] = 38
b[3] + b[4] + b[5] + b[6] = 38
...
```

## Solutions

There are 12 solutions, although there is only really 1 unique solutions. The others
are just mirrors or reflections. 

We will let the programs find all 12 solutions, rather than finding 1 and then 
computing the other ones from it. 

### Brute force

- Try all possible combinations and check whether the board is valid
- Time complexity: `O(n!)`
- Number of possible permutations: `19! ~= 1.2^17` 
- Estimated time on my laptop (MacBook Pro M1) using Rust: # TODO
- Estimated amount of storage it would take to store all permutations: 
  - `~1.2^17 permutations * 47 bytes` = `~5.7^18 bytes` = `~5700 Petabytes` = `~5.7 Exabytes`
      - If we store one permutation per line, as a sequence of comma separated numbers, in a `.txt` file,
      each permutation will use `~47 bytes`:
        - `9 bytes` to store digits `0..=9`
        - `20 bytes` to store digits `10..=19`
        - `18 bytes` for commas

### Recursive approach with pruning

Language | Time Basic | Time Optimal | Memory
---------|------------|--------------|-------
Python   | ~11m 15s   |      ~5.5s   |   ~6MB
Rust     |     ~22s   |     ~201ms   | ~980KB

This approach relies on pruning--many permutations of the board will never be checked 
because we know in advance they would not be valid. 

For example, in the following board configuration, the top line does not sum up to 38.
```
    01  02  03
  00  00  00  00
00  00  00  00  00
  00  00  00  00
    00  00  00
```

So we already know that all permutations of the board, which include that top line, are invalid 
and don't need to bec checked. In this case, this means we don't have to fill up the remaining 
16 slots and saves us `16! ~= 2.1^13` checks.

#### Basic (No optimizations)

- Use pruning to discard whole sets of solutions that are not valid
- Order of traversal:
```
    01  02  03
  04  05  06  07
08  09  10  11  12
  13  14  15  16
    17  18  19
```

#### Optimal

- Try slots in an order such that more solutions get pruned
  <!-- - Key observation: lines of length 3 will fail quicker than lines of length 4 which will fail quicker than  -->
  <!-- lines of length 5. -->

TODO: Explain how you calulcate number of valid board configurations.

Filling the board:
- First row (indexes 01, 02, 03):
  - 0 pieces have already been set, 19 are left
  - 5'814: configurations of new pieces (19 * 18 * 17)
  - 5'814: total configurations checked. 0 (previous valid) * 5'814 (new).
  - 180: valid board configurations 30 * 3!
- indexes 04, 05
  - 3 pieces have already been set, 16 are left
  - 240: configurations of new pieces (16 * 15)
  - 43'200: total configurations checked. 180 (previous valid) * 240 (new).
  - 1'760: valid board configurations
- indexes 06, 07
  - 5 pieces have already been set, 14 are left
  - 182: configurations of new pieces (14 * 13)
  - 320'320: total configurations checked. 1'760 (previous valid) * 182 (new).
  - ??? valid board combinations
- ...

- Order of traversal:
```
    01  02  03
  12  13  14  04
11  18  19  15  05
  10  17  16  06
    09  08  07
```

#### First few moves

- Basic

```
    01  00  00
  00  00  00  00
00  00  00  00  00
  00  00  00  00
    00  00  00

    01  02  00
  00  00  00  00
00  00  00  00  00
  00  00  00  00
    00  00  00

    01  02  03
  00  00  00  00
00  00  00  00  00
  00  00  00  00
    00  00  00

    01  02  04
  00  00  00  00
00  00  00  00  00
  00  00  00  00
    00  00  00
...
    01  02  19
  00  00  00  00
00  00  00  00  00
  00  00  00  00
    00  00  00
...
    01  18  19
  00  00  00  00
00  00  00  00  00
  00  00  00  00
    00  00  00

    01  18  19
  02  00  00  00
00  00  00  00  00
  00  00  00  00
    00  00  00

    01  18  19
  02  03  00  00
00  00  00  00  00
  00  00  00  00
    00  00  00

    01  18  19
  02  03  04  00
00  00  00  00  00
  00  00  00  00
    00  00  00

    01  18  19
  02  03  04  05
00  00  00  00  00
  00  00  00  00
    00  00  00

    01  18  19
  02  03  04  06
00  00  00  00  00
  00  00  00  00
    00  00  00

...
```

- Optimized

```
    01  00  00
  00  00  00  00
00  00  00  00  00
  00  00  00  00
    00  00  00

    01  02  00
  00  00  00  00
00  00  00  00  00
  00  00  00  00
    00  00  00

    01  02  03
  00  00  00  00
00  00  00  00  00
  00  00  00  00
    00  00  00

    01  02  04
  00  00  00  00
00  00  00  00  00
  00  00  00  00
    00  00  00
...
    01  02  19
  00  00  00  00
00  00  00  00  00
  00  00  00  00
    00  00  00
...
    01  18  19
  00  00  00  00
00  00  00  00  00
  00  00  00  00
    00  00  00

    01  18  19
  00  00  00  02
00  00  00  00  00
  00  00  00  00
    00  00  00

    01  18  19
  00  00  00  02
00  00  00  00  03
  00  00  00  00
    00  00  00

    01  18  19
  00  00  00  02
00  00  00  00  04
  00  00  00  00
    00  00  00
...
```

