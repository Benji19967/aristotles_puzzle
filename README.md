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

### Recursive approach

- Use pruning to discard whole sets of solutions that are not valid
- Memory usage using Python: ~6MB
- Memory usage using Rust: ~980KB

#### Basic -- no optimizations

- Time using Python: ~11min 15sec
- Time using Rust: ~22s

#### Optimal traversal

- Try slots in an order such that more solutions get pruned
- Time using Python: ~5.5s
- Time using Rust: ~201ms
