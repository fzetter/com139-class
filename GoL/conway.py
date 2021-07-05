"""
conway.py
A simple Python/matplotlib implementation of Conway's Game of Life.
"""

import sys, argparse
import json
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

CROP = 10
ON = 255
OFF = 0
vals = [ON, OFF]

### CLASS POINT ###
class Point:
    def __init__(self, i, j):
        self.i = i
        self.j = j

    def __str__(self):
        return "Point({0},{1})".format(self.i, self.j)

### RANDOM GRID ###
# Returns a grid of NxN random values
def randomGrid(N):
    return np.random.choice(vals, N*N, p=[0.2, 0.8]).reshape(N, N)

### ADD GLIDER ###
# Adds a glider with top left cell at (i, j)
def addGlider(i, j, grid, pattern):
    glider = np.array(pattern)
    w = len(glider)
    h = len(glider[0])
    grid[i:i+w, j:j+h] = glider

### COUNT NEIGHBOURS ###
# Count number of live adjacent cells
def countNeighbours(grid, point):
    count = 0
    for i in range(point.i-1, point.i+2):
        for j in range(point.j-1, point.j+2):
            try:
                if grid[i][j] == 255: count += 1
            except IndexError: continue

    if grid[point.i][point.j] == 255: count -= 1
    return count

### SET RULES ###
# Conway's Game of Life rules
def setRules(grid, newGrid):
    for i in range (len(grid)): # ROWS
        for j in range (len(grid[i])):  # COLUMNS

            count = countNeighbours(grid, Point(i, j))

            # Rule 1.
            # Any live cell with two or three neighbors survives.
            if grid[i][j] == 255 and (count == 2 or count == 3): continue

            # Rule 2.
            # Any dead cell with three live neighbors becomes a live cell.
            elif grid[i][j] == 0 and count == 3: newGrid[i][j] = 255

            # Rule 3.
            # All other live cells die in the next generation.
            # Similarly, all other dead cells stay dead.
            else: newGrid[i][j] = 0

    return newGrid

### UPDATE ###
# Update grid
def update(frameNum, img, grid, N):
    # Copy grid since we require 8 neighbours for calculation
    # and we go line by line
    newGrid = grid.copy()

    # Implement the rules of Conway's Game of Life
    newGrid = setRules(grid, newGrid)

    # Update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,

### MAIN ###
def main():

    # Configuration file
    with open('configuration.json') as file:
        data = json.load(file)

    # Grid size & animation update interval
    N = data["universeSize"]
    updateInterval = data["updateInterval"]
    pattern = data["initialSetup"]["4"]
    colorMap = random.choice(["Accent", "YlOrRd", "magma", "tab20", "plasma", "summer"])

    # Start grid
    if data["generateRandom"]:
        grid = np.array([])
        grid = randomGrid(N)
    else:
        grid = np.zeros(N*N).reshape(N, N)
        addGlider(10, 10, grid, pattern)

    # Animation
    fig, ax = plt.subplots()
    fig.set_facecolor("white")
    img = ax.imshow(grid, interpolation='nearest', cmap = colorMap)
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ),
                                  frames = 10, interval = updateInterval, save_count = 50)

    plt.show()

# call main
if __name__ == '__main__':
    main()
