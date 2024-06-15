"""
Animate Depth First Search using Recursion rather than a strack over a randomly generated maze.

You can also modify the program to store snapshots of the progress in the images/dfs_recursive folder
"""
import random
import tkinter

from maze import Maze
from visualize_search import visualize, make_path, change_color, capture

def dfs_recursive(event, maze):
    """Compute DFS using recursive implementation and generate images suitable for animated GIF."""
    visited = {}             # Squares already visited
    dist = {}                # Computed distance to visited square
    
    start = maze.start()
    start.prev = None        # set 'previous' square for start to None
    end = maze.end()
    
    visited[start] = make_path(maze, start, 'lightblue')    #   has been visited
    dist[start] = 0          #   Computed distance is known
    
    def dfs(s):
        change_color(maze, visited[s], 'blue')
        capture(maze.w, 'dfs_recursive')
        if s == end:
            return s
        
        for n in maze.neighbors(s):
            if n not in visited and not maze.isWall(n):
                dist[n] = dist[s] + 1
                n.prev = s   # Remember: came to n from s
                visited[n] = make_path(maze, n, 'lightblue')
                if dfs(n):
                    return n
        return None
        
    dfs(start)
    return (dist, None)     

if __name__ == "__main__":
    random.seed(32)   # a maze with solution. Change as you like
    N=16
    M = Maze(N, N)
    M.random(33/100)  # Chooses a random maze
    
    # If you add capture=True, then images will be generated in images/dfs folder
    visualize(M, dfs_recursive)
    tkinter.mainloop()
    