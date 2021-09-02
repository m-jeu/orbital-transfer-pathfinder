from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
import matplotlib  # For typing

import orbital_transfer_pathfinder.lib.orbitalmechanics.orbits as orbits


def orbit_names(n: int) -> list[str]:
    """Create some appropriate names to label orbits with during visualization.

    The origin orbit will be called 'Start orbit', then any amount of numbered 'Intermediate' orbits {num},
    ending with an orbit called 'Target orbit'.

    Args:
        n: amount of names to create, should be 2 at least..

    Returns:
        n amount of names ordered.

    Raises:
        RunTimeError if n < 2 because there should be at least a start and a target, logically."""
    if n < 2:
        raise RuntimeError("orbit_names being passed with n < 2 shouldn't happen.")
    return ["Start orbit"] + [f"Intermediate orbit {x}" for x in range(1, n - 1)] + ["Target orbit"]


def remove_ticktabels(ax: matplotlib.axes._subplots.Axes3DSubplot):
    """Remove the ticklabels from a 3D matplotlib graph.

    Args:
        ax: the graph to remove ticklabels from."""
    ax.xaxis.set_ticklabels([])
    ax.yaxis.set_ticklabels([])
    ax.zaxis.set_ticklabels([])


def orbit_to_3d_coordinates(orbit: orbits.Orbit, n: int = 200) -> np.ndarray:
    """Turn an orbitalmechanics.orbits Orbit into n-equally spaced xyz coordinates along it's path.
    Formatted as a numpy array that contains 3 arrays, for X Y and Z coordinates. Each array is n elements long.

    Args:
        orbit: orbit to compute coordinates for.
        n: amount of points to compute coordinates at.

    Returns:
        numpy array that contains 3 arrays for X, Y and Z coordinates, each n elements long."""
    pa_orbit = orbit.to_PyAstronomy_orbit()  # PyAstronomy does most of the heavy lifting for visualization
    t = np.linspace(0, int(orbit.period), n)
    coords_per_dimension = np.matrix.transpose(pa_orbit.xyzPos(t))  # PyAstronomy.KeplerEllipse.xyzPos()
    coords_per_dimension[[0, 1]] = coords_per_dimension[[1, 0]]  # Returns coordinates in YXZ format ???
    return coords_per_dimension


def visualize_orbits(orbits: list[orbits.Orbit]):
    """Visualize any number of orbits around one body in one matplotlib 3d figure.

    Args:
        orbits: orbits to visualize."""
    ax = plt.axes(projection="3d")
    ax.set_title("Computed Path")
    ax.scatter3D(0, 0, edgecolor="k", facecolor="k", alpha=0.5)  # Place a dot to represent midpoint, not to scale
    labels = orbit_names(len(orbits))
    for num, orbit in enumerate(orbits):
        xyz_coords = orbit_to_3d_coordinates(orbit)
        ax.plot3D(xyz_coords[0], xyz_coords[1], xyz_coords[2], label=labels[num])
    ax.legend()
    remove_ticktabels(ax)
    plt.show()
