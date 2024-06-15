"""
Animate Depth First Search over a randomly generated maze.

You can also modify the program to store snapshots of the progress in the images/dfs folder
"""
import random
import tkinter
from collections import deque

from maze import Maze, Square
from visualize_search import visualize, make_path, change_color, capture

def dfs(event, maze):
    """Compute DFS and generate images suitable for animated GIF."""
    st = deque()             # Stack of Squares to process
    visited = {}             # Squares already visited
    
    start = Square(0, maze.nc // 2)
    end = Square(maze.nr-1, maze.nc // 2)
    
    st.append(start)         # For every square in the Stack
    visited[start] = make_path(maze, start, 'lightblue')    #   has been visited
    while st:
        s = st.pop()
        change_color(maze, visited[s], 'blue')
        capture(maze.w, 'dfs')
        
        if s == end:
            return s
        
        for n in maze.neighbors(s):
            if not maze.isWall(n):
                if n not in visited:
                    st.append(n)
                    visited[n] = make_path(maze, n, 'lightblue')
                    
    return None


if __name__ == "__main__":
    random.seed(32)   # a maze with solution. Change as you like
    N=16
    M = Maze(N, N)
    M.random(33/100)  # Chooses a random maze
    
    # If you add capture=True, then images will be generated in images/dfs folder
    visualize(M, dfs)
    tkinter.mainloop()
    