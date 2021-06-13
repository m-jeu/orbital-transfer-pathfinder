import orbitalmechanics.bodies as bodies
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
        manoeuvres: all manoeuvres associated with this Orbit. Added to by Manoeuvre constructor.
        semimajor_axis: the orbit's semimajor axis (a) in m.
        eccentricity: the orbit's eccentricity (e). 0 means orbit is circular.
        apogee: the orbit's apogee in m. Should be int for transfer-calculations.
        perigee: the orbit's perigee in m. Should be int for transfer-calculations.
        apsides: apogee and perigee in 1 set, for convenience."""

    def __init__(self, central_body: bodies.CentralBody, **kepler_elements):
        """Initialize instance with central_body, semimajor_axis, eccentricity, apogee and perigee.

        Keyword-arguments kepler_elements may contain:
            'a': semi-major axis.
            'e': eccentricity.
            'apo': apogee as integer.
            'per': perigee as integer.
        kepler_elements must contain either 'a' and 'e', or 'apo' and 'per'.
        Consult Class attribute documentation for full documentation.

        Raises:
            KeplerElementError: when kepler_elements arguments are not being passed properly.
        """
        self.central_body = central_body
        self.manoeuvres = set()
        if "a" in kepler_elements and "e" in kepler_elements:  # TODO: Check whether using kwargs like this is okay.
            self.sm_axis, self.eccentricity = kepler_elements["a"], kepler_elements["e"]
            self.apogee, self.perigee = Orbit._apo_and_per(self.sm_axis, self.eccentricity)
        elif "apo" in kepler_elements and "per" in kepler_elements:  # FIXME: String comparisons slow down performance.
            self.apogee, self.perigee = kepler_elements["apo"], kepler_elements["per"]
            self.sm_axis, self.eccentricity = Orbit._a_and_e(self.apogee, self.perigee)
        else:
            raise KeplerElementError()
        self.apsides: set[int] = {self.apogee, self.perigee}

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
        return round(a * (1 + e)), round(a * (1 - e))

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

    def evaluate_pro_retro_grade_manoeuvre(self, target_orbit) -> int or None:
        """Evaluate whether, and if so at what attitude, a pro- or retrograde manoeuvre is possible
        to transfer to a certain target orbit.

        Args:
            target_orbit: the orbit to transfer to.

        Returns:
            None if manoeuvre is not possible.
            The distance from the central body's centre at which it's possible if it's possible."""
        overlap = self.apsides.intersection(target_orbit.apsides)
        return None if len(overlap) == 0 else overlap.pop()

    def __str__(self) -> str:
        return f"Orbit: apoapsis={self.apogee}m periapsis={self.perigee}m."

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        """Determine equality based on apsides.

        Args:
            other: object to check determine equality to.

        Returns:
            equality to other object."""
        if isinstance(other, Orbit):
            return self.apsides == other.apsides
        return False

    def __hash__(self) -> int:
        """Hash based on apoapsis/periapsis.

        Returns:
            hash."""
        return hash((self.apogee, self.perigee))

    # TODO: Move to bodies.CentralBody once circle import is fixed.
    @staticmethod
    def compute_radia(section_limits: list[int], permutations_per_section: int) -> list[int]:
        """Compute all radia permutations that should be used in generating an amount of possible orbits around
        a body, possibly divided into several sections.

        Args:
            section_limits: the left/right end of every section.
            permutations_per_section: amount of radia that should be computed in every section.

        Returns:
            ((#(section_limit) - 1) * permutations_per_section) radia.

        For example, when dividing into 3 sections:
        10.000 <-> 100.000 <-> 500.000 <-> 1.000.000.
        With permutations_per_sections = 1000.
        Then there will be 1000 uniformly distributed numbers between
        the limit on the left of the <-> symbol and the limit on the right of the symbol
        returned in an ordered list."""
        radia = []
        while len(section_limits) > 1:
            for r in range(section_limits[0], section_limits[1],
                           (section_limits[1] - section_limits[0]) // permutations_per_section):
                radia.append(r)
            section_limits.pop()
        return radia

    # TODO: Move to bodies.CentralBody once circle import is fixed.
    @staticmethod
    def create_orbits(central_body: bodies.CentralBody,
                      permutations_per_section: int,
                      section_limiters: list[int] = None) -> list:
        """Generate a significant amount of possible orbits around a certain CentralBody, divided into sections.
        Calls Orbit.compute_radia with central_body.min_viable_orbit_r and central_body.max_viable_orbit_r as extra
        limits. Consult Orbit.compute_radia for detailed section_limiters information.

        Args:
            central_body:
                CentralBody that orbits are around. CentralBody should have had orbit parameter filled on
                initialization, so that Hill Sphere could be estimated.
            permutations_per_section:
                the amount of attitudes that should be used for apoapsis/periapsis in every section.
            section_limiters:
                the limits between sections. Consult Orbit.compute_radia() for detailed documentation.
                """  # TODO: Add Returns doc
        if section_limiters is None: section_limiters = []
        section_limiters = [central_body.min_viable_orbit_r] + section_limiters + [central_body.max_viable_orbit_r]
        radia = Orbit.compute_radia(section_limiters, permutations_per_section)
        orbits = []
        for per_i in range(len(radia)):
            for apo_i in range(per_i, len(radia)):
                orbits.append(Orbit(central_body, apo=radia[apo_i], per=radia[per_i]))
        return orbits



