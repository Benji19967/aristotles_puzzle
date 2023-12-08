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

### Brute force

- Try all possible combinations and check whether the board is valid
- Time complexity: `O(n!)`
- `19! ~= 1.2^17` 
- Estimated time on my laptop (MacBook Pro M1) using Rust: # TODO

### Recursive approach

#### Bacis -- no optimizations

- Use pruning to discard whole sets of solutions that are not valid
- Time: # TODO

#### Optimal traversal

- Use pruning to discard whole sets of solutions that are not valid
- Try slots in an order such that more solutions get pruned
- Time: # TODO
