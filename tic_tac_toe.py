# how many Tic-Tac-Toe unique games?

board = [[None, None, None], [None, None, None], [None, None, None]]

def represent():
    """Represent board as a 3x3 grid."""
    return ','.join([f'{board[r][c]}' for r in range(3) for c in range(3)])

def has_won(mark):
    """Check if player with mark has won."""
    for r in range(3):
        if board[r][0] == mark and board[r][1] == mark and board[r][2] == mark:
            return True

    for c in range(3):
        if board[0][c] == mark and board[1][c] == mark and board[2][c] == mark:
            return True

    # diagonal
    if board[0][0] == mark and board[1][1] == mark and board[2][2] == mark:
        return True
    if board[2][0] == mark and board[1][1] == mark and board[0][2] == mark:
        return True
    
    return False

def is_full():
    """If all are occupied, then board is full"""
    for r in range(3):
        for c in range(3):
            if board[r][c] == None:
                return False

    return True

def opponent(mark):
    """Return opponent of mark (only call with 'O' or 'X')"""
    return 'O' if mark == 'X' else 'X'

x_wins = []
o_wins = []
draws  = []

def record_win(mark):
    if mark == 'X':
        x_wins.append(represent())
    elif mark == 'O':
        o_wins.append(represent())

def record_draw():
    draws.append(represent())

def play(mark):
    """Play from mark and continue until won or drawn."""
    for r,c in [(r,c) for r in range(3) for c in range(3)]:
        if not board[r][c]:
            board[r][c] = mark
            if has_won(mark):
                record_win(mark)
            elif is_full():
                record_draw()
            else:
                play(opponent(mark))
            board[r][c] = None         # Undo and try next one
                    
def new_play(mark):
    """Play from mark and continue until won or drawn."""
    for r,c in [(r,c) for r in range(3) for c in range(3)]:
        if not board[r][c]:
            board[r][c] = mark
            if has_won(mark):
                record_win(mark)
                board[r][c] = None     # Undo and keep trying
                continue
            elif is_full():
                record_draw()
                board[r][c] = None     # Undo and keep trying
                continue

            play(opponent(mark))
            board[r][c] = None

print(has_won('X'))
print(represent())

play('X')
print('X wins:', len(x_wins))
print('O wins:', len(o_wins))
print('Draws:', len(draws))

print('Total:',len(x_wins) + len(o_wins) + len(draws))

print ("Now, many of these could be duplicates, so need to confirm")
print ("Duplicates occur because same board could result from moves")
print ("made in a different order.")

x_uniq = list(set(x_wins))
o_uniq = list(set(o_wins))
draws_uniq = list(set(draws))

print('X wins:', len(x_uniq))
print('O wins:', len(o_uniq))
print('Draws :', len(draws_uniq))

def output(br, indices):
    b = br.split(',')
    return ','.join([b[idx] for idx in indices])

def symmetries(br):
    """Given a string representation of a board, generate representations of all other symmetries."""
       
    ## SELF is [0,1,2,3,4,5,6,7,8])
    
    # Rotations
    yield output(br, [2,5,8,1,4,7,0,3,6])
    yield output(br, [8,7,6,5,4,3,2,1,0])
    yield output(br, [6,3,0,7,4,1,8,5,2])
    
    # Flip Horizontal
    yield output(br, [2,1,0,5,4,3,8,7,6])
    
    # Flip Vertical
    yield output(br, [6,7,8,3,4,5,0,1,2])
    
    # Flip diagonals(both directions)
    yield output(br, [8,5,2,7,4,1,6,3,0])
    yield output(br, [0,3,6,1,4,7,2,5,8])
    

# eliminating symmetries is a bit more work!
x_wins_ns = set()
for b in x_uniq:
    if len(set(symmetries(b)).intersection(x_wins_ns)) == 0:
        x_wins_ns.add(b)

o_wins_ns = set()
for b in o_uniq:
    if len(set(symmetries(b)).intersection(o_wins_ns)) == 0:
        o_wins_ns.add(b)
        
draws_ns = set()
for b in draws_uniq:
    if len(set(symmetries(b)).intersection(draws_ns)) == 0:
        draws_ns.add(b)
                
print("---")
print('X wins:', len(x_wins_ns))
print('O wins:', len(o_wins_ns))
print('Draws :', len(draws_ns))
print("---")

for b in draws_ns:
    print(b)
