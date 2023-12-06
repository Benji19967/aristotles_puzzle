use std::collections::HashSet;

use itertools::{Itertools, Tuples};

const DIAGONAL_LINE_DOWN_LEFT_INDEXES: &[&[&[usize]]] = &[
    &[&[0, 0], &[1, 0], &[2, 0]],
    &[&[0, 1], &[1, 1], &[2, 1], &[3, 0]],
    &[&[0, 2], &[1, 2], &[2, 2], &[3, 1], &[4, 0]],
    &[&[1, 3], &[2, 3], &[3, 2], &[4, 1]],
    &[&[2, 4], &[3, 3], &[4, 2]],
];

const DIAGONAL_LINE_DOWN_RIGHT_INDEXES: &[&[&[usize]]] = &[
    &[&[2, 0], &[3, 0], &[4, 0]],
    &[&[1, 0], &[2, 1], &[3, 1], &[4, 1]],
    &[&[0, 0], &[1, 1], &[2, 2], &[3, 2], &[4, 2]],
    &[&[0, 1], &[1, 2], &[2, 3], &[3, 3]],
    &[&[0, 2], &[1, 3], &[2, 4]],
];

fn main() {
    // let rows_5 = get_all_rows_summing_to_38(5);
    // println!("{:?}", rows_5);
    get_valid_board_combinations();
}

type Board = Vec<Vec<u32>>;

fn get_valid_board_combinations() -> () {
    let rows_of_3 = get_all_rows_summing_to_38(3);
    let rows_of_4 = get_all_rows_summing_to_38(4);
    let rows_of_5 = get_all_rows_summing_to_38(5);
    // println!("{:?}", rows_of_3.len());
    // println!("{:?}", rows_of_4.len());
    // println!("{:?}", rows_of_5.len());

    let mut using: HashSet<u32> = HashSet::new();
    let mut board_combinations: Vec<Vec<&Vec<u32>>> = vec![];

    for x in rows_of_3.iter().combinations(2) {
        using.extend(x[0]);
        for y in rows_of_4.iter().combinations(2) {
            for z in rows_of_5.iter() {
                // println!("{:?}", x);
                // println!("{:?}", y);
                // println!("{:?}", z);
                let mut board: Vec<&Vec<u32>> = vec![];
                board.push(x[0]);
                board.push(y[0]);
                board.push(z);
                board.push(y[1]);
                board.push(x[1]);
            }
        }
    }
}

fn get_all_rows_summing_to_38(row_length: usize) -> Vec<Vec<u32>> {
    let mut rows: Vec<Vec<u32>> = vec![];
    for x in (1..=19).combinations(row_length) {
        if x.iter().sum::<u32>() == 38 {
            rows.push(x);
            // println!("{:?}", x);
        }
    }
    rows
}
