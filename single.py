"""
Sample Game between players 'X' and 'O' on a board that only has a single row of three squares.

This generates all possible board states
"""
board = [None, None, None]

def is_full():
    """Board is full if a mark in each location."""
    return board[0] and board[1] and board[2]

def play(mark):
    """Play from mark and continue until won or drawn."""
    for r in range(3):
        if not board[r]:
            board[r] = mark           # Place mark
            if is_full():
                print(','.join(board))
            else:
                play(opponent(mark))  # Recursively play opponent
            board[r] = None           # Undo and try next one

def opponent(mark):
    """Return opponent for given mark."""
    return 'O' if mark == 'X' else 'X' 

if __name__ == "__main__":
    play('X')