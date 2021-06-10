import bodies
import mmath.math


class KeplerElementError(Exception):
    """Exception to help diagnose problems related to not initializing an Orbit object with the proper parameters."""
    def __init__(self):
        super().__init__("""Orbit should be initialized with either:
-semi-major axis and eccentricity as 'a' and 'e' or
-apogee and perigee as 'apo' and 'per'
in the keyword argument.""")


class Orbit:
    """An orbit around a central body.

    Attributes:
        central_body: the body this orbit is around.
        semimajor_axis: the orbit's semimajor axis (a) in m.
        eccentricity: the orbit's eccentricity (e). 0 means orbit is circular.
        apogee: the orbit's apogee in m.
        perigee: the orbit's perigee in m."""

    def __init__(self, central_body: bodies.CentralBody, **kepler_elements):
        """Initialize instance with central_body, semimajor_axis, eccentricity, apogee and perigee.

        Keyword-arguments kepler_elements may contain:
            'a': semi-major axis.
            'e': eccentricity.
            'apo': apogee.
            'per': perigee.
        kepler_elements must contain either 'a' and 'e', or 'apo' and 'per'.
        Consult Class attribute documentation for full documentation.

        Raises:
            KeplerElementError: when kepler_elements arguments are not being passed properly.
        """
        self.central_body = central_body
        if "a" in kepler_elements and "e" in kepler_elements:
            self.sm_axis, self.eccentricity = kepler_elements["a"], kepler_elements["e"]
            self.apogee, self.perigee = Orbit._apo_and_per(self.sm_axis, self.eccentricity)
        elif "apo" in kepler_elements and "per" in kepler_elements:
            self.apogee, self.perigee = kepler_elements["apo"], kepler_elements["per"]
            self.sm_axis, self.eccentricity = Orbit._a_and_e(self.apogee, self.perigee)
        else:
            raise KeplerElementError()

    @staticmethod
    def _apo_and_per(a: int or float, e: float) -> tuple[float, float]:
        """Compute an apogee and perigee from semi-major axis and eccentricity.

        Args:
            a: orbit semi-major axis in m.
            e: orbit eccentricity.

        Returns:
            tuple that contains:
                0: orbit apogee in m.
                1: orbit perigee in m."""
        return a * (1 + e), a * (1 - e)

    @staticmethod
    def _a_and_e(apo: int or float, per: int or float) -> tuple[float, float]:
        """Compute a semi-major axis and eccentricity from apogee and perigee.

        Args:
            apo: orbit apogee in m.
            per: orbit perigee in m.

        Returns:
            tuple that contains:
                0: orbit semi-major axis in m.
                1: orbit eccentricity."""
        return mmath.math.v_avg(apo, per), 1 - (2 / (apo / per) + 1)

    def v_at(self, r) -> float:
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
        return target_orbit.v_at(shared_r) - self.v_at(shared_r)


#Example use
if __name__ == "__main__":
    leo = Orbit(bodies.earth, a=bodies.earth.add_radius(200000), e=0)
    gto = Orbit(bodies.earth, a=24367500, e=0.730337539)
    geo = Orbit(bodies.earth, a=42164000, e=0)
    iss = (Orbit(bodies.earth, apo=bodies.earth.add_radius(422000), per=bodies.earth.add_radius(418000)))

    print("200km LEO -> GTO -> GEO costs approx:")
    print(f"{leo.pro_retro_grade(gto, gto.perigee) + gto.pro_retro_grade(geo, gto.apogee)} Delta-V.")
