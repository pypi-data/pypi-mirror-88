# Useful plotting routines

import numpy as np

def plot_grid(m, ax, proj, step = 10, **kwargs):
    """
    Plot the pixel boundaries of a Healpix grid
    
    Args:
        m (HealpixBase): Map defining the grid
        ax (matplotlib.axes.Axes): Axes on where to plot
        proj (healpy.projector.SphericalProj): Projector to converto 
            spherical coordinates to plot's axes coodinates
        step (int): How many points per pixel side
        **kwargs: Passed to matplotlib.pyplot.plot()
    """
    
    # Keep track of limits
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    
    # Every line should have the same color
    if 'c' in kwargs:
        color = kwargs.pop('c')
    else:
        color = kwargs.pop('color', 'white')
    
    # Plot every pixel
    for pix in range(m.npix):

        # Get boundaries
        vec = m.boundaries(pix, step = step)
        
        # Close loop
        vec = np.append(vec, vec[:,0].reshape(-1,1), axis = 1)
 
        # Project
        x,y = proj.vec2xy(vec)

        # Remove discontinuities
        dx = np.abs(np.diff(x))
        dy = np.abs(np.diff(y))
        jumps = np.logical_or(dx > 2*np.mean(dx), 
                              dy > 2*np.mean(dy))
        jumps = np.append(jumps, False)

        if any(jumps):
            
            ijumps = np.nonzero(jumps)[0]+1
            
            x = np.insert(x, ijumps, np.nan)
            y = np.insert(y, ijumps, np.nan)
            
        # Plot
        ax.plot(x,y, color = color, **kwargs)

    # Set axes back to the original limits
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
