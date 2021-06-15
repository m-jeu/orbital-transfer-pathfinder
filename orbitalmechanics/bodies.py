# To prevent circle import (for typehints) problems
from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import orbitalmechanics.orbits as orbits


GRAVITATIONAL_CONSTANT = 6.67430E-11  # kg^-1 m^3 s^-2
# according to https://ssd.jpl.nasa.gov/?constants


class CentralBody:
    """Massive central body around which another object can orbit.

    Current implementation requires object that orbits around it to be significantly less massive
    so that it's gravitational influence on the central body can be ignored.

    Attributes:
        mass: the body's mass in kG.
        radius: the body's radius.
        min_viable_orbit_r:
            the minimum viable distance an object could orbit at from the centre of the body in m
            because of factors like body size, terrain and atmosphere.
        mu:
            the standard gravitational parameter for the body in m^3 s^-2.
            """

    # TODO: Consider shortening __init__ docstring because of double information with class docstring.
    def __init__(self, mass: float,
                 radius: int,
                 lowest_orbit_from_surface: int = 0,
                 mu: float = None):
        """Initialize instance with mass, radius, min_viable_r and mu.

        Args:
            mass: the body's mass in kG.
            radius: the body's radius in m.
            lowest_orbit_from_surface:
                the minimum viable distance from the surface an object could orbit in m
                because of factors like atmosphere and terrain.
            mu:
                the standard gravitational parameter for the body in m^3 s^-2.
                the value of mu is currently knows to greater precision the G or M for many bodies
                so specifying the known value in the parameters might improve accuracy."""
        self.mass: float = mass
        self.radius: int = radius
        self.min_viable_orbit_r = radius + lowest_orbit_from_surface
        if mu is None:
            self.mu: float = mass * GRAVITATIONAL_CONSTANT
        else:
            self.mu: float = mu

    def add_radius(self, num: float or int) -> float or int:
        """Add this bodies radius to a number,
        so that orbits measured from the surface can easily be converted to orbits measure from the centre.

        Args:
            num: number to add radius to.

        Returns:
            num with the radius added to it."""
        return num + self.radius


class CentralBodyInOrbit(CentralBody):
    """A massive central body, around which another object can orbit, that itself is in an orbit.

    Consult parent class for full attribute documentation.

    Attributes:
        orbit: the orbit this body is in.
        hill_sphere_radius: the hill sphere radius of this body in m.
        max_viable_orbit_r:
            estimation of the maximum viable orbit r based on hill_sphere_radius in m rounded to nearest int"""

    def __init__(self, mass: float,
                 radius: int,
                 lowest_orbit_from_surface: int = 0,
                 mu: float = None,
                 orbit: orbits.Orbit = None):
        """Initialize instance with orbit, hill_sphere_radius, max_viable_orbit, and superclass attributes."""
        super().__init__(mass, radius, lowest_orbit_from_surface, mu)
        self.orbit = orbit
        self.hill_sphere_radius = None if orbit is None else CentralBodyInOrbit._hill_sphere(orbit, mass)
        self.max_viable_orbit_r = None if self.hill_sphere_radius is None else round(self.hill_sphere_radius / 3)
        #                                         TODO: Current number based on wikipedia, find better source  ^

    @staticmethod
    def _hill_sphere(orbit: orbits.Orbit, own_mass: float):
        """Calculate the radius of the hill sphere of a body.

        Args:
            orbit: the orbit the body is in.
            own_mass: the mass of the body to calculate the hill sphere radius for.

        Returns:
            the body's hill sphere radius in m."""
        return orbit.sm_axis * (1 - orbit.eccentricity) * \
               ((own_mass / (3 * orbit.central_body.mass)) ** (1 / 3))

    def compute_radia(self, permutations_per_section: int, section_limits: list[int] = None) -> list[int]:
        """Compute all radia permutations that should be used in generating an amount of possible orbits around
        a body, possibly divided into several sections.

        Args:
            permutations_per_section: amount of radia that should be computed in every section.
            section_limits:
                the left/right end of every section. self.min_viable_orbit_r and .max_viable_orbit_r are added
                respectively to start- end end of this list.

        Returns:
            ((#(section_limit) - 1) * permutations_per_section) radia.

        For example, when dividing into 3 sections:
        10.000 <-> 100.000 <-> 500.000 <-> 1.000.000.
        With permutations_per_sections = 1000.
        Then there will be 1000 uniformly distributed numbers between
        the limit on the left of the <-> symbol and the limit on the right of the symbol
        returned in an ordered list."""
        if section_limits is None: section_limits = []
        section_limits = [self.min_viable_orbit_r] + section_limits + [self.max_viable_orbit_r]
        radia = []
        while len(section_limits) > 1:
            for r in range(section_limits[0], section_limits[1],
                           (section_limits[1] - section_limits[0]) // permutations_per_section):
                radia.append(r)
            section_limits.pop(0)
        return radia