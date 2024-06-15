"""
Generic code for executing a search algorithm over a randomly generated maze using Tkinter.

Can be configured to store snapshots of progress in images/ subdirectory
"""
import time
import os
import functools
import tkinter
from PIL import ImageGrab 

from maze import Square

# Helpful constants that you can tweak as you like
size = 16
offset = size // 2
delay = .050                  # Speed up or slow down tkinter visualization

# If you set grab_images to True, then the resulting tkinter visualizations are stored frame by frame in 'images' directory.
# Images are numbered based on the image_counter
grab_images = False
image_counter = 0           

## https://stackoverflow.com/questions/70576249/how-do-you-take-a-screenshot-of-a-particular-widget-in-tkinter
def capture(wid, algorithm):
    global image_counter
    """Take screenshot of the passed widget"""
    if grab_images:
        x0 = wid.winfo_rootx()
        y0 = wid.winfo_rooty()
        x1 = x0 + wid.winfo_width()
        y1 = y0 + wid.winfo_height()
    
        im = ImageGrab.grab((x0, y0, x1, y1))
        path = os.path.join('images', algorithm, f'image{image_counter:03d}.png')
        image_counter += 1
        im.save(path)
    else:
        time.sleep(delay)

def visualize(maze, explore, capture=False):
    """Pursue the explore algorithm over the given maze. if capture is true, then images are stored in appropriate subdirectory of images/"""
    global grab_images
    grab_images = capture
    
    master = tkinter.Tk()
    master.title('Left press to start')
        
    # Pass object as an argument to the expore function
    master.bind('<Button-1>', functools.partial(explore, maze=maze))
    
    # Create window and store in maze
    maze.w = tkinter.Canvas(master, width=maze.nc * size + offset, height= maze.nr * size + offset)
    maze.w.pack()
    
    # Make initial maze visualization
    for r in range(maze.nr):
        for c in range(maze.nc):
            sq = Square(r, c)
            if maze.isWall(sq):
                make_wall(maze, sq)
                
def make_wall(maze, sq):
    """Walls are in dark gray."""
    try:
        rect = maze.w.create_rectangle(sq.column*size + offset, sq.row*size + offset, sq.column*size+size + offset, sq.row*size+size + offset, fill='darkgray')
        return rect    
    except tkinter.TclError:
        return None
    
def make_path(maze, sq, color):
    """Drawing the square for a path produces a slightly inset square inside the maze square."""
    try:
        d = 2
        off = size - d
        rect = maze.w.create_rectangle(sq.column*size + offset + d, sq.row*size + offset + d, sq.column*size + offset + off, sq.row*size + offset + off, fill=color)
        return rect
    except tkinter.TclError:
        return None

def change_color(maze, rect, color):
    """Change the color of an existing square."""
    try:
        maze.w.itemconfig(rect, fill=color)
        maze.w.update()
    except tkinter.TclError:
        return
