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
        mu: the standard gravitational parameter for the body in m^3 s^-2.
        orbit:
            the orbit this body is in. optional, but needed to compute the Hill Sphere."""

    # TODO: Consider shortening __init__ docstring because of double information with class docstring.
    def __init__(self, mass: float,
                 radius: int,
                 lowest_orbit_from_surface: int = 0,
                 mu: float = None,
                 orbit=None):  # FIXME: Typehint & Circle import
        """Initialize instance.

        Args:
            mass: the body's mass in kG.
            radius: the body's radius in m.
            lowest_orbit_from_surface:
                the minimum viable distance from the surface an object could orbit in m
                because of factors like atmosphere and terrain.
            mu:
                the standard gravitational parameter for the body in m^3 s^-2.
                the value of mu is currently knows to greater precision the G or M for many bodies
                so specifying the known value in the parameters might improve accuracy.
            orbit:
                optional orbit around another more massive Central Body.
                typehint currently not possible because of circle-import problem."""
        self.mass: float = mass
        self.radius: int = radius
        self.min_viable_orbit_r = radius + lowest_orbit_from_surface
        if mu is None:
            self.mu: float = mass * GRAVITATIONAL_CONSTANT
        else:
            self.mu: float = mu
        self.orbit = orbit
        self.hill_sphere_radius = None if orbit is None else CentralBody._hill_sphere(orbit, mass)

    @staticmethod
    def _hill_sphere(orbit, own_mass: float):
        """Calculate the radius of the hill sphere of a body.

        Args:
            orbit: the orbit the body is in. Typehint currently not possible because of circle import problem.
            own_mass: the mass of the body to calculate the hill sphere radius for.

        Returns:
            the body's hill sphere radius in m."""
        return orbit.sm_axis * (1 - orbit.eccentricity) * \
               ((own_mass / (3 * orbit.central_body.mass)) ** (1/3))

    def add_radius(self, num: float or int) -> float or int:
        """Add this bodies radius to a number,
        so that orbits measured from the surface can easily be converted to orbits measure from the centre.

        Args:
            num: number to add radius to.

        Returns:
            num with the radius added to it."""
        return num + self.radius
