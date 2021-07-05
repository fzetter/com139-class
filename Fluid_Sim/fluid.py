"""
Based on the Jos Stam paper https://www.researchgate.net/publication/2560062_Real-Time_Fluid_Dynamics_for_Games
and the mike ash vulgarization https://mikeash.com/pyblog/fluid-simulation-for-dummies.html

https://github.com/Guilouf/python_realtime_fluidsim
"""
import numpy as np
import math
import json
import random

### CLASS FLUID ###
###################
class Fluid:

    ### INIT ###
    def __init__(self):
        self.rotx = 1
        self.roty = 1
        self.cntx = 1
        self.cnty = -1

        self.size = 60  # Map size
        self.dt = 0.2   # Time interval
        self.iter = 2   # Linear equation solving iteration number

        self.diff = 0.0000  # Diffusion - how fast stuff spreads out in the fluid
        self.visc = 0.0000  # Viscosity - how thick the fluid is

        self.s = np.full((self.size, self.size), 0, dtype=float)        # Previous density
        self.density = np.full((self.size, self.size), 0, dtype=float)  # Current density

        # array of 2d vectors, [x, y]
        self.velo = np.full((self.size, self.size, 2), 0, dtype=float)
        self.velo0 = np.full((self.size, self.size, 2), 0, dtype=float)

    ### STEP ###
    # Main simulation method.
    def step(self):
        # Diffuse the velocity throughout the grid.
        self.diffuse(self.velo0, self.velo, self.visc)

        # Fix up velocities so they keep things incompressible.
        # Input: x0, y0, x, y
        self.project(self.velo0[:, :, 0], self.velo0[:, :, 1], self.velo[:, :, 0], self.velo[:, :, 1])

        # Move the velocities around according to the velocities of the fluid.
        # New velocities affect the ones already in the fluid.
        self.advect(self.velo[:, :, 0], self.velo0[:, :, 0], self.velo0)
        self.advect(self.velo[:, :, 1], self.velo0[:, :, 1], self.velo0)

        # Fix up the velocities again
        self.project(self.velo[:, :, 0], self.velo[:, :, 1], self.velo0[:, :, 0], self.velo0[:, :, 1])

        # Diffuse the dye or the new densities affecting the fluid.
        self.diffuse(self.s, self.density, self.diff)

        # Move the dye around according to the velocities
        self.advect(self.density, self.s, self.velo)

    ### SOLVE EQUATION ###
    # Implementation of the Gauss-Seidel relaxation.
    # Solves a system of linear equations. Since the matrix of this system is sparse (i.e contain a lot of zeros),
    # this system can be solved efficiently using a Gauss-Seidel algorithm.
    # For the diffusion, we try to find the densities which, when diffused backward in time, gives the density we started with.
    # In the case of the projection, we are solving a linear system called a poisson equation.
    #   Poisson's equation is a partial differential equation.
    #   To make sure that the fluid is incompressible, we need to satisfy the non-divergence condition.
    #   The divergence of a vector field represents how much the field is ‘expanding’ at the point.
    #   A positive value represents a divergence and a negative value represents a convergence or compression.
    #   If we assume that a fluid is incompressible, that implies that the divergence of the velocity must be zero everywhere.
    #
    # The solving is done by iterating through the array and setting each cell to a combination of its neighbors.
    # It does this several times; the more iterations it does, the more accurate the results, but the slower things run.
    # After each iteration, it resets the boundaries so the calculations aren't messed up.
    def lin_solve(self, x, x0, a, c):
        c_recip = 1 / c

        for iteration in range(0, self.iter):
            # Calculates the interactions with the 4 closest neighbors
            x[1:-1, 1:-1] = (x0[1:-1, 1:-1] + a * (x[2:, 1:-1] + x[:-2, 1:-1] + x[1:-1, 2:] + x[1:-1, :-2])) * c_recip

            self.set_boundaries(x)

    ### SET BOUNDARIES ###
    # This method keeps the fluid from leaking out of our 3D array.
    # Walls are added by treating the outer layer of cells as the wall.
    # Basically, every velocity in the layer next to this outer layer is mirrored.
    # So when we have some velocity towards the wall in the next-to-outer layer,
    # the wall gets a velocity that perfectly counters it.
    def set_boundaries(self, table):
        if len(table.shape) > 2:  # 3d velocity vector array
            # Simulating the bouncing effect of the velocity array
            # vertical, invert if y vector
            table[:, 0, 1] = - table[:, 0, 1]
            table[:, self.size - 1, 1] = - table[:, self.size - 1, 1]

            # horizontal, invert if x vector
            table[0, :, 0] = - table[0, :, 0]
            table[self.size - 1, :, 0] = - table[self.size - 1, :, 0]

        table[0, 0] = 0.5 * (table[1, 0] + table[0, 1])
        table[0, self.size - 1] = 0.5 * (table[1, self.size - 1] + table[0, self.size - 2])
        table[self.size - 1, 0] = 0.5 * (table[self.size - 2, 0] + table[self.size - 1, 1])
        table[self.size - 1, self.size - 1] = 0.5 * table[self.size - 2, self.size - 1] + \
                                              table[self.size - 1, self.size - 2]

    ### DIFFUSE ###
    # We use diffusion for making the dye and velocities of the fluid spread out throughout the grid.
    def diffuse(self, x, x0, diff):
        if diff != 0:
            a = self.dt * diff * (self.size - 2) * (self.size - 2)
            self.lin_solve(x, x0, a, 1 + 6 * a)
        else:  # equivalent to lin_solve with a = 0
            x[:, :] = x0[:, :]

    ### PROJECT ###
    # We're only simulating incompressible fluids so the amount of fluid in each cell has to stay constant.
    # This method runs through all the cells and fixes them up so everything is in equilibrium.
    def project(self, velo_x, velo_y, p, div):
        # numpy equivalent to this in a for loop:
        # div[i, j] = -0.5 * (velo_x[i + 1, j] - velo_x[i - 1, j] + velo_y[i, j + 1] - velo_y[i, j - 1]) / self.size
        div[1:-1, 1:-1] = -0.5 * (
                velo_x[2:, 1:-1] - velo_x[:-2, 1:-1] +
                velo_y[1:-1, 2:] - velo_y[1:-1, :-2]) / self.size
        p[:, :] = 0

        self.set_boundaries(div)
        self.set_boundaries(p)
        self.lin_solve(p, div, 1, 6)

        velo_x[1:-1, 1:-1] -= 0.5 * (p[2:, 1:-1] - p[:-2, 1:-1]) * self.size
        velo_y[1:-1, 1:-1] -= 0.5 * (p[1:-1, 2:] - p[1:-1, :-2]) * self.size

        self.set_boundaries(self.velo)

    ### ADVECT ###
    # Every cell has a set of velocities, and these velocities make things move.
    # As with diffusion, advection applies both to the dye and to the velocities themselves.
    #
    # It looks at each cell, grabs the velocity and follows it back in time to see where it lands.
    # It then takes a weighted average of the cells around the spot where it lands,
    # then applies that value to the current cell.
    def advect(self, d, d0, velocity):
        dtx = self.dt * (self.size - 2)
        dty = self.dt * (self.size - 2)

        for j in range(1, self.size - 1):
            for i in range(1, self.size - 1):
                tmp1 = dtx * velocity[i, j, 0]
                tmp2 = dty * velocity[i, j, 1]
                x = i - tmp1
                y = j - tmp2

                if x < 0.5:
                    x = 0.5
                if x > (self.size - 1) - 0.5:
                    x = (self.size - 1) - 0.5
                i0 = math.floor(x)
                i1 = i0 + 1.0

                if y < 0.5:
                    y = 0.5
                if y > (self.size - 1) - 0.5:
                    y = (self.size - 1) - 0.5
                j0 = math.floor(y)
                j1 = j0 + 1.0

                s1 = x - i0
                s0 = 1.0 - s1
                t1 = y - j0
                t0 = 1.0 - t1

                i0i = int(i0)
                i1i = int(i1)
                j0i = int(j0)
                j1i = int(j1)

                try:
                    d[i, j] = s0 * (t0 * d0[i0i, j0i] + t1 * d0[i0i, j1i]) + \
                              s1 * (t0 * d0[i1i, j0i] + t1 * d0[i1i, j1i])
                except IndexError:
                    # tmp = str("inline: i0: %d, j0: %d, i1: %d, j1: %d" % (i0, j0, i1, j1))
                    # print("tmp: %s\ntmp1: %s" %(tmp, tmp1))
                    raise IndexError
        self.set_boundaries(d)

    ### TURN ###
    def turn(self):
        self.cntx += 1
        self.cnty += 1
        if self.cntx == 3:
            self.cntx = -1
            self.rotx = 0
        elif self.cntx == 0:
            self.rotx = self.roty * -1
        if self.cnty == 3:
            self.cnty = -1
            self.roty = 0
        elif self.cnty == 0:
            self.roty = self.rotx
        return self.rotx, self.roty

### MAIN ###
############
if __name__ == "__main__":
    try:
        import matplotlib.pyplot as plt
        from matplotlib import animation
        from config import *

        inst = Fluid()
        data = Config().data

        def update_im(i):
            # We add dye so it allows us to see things moving.
            # The water is equally dense everywhere, but some of it has more dye than others.
            # We add new density creators in here.
            # Add density into a 3*3 square.
            for density in data["densities"]:
                val = density["value"]
                x_start = density["pos"]["x"]["start"]
                x_end = density["pos"]["x"]["end"]
                y_start = density["pos"]["y"]["start"]
                y_end = density["pos"]["y"]["end"]

                inst.density[y_start:y_end, x_start:x_end] += val

            # We add velocity vector values in here.
            for force in data["velocities"]:
                start = force["int"][0]
                end = force["int"][1]
                x = eval(force["pos"]["x"])
                y = eval(force["pos"]["y"])
                x_vec = eval(force["dir"]["x"])
                y_vec = eval(force["dir"]["y"])

                if start == -1 and end == -1:
                    inst.velo[x, y] = [x_vec, y_vec]
                else:
                    if i>start and i<end:
                        inst.velo[x, y] = [x_vec, y_vec]

            # Drop velocity when hit an object.
            for object in data["objects"]:
                x = object["pos"]["x"]
                y = object["pos"]["y"]
                len = object["len"]
                inst.velo[y:y+len, x:x+len] = 0

            inst.step()
            im.set_array(inst.density)
            q.set_UVC(inst.velo[:, :, 1], inst.velo[:, :, 0])
            im.autoscale()

        fig = plt.figure()
        colorMap = random.choice(["Accent", "YlOrRd", "tab20", "plasma", "summer"])

        # Plot density
        im = plt.imshow(inst.density, cmap=colorMap, vmax=100, interpolation='bilinear')

        # Plot vector field
        q = plt.quiver(inst.velo[:, :, 1], inst.velo[:, :, 0], scale=10, angles='xy')
        anim = animation.FuncAnimation(fig, update_im, interval=1)
        # anim.save("movie.mp4", fps=30, extra_args=['-vcodec', 'libx264'])
        plt.show()

    except ImportError:
        import imageio

        frames = 30

        flu = Fluid()

        video = np.full((frames, flu.size, flu.size), 0, dtype=float)

        for step in range(0, frames):
            flu.density[4:7, 4:7] += 100 # Add density into a 3*3 square
            flu.velo[5, 5] += [1, 2]

            flu.step()
            video[step] = flu.density

        imageio.mimsave('./video.gif', video.astype('uint8'))
