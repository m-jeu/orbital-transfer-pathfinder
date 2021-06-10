import bodies


class Orbit:
    """An orbit around a central body.

    Attributes:
        central_body: the body this orbit is around.
        semimajor_axis: the orbit's semimajor axis (a) in m.
        eccentricity: the orbit's eccentricity (e). 0 means orbit is circular."""

    def __init__(self,
                 central_body: bodies.CentralBody,
                 semimajor_axis: int,
                 eccentricity: float):
        """Initialize Orbit with central_body, semimajor_axis, eccentricity."""
        self.central_body = central_body
        self.sm_axis = semimajor_axis
        self.eccentricity = eccentricity

    def _per(self):
        """Compute the orbit perigee.

        Returns:
            Orbit perigee in m."""
        return self.sm_axis * (1 - self.eccentricity)

    def _apo(self):
        """Compute the orbit apogee.

        Returns:
            Orbit apogee in m."""
        return self.sm_axis * (1 + self.eccentricity)

    def _v_at(self, r) -> float:
        """Compute the speed relative to the central body at a certain point in the orbit.

        Args:
            r: the current attitude from the centre of the central body in m.

        Returns:
            The speed relative to the central body at the specified attitude in m s^-1."""
        return (self.central_body.mu * ((2 / r) - (1 / self.sm_axis))) ** 0.5


#Approximate orbit, because of drag this changes constantly
iss = Orbit(bodies.earth,
            bodies.earth.add_radius(420000),
            0)
