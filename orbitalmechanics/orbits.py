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

    def pro_retro_grade(self, target_orbit, shared_r: float) -> float:
        """Compute the Delta-V cost for a simple pro- or retrograde manoeuvre.

        Args:
            target_orbit: the orbit to transfer to.
            shared_r: the distance from the central bodies the original and target orbit share.

        Returns:
            The required delta-V to go from the original orbit to the target orbit.
            Negative if manoeuvre requires expending the delta-V in retrograde direction."""
        return target_orbit._v_at(shared_r) - self._v_at(shared_r)


#Example use
if __name__ == "__main__":
    leo = Orbit(bodies.earth, bodies.earth.add_radius(200000), 0)
    gto = Orbit(bodies.earth, 24367500, 0.730337539)
    geo = Orbit(bodies.earth, 42164000, 0)

    print("200km LEO -> GTO -> GEO costs approx:")
    print(f"{leo.pro_retro_grade(gto, gto._per()) + gto.pro_retro_grade(geo, gto._apo())} Delta-V.")
