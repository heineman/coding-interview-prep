import random
from collections import deque

"""
Proides implementations of dfs, dfs_recursive, and bfs to be able to demonstrate their differences. All output is
textual, showing the distance computed from the entrance of the maze.
"""


"""
Represents a rectangular maze whose entrance is in the middle of the top row and whose exit is in the middle
of the bottom row. You can rapidly construct some random graphs by calling 'random(density)' where higher values
of density means more walls and a lower likelihood of finding a path in the maze.
"""
class Maze:
    def __init__(self, num_rows, num_columns):
        self.nr = num_rows
        self.nc = num_columns
        self.M = [None] * num_rows
        for i in range(num_rows):
            self.M[i] = [0] * num_columns
        
    def random(self, density = .2):
        """Create a random NxN maze with entrance at mid-top and exit at mid-bottom."""
            
        # walls outside
        for i in range (self.nr):
            self.M[i][0] = 1
            self.M[i][self.nc-1] = 1
        for i in range (self.nc):
            self.M[0][i] = 1
            self.M[self.nr-1][i] = 1
        
        self.M[0][self.nc//2] = 0
        self.M[self.nr-1][self.nc//2] = 0
        
        for r in range(1, self.nr-1):
            for c in range(1, self.nc-1):
                if random.random() < density:
                    self.M[r][c] = 1

    def isWall(self, sq):
        return self.M[sq.row][sq.column] == 1

    def start(self):
        return Square(0, self.nc//2)
    
    def end(self):
        return Square(self.nr-1, self.nc//2)
    
    def neighbors(self, sq):
        u = sq.up()
        if self.isValid(u): yield u
        
        d = sq.down()
        if self.isValid(d): yield d
        
        l = sq.left()
        if self.isValid(l): yield l
        
        r = sq.right()
        if self.isValid(r): yield r
        
    def isValid(self, sq):
        if sq.row < 0: return False
        if sq.row > self.nr-1: return False
        if sq.column < 0: return False
        if sq.column > self.nc-1: return False
        return True

"""
Represents a square in the maze identified by a (row, column).
Has __eq__() and __hash()__ methods so Square can be a key in a dictionary.
"""
class Square:
    def __init__(self, r, c):
        self.row = r
        self.column = c
        
    def __eq__(self, other):
        return (hasattr(other, 'row') and self.row == other.row) and (hasattr(other, 'column') and self.column == other.column)
    
    def __str__(self):
        return f"{self.row},{self.column}"
    
    def up(self):
        return Square(self.row-1, self.column)
    def down(self):
        return Square(self.row+1, self.column)
    def left(self):
        return Square(self.row, self.column-1)
    def right(self):
        return Square(self.row, self.column+1)
    
    def __hash__(self):
        return hash((self.row, self.column))

def bfs(maze):
    q = deque()
    
    start = maze.start()
    start.prev = None
    end = maze.end()
    
    q.append(start)
    marked = {}
    dist = {}
    marked[start] = True
    dist[start] = 0
    while q:
        s = q.popleft()
        if s == end:
            return (dist, s)
        
        for n in maze.neighbors(s):
            if n not in marked and not maze.isWall(n):
                q.append(n)
                dist[n] = dist[s] + 1
                n.prev = s
                marked[n] = True
        
    return (dist, None)
                
def dfs(maze):
    st = deque()             # Stack of Squares to process
    visited = {}             # Squares already visited
    
    start = maze.start()
    start.prev = None        # set 'previous' square for start to None
    end = maze.end()
    
    st.append(start)         # For every square in the Stack
    visited[start] = True    #   has been visited
    while st:
        s = st.pop()
        if s == end:
            return s
        
        for n in maze.neighbors(s):
            if n not in visited and not maze.isWall(n):
                st.append(n)
                n.prev = s   # Remember: came to n from s
                visited[n] = True
        
    return None                  
                
def dfs_distance(maze):
    st = deque()             # Stack of Squares to process
    visited = {}             # Squares already visited
    dist = {}                # Computed distance to visited square
    
    start = maze.start()
    start.prev = None        # set 'previous' square for start to None
    end = maze.end()
    
    st.append(start)         # For every square in the Stack
    visited[start] = True    #   has been visited
    dist[start] = 0          #   Computed distance is known
    while st:
        s = st.pop()
        if s == end:
            return (dist, s)
        
        for n in maze.neighbors(s):
            if n not in visited and not maze.isWall(n):
                st.append(n)
                dist[n] = dist[s] + 1
                n.prev = s   # Remember: came to n from s
                visited[n] = True
        
    return (dist, None)                
                
def dfs_recursive(maze):
    visited = {}             # Squares already visited
    
    start = maze.start()
    start.prev = None        # set 'previous' square for start to None
    end = maze.end()
    
    visited[start] = True    #   has been visited
    
    def dfs(s):
        if s == end:
            return s
        
        for n in maze.neighbors(s):
            if n not in visited and not maze.isWall(n):
                n.prev = s   # Remember: came to n from s
                visited[n] = True
                solution = dfs(n)
                if solution:
                    return solution
        return None
        
    return dfs(start)           
                
def output(maze):
    """Output maze to screen."""
    for r in range(maze.nr):
        for c in range(maze.nc):
            if maze.isWall(Square(r,c)):
                print('#', end='')
            else:
                print(' ', end='')
        print()
        
def output_distances(maze, distances):
    """Output path to screen."""
    for r in range(maze.nr):
        for c in range(maze.nc):
            sq = Square(r,c)
            if maze.isWall(sq):
                print('#', end=',')
            else:
                if sq in distances:
                    print(distances[sq], end=',')
                else:
                    print(0, end=',')
        print()

def output_path(end):
    """Output path to screen."""
    path = []
    while end:
        path.insert(0, end)
        end = end.prev
        
    for p in path:
        print(f'({p}),', end='')
    print()

def output_solution(maze, end):
    """Output path to screen."""
    path = []
    while end:
        path.append(end)
        end = end.prev
        
    for r in range(maze.nr):
        for c in range(maze.nc):
            sq = Square(r,c)
            if maze.isWall(sq):
                print('#', end=',')
            else:
                if sq in path:
                    print(distances[sq], end=',')
                else:
                    print(0, end=',')
        print()

def load_maze(fname):
    """
    Load up a maze from a file, where first line contains "#rows #columns" and successive lines
    interpret "#" as a wall and anything else as an empty Square.
    """
    with open(fname) as maze_file:
        lines = maze_file.readlines()
        (nr,nc) = [int(d) for d in lines[0].split()]
        maze = Maze(int(nr), int(nc))
        for r in range(1, len(lines)):
            for c in range(nc):
                maze.M[r-1][c] = 1 if lines[r][c] == '#' else 0
    return maze

def path_length(sq):
    """Quickly compute the length of the path from the entrance to the given square based on prev links."""
    ct = 0
    while sq:
        sq = sq.prev
        ct += 1
    return ct
                
if __name__ == '__main__':
    random.seed(32)   # a maze with solution
    N=16
    M = Maze(N, N)
    M.random(33/100)
    
    (distances, end) = bfs(M)
    output_distances(M, distances)
    print()
    output_solution(M, end)
    print()
    
    print('BFS')
    M = load_maze('sample.maze')
    (distances, end) = bfs(M)
    output_distances(M, distances)
    print()
    output_solution(M, end)
    print()
    
    print('DFS')
    M = load_maze('sample.maze')
    (distances, end) = dfs_distance(M)
    output_distances(M, distances)
    print()
    output_solution(M, end)
    print()
    
    print('DFS-RECURSIVE')
    M = load_maze('sample.maze')
    end = dfs_recursive(M)
    output_path(end)

    print ("--- Smaller maze ----")
    print('DFS')
    M = load_maze('eight.maze')
    (distances, end) = dfs_distance(M)
    output_distances(M, distances)
    print()
    output_solution(M, end)
    print()
    
    print('DFS-RECURSIVE')
    M = load_maze('eight.maze')
    end = dfs_recursive(M)
    output_path(end)
    
    print('BFS')
    M = load_maze('eight.maze')
    (distances, end) = bfs(M)
    output_distances(M, distances)
    print()
    output_solution(M, end)
    print()
    
    
    