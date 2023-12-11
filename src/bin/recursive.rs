use std::process;

const REQUIRED_SUM: usize = 38;
const N: usize = 19;

// Changing the order or traversal brings the time down from ~22s to ~0.2s, roughly a 100x
// improvement
const INDEXES_ORDER: &[usize] = &[
    0, 1, 2, 6, 11, 15, 18, 17, 16, 12, 7, 3, 4, 5, 10, 14, 13, 8, 9,
];

fn main() {
    let mut board: Vec<u32> = vec![0; N];
    let mut used: Vec<u32> = vec![0; N + 1];
    let mut checked: Vec<u32> = vec![0; N + 1];
    place(&mut board, &mut used, &mut checked, 0, true);

    println!("{:?}", checked);
    println!("{:?}", checked.iter().sum::<u32>());
}

fn place(
    board: &mut Vec<u32>,
    used: &mut Vec<u32>,
    checked: &mut Vec<u32>,
    i: usize,
    find_all_solutions: bool,
) -> bool {
    if i == N {
        print_board(board);
        return true && !find_all_solutions;
    }

    let board_idx = INDEXES_ORDER[i];
    for j in 1..=19 {
        if used[j] != 0 {
            continue;
        }

        board[board_idx] = j as u32;
        used[j as usize] = 1;
        if is_valid(board, LINES) && place(board, used, checked, i + 1, find_all_solutions) {
            process::exit(0);
        }

        board[board_idx] = 0;
        used[j as usize] = 0;
        checked[i] += 1;
    }
    false
}

const LINES: &[&[usize]] = &[
    &[2, 1, 0],
    &[7, 3, 0],
    &[11, 6, 2],
    &[16, 12, 7],
    &[18, 15, 11],
    &[18, 17, 16],
    &[6, 5, 4, 3],
    &[12, 8, 4, 1],
    &[15, 10, 5, 1],
    &[17, 13, 8, 3],
    &[17, 14, 10, 6],
    &[15, 14, 13, 12],
    &[11, 10, 9, 8, 7],
    &[18, 14, 9, 4, 0],
    &[16, 13, 9, 5, 2],
];

fn is_valid(b: &Vec<u32>, lines: &[&[usize]]) -> bool {
    for line in lines {
        if !(line.iter().map(|idx| b[*idx]).sum::<u32>() == REQUIRED_SUM as u32
            || line.iter().any(|idx| b[*idx] == 0))
        {
            return false;
        }
    }
    true
}

/// Resources for formatting when printing:
///
/// https://stackoverflow.com/questions/35280798/printing-a-character-a-variable-number-of-times-with-println
/// https://stackoverflow.com/questions/61032075/how-can-i-join-a-vec-of-i32-numbers-into-a-string
///
fn print_board(board: &Vec<u32>) {
    let mut starting_idx: usize = 0;
    for row_len in vec![3, 4, 5, 4, 3] {
        let row = &board[starting_idx..starting_idx + row_len];
        let joined: String = row
            .iter()
            .map(|&id| format!("{:0>2}", id.to_string()) + " ")
            .collect();
        println!("{: ^15}", joined);
        starting_idx += row_len;
    }
    println!("");
}
