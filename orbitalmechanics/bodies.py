GRAVITATIONAL_CONSTANT = 6.67430E-11 #kg^-1 m^3 s^-2
#according to https://ssd.jpl.nasa.gov/?constants


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
        mu: the standard gravitational parameter for the body in m^3 s^-2."""

    def __init__(self, mass: float,
                 radius: int,
                 lowest_orbit_from_surface: int = 0,
                 mu: float = None):
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
            """
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


earth = CentralBody(5.9736E24,
                    6371000,
                    160000,
                    3.986004418E14)
