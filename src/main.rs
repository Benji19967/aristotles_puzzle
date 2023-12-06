use std::collections::HashSet;

use itertools::{iproduct, Itertools, Tuples};

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

type Row<'a> = &'a Vec<&'a u32>;
type Board<'a> = Vec<Row<'a>>;

fn main() {
    get_valid_board_combinations();
}

fn hashset(data: &[u32]) -> HashSet<u32> {
    HashSet::from_iter(data.iter().cloned())
}

fn get_valid_board_combinations() -> () {
    let rows_of_3 = get_all_rows_summing_to_38(3);
    let rows_of_4 = get_all_rows_summing_to_38(4);
    let rows_of_5 = get_all_rows_summing_to_38(5);
    // println!("{:?}", rows_of_3.len());
    // println!("{:?}", rows_of_4.len());
    // println!("{:?}", rows_of_5.len());

    let mut using: HashSet<u32> = HashSet::new();
    let mut board_combinations: Vec<Vec<&Vec<u32>>> = vec![];
    let mut num_iterations = 0;

    for (row_1, row_5) in rows_of_3.iter().combinations(2).map(|v| (v[0], v[1])) {
        using.extend(row_1);
        if !using.is_disjoint(&hashset(row_5)) {
            for i in row_1.iter() {
                using.remove(i);
            }
            continue;
        }
        using.extend(row_5);
        for (row_2, row_4) in rows_of_4.iter().combinations(2).map(|v| (v[0], v[1])) {
            if !using.is_disjoint(&hashset(&row_2)) {
                continue;
            }
            using.extend(row_2);
            if !using.is_disjoint(&hashset(&row_4)) {
                for i in row_2.iter() {
                    using.remove(i);
                }
                continue;
            }
            using.extend(row_4);
            for row_3 in rows_of_5.iter() {
                if !using.is_disjoint(&hashset(&row_3)) {
                    continue;
                }

                for r1_perm in row_1.iter().permutations(row_1.len()) {
                    for r2_perm in row_2.iter().permutations(row_2.len()) {
                        for r3_perm in row_3.iter().permutations(row_3.len()) {
                            for r4_perm in row_4.iter().permutations(row_4.len()) {
                                for r5_perm in row_5.iter().permutations(row_5.len()) {
                                    let board = build_board(
                                        &r1_perm, &r2_perm, &r3_perm, &r4_perm, &r5_perm,
                                    );
                                    if is_board_valid(board) {
                                        panic!("Found solution");
                                    }

                                    num_iterations += 1;
                                    // println!("{:?}", board);
                                    if num_iterations % 1000000 == 0 {
                                        println!("{}", num_iterations);
                                        return;
                                    }
                                }
                            }
                        }
                    }
                }
            }
            for i in row_2.iter() {
                using.remove(i);
            }
            for i in row_4.iter() {
                using.remove(i);
            }
        }
        for i in row_1.iter() {
            using.remove(i);
        }
        for i in row_5.iter() {
            using.remove(i);
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

fn build_board<'a>(
    r1_perm: Row<'a>,
    r2_perm: Row<'a>,
    r3_perm: Row<'a>,
    r4_perm: Row<'a>,
    r5_perm: Row<'a>,
) -> Board<'a> {
    let mut board: Board = vec![];
    board.push(r1_perm);
    board.push(r2_perm);
    board.push(r3_perm);
    board.push(r4_perm);
    board.push(r5_perm);
    board
}

/// for (r1, r2, r3, r4, r5) in generate_permuations(row_1, row_2, row_3, row_4, row_5) {
///     ...
/// }
///
/// Using this makes the program ~3x slower ...
fn generate_permuations<'a>(
    row_1: &'a Vec<u32>,
    row_2: &'a Vec<u32>,
    row_3: &'a Vec<u32>,
    row_4: &'a Vec<u32>,
    row_5: &'a Vec<u32>,
) -> impl Iterator<
    Item = (
        Vec<&'a u32>,
        Vec<&'a u32>,
        Vec<&'a u32>,
        Vec<&'a u32>,
        Vec<&'a u32>,
    ),
> {
    iproduct!(
        row_1.iter().permutations(row_1.len()),
        row_2.iter().permutations(row_2.len()),
        row_3.iter().permutations(row_3.len()),
        row_4.iter().permutations(row_4.len()),
        row_5.iter().permutations(row_5.len())
    )
}

fn is_board_valid(board: Board) -> bool {
    for line in DIAGONAL_LINE_DOWN_LEFT_INDEXES.iter() {
        let mut sum_of_line = 0;
        for x_y in line.iter() {
            sum_of_line += board[x_y[0]][x_y[1]];
        }
        if sum_of_line != 38 {
            return false;
        }
    }
    for line in DIAGONAL_LINE_DOWN_RIGHT_INDEXES.iter() {
        let mut sum_of_line = 0;
        for x_y in line.iter() {
            sum_of_line += board[x_y[0]][x_y[1]];
        }
        if sum_of_line != 38 {
            return false;
        }
    }
    println!("{:?}", board);
    true
}
