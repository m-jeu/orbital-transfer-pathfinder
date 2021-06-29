from __future__ import annotations
import abc

import orbital_transfer_pathfinder.lib.mmath.math as mmath
import orbital_transfer_pathfinder.lib.orbitalmechanics.orbits as orbits
import orbital_transfer_pathfinder.lib.shortpathfinding.custom_dijkstras_algorithm as custom_dijkstras_algorithm


class BaseManoeuvre(custom_dijkstras_algorithm.CDijkstraEdge, metaclass=abc.ABCMeta):
    """An abstract bidirectional 1-burn manoeuvre between 2 orbits with a certain Delta-V cost.

    Attributes:
        orbit1: orbit on one 'end' of the manoeuvre.
        orbit2: orbit on other 'end' of the manoeuvre.
        dv: Delta-V cost."""
    def __init__(self, orbit1: orbits.Orbit, orbit2: orbits.Orbit, insect_r: int):
        """Initialize instance with orbit1, orbit2, dv attributes.
        Adds itself to orbit1- and orbit2.manoeuvres.

        Non-attribute args:
            insect_r: the attitude at which the 2 orbits intersect (and the manoeuvre is performed)."""
        self.orbit1: orbits.Orbit = orbit1
        self.orbit2: orbits.Orbit = orbit2
        self.dv = self._delta_v(insect_r)
        self.orbit1.manoeuvres.add(self)
        self.orbit2.manoeuvres.add(self)

    @abc.abstractmethod
    def _delta_v(self, insect_r):
        """Compute the manoeuvre's Delta-V cost.

        Args:
            insect_r: the attitude at which the 2 orbits intersect (and the manoeuvre is performed)."""
        pass

    def get_other(self, origin: orbits.Orbit):
        """Get the orbit on the other 'end' of the manoeuvre.

        Args:
            origin: orbit on one 'end' of the manoeuvre, whose other side should be fetched."""
        return self.orbit2 if origin == self.orbit1 else self.orbit1  # TODO: Consider implementing exception.

    def get_weight(self) -> float:
        """Get the Delta-V of this manoeuvre as weight for pathfinding.

        Returns:
            Delta-V of this manoeuvre."""
        return self.dv

    @staticmethod
    @abc.abstractmethod
    def evaluate(orbit1: orbits.Orbit, orbit2: orbits.Orbit) -> bool:
        """Evaluate whether a manoeuvre of own type is possible between 2 orbits.

        Args:
            orbit1: orbit1 to compare.
            orbit2: orbit2 to compare.

        Returns:
            boolean for manoeuvre possibility.
            also returns False if orbit1 is orbit2
            or if the manoeuvre simply doesn't make sense (dependant on subtype)."""
        pass

    def __eq__(self, other) -> bool:
        """Determine equality based on connected orbits.

        Args:
            other: object to check determine equality to.

        Returns:
            equality to other object."""
        if isinstance(other, BaseManoeuvre):
            return ((self.orbit1 == other.orbit1) and (self.orbit2 == other.orbit2)) or \
                   ((self.orbit1 == other.orbit2) and (self.orbit2 == other.orbit1))  # FIXME: Ugly conditional.
        return False

    def __hash__(self) -> int:
        """Hash based on associated orbits.

        Returns:
            hash."""
        return hash((self.orbit1, self.orbit2))

    def __str__(self) -> str:
        return f"{self.dv}m/s between {self.orbit1} and {self.orbit2}."

    def __repr__(self) -> str:
        return self.__str__()


class ProRetroGradeManoeuvre(BaseManoeuvre):
    """Bidirectional 1-burn pro- or retrograde manoeuvre at apoapsis or periapsis.

    Consult parent documentation for full attribute documentation."""

    def _delta_v(self, insect_r):
        """Compute the manoeuvre's Delta-V cost.

        Consult parent method documentation for full documentation."""
        return abs(self.orbit1.v_at(insect_r) - self.orbit2.v_at(insect_r))

    @staticmethod
    def evaluate(orbit1: orbits.Orbit, orbit2: orbits.Orbit) -> bool:
        """Evaluate whether 1-burn pro- or retrograde manoeuvre is possible between 2 orbits.

        Args:
            orbit1: orbit1 to compare.
            orbit2: orbit2 to compare.

        Returns:
            boolean for manoeuvre possibility.
            also returns False if orbit1 is orbit2."""
        if orbit1.inclination != orbit2.inclination:
            return False
        return len(orbit1.apsides.intersection(orbit2.apsides)) >= 1

    def __str__(self) -> str:
        return "Pro- Retrograde " + super().__str__()


class InclinationChange(BaseManoeuvre):
    """Bidirectional 1-burn pure plane change manoeuvre.

    Consult parent documentation for full attribute documentation."""

    def _delta_v(self, insect_r):
        return mmath.cosine_rule(self.orbit1.v_at(insect_r),
                                 self.orbit2.v_at(insect_r),
                                 abs(self.orbit1.inclination - self.orbit2.inclination))

    @staticmethod
    def evaluate(orbit1: orbits.Orbit, orbit2: orbits.Orbit) -> bool:
        """Evaluate whether 1-burn pure plane change manoeuvre is possible between 2 orbits.

        Args:
            orbit1: orbit1 to compare.
            orbit2: orbit2 to compare.

        Returns:
            boolean for manoeuvre possibility.
            also returns False if orbit1 is orbit2 or if the orbits share an inclination already."""
        return orbit1.apsides == orbit2.apsides and orbit1.inclination != orbit2.inclination

    def __str__(self) -> str:
        return "Inclination Change " + super().__str__()


class InclinationAndProRetroGradeManoeuvre(InclinationChange):
    """Bidirectional 1-burn pro- or retrograde combined with plane change manoeuvre at apoapsis or periapsis.

    Consult parent documentation for full attribute documentation."""

    @staticmethod
    def evaluate(orbit1: orbits.Orbit, orbit2: orbits.Orbit) -> bool:
        """Evaluate whether 1-burn pro- or retrograde combined with plane change manoeuvre at apoapsis or periapsis
        is possible between 2 orbits.

            Args:
                orbit1: orbit1 to compare.
                orbit2: orbit2 to compare.

            Returns:
                boolean for manoeuvre possibility.
                also returns False if orbit1 is orbit2 or if the orbits share an inclination already."""
        if orbit1.inclination == orbit2.inclination:
            return False
        return len(orbit1.apsides.intersection(orbit2.apsides)) >= 1

    def __str__(self) -> str:
        return "Pro- Retrograde + Inclination Change " + super().__str__()