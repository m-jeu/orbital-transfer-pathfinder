# To prevent circle import (for typehints) problems
#from typing import TYPE_CHECKING TODO: Check whether this is necesarry after implementing new features.
#if TYPE_CHECKING:
import orbitalmechanics.manoeuvres as manoeuvres


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

    def __init__(self, central_body: bodies.CentralBody,
                 a: int = None, e: float = None,
                 apo: int = None, per: int = None):
        """Initialize instance with central_body, semimajor_axis, eccentricity, apogee and perigee.

        Either apo/per, or a/e need to be passed. The other 2 can be computed from the first 2.
        Consult Class attribute documentation for full documentation.

        Raises:
            KeplerElementError: when kepler_elements arguments are not being passed properly.
        """
        self.central_body = central_body
        self.manoeuvres = set()
        if apo is not None and per is not None:  # Compute a/e from apo/per
            self.apogee, self.perigee = apo, per
            self.sm_axis, self.eccentricity = Orbit._a_and_e(self.apogee, self.perigee)
        elif a is not None and e is not None:  # Compute apo/per from a/e
            self.sm_axis, self.eccentricity = a, e
            self.apogee, self.perigee = Orbit._apo_and_per(self.sm_axis, self.eccentricity)
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
