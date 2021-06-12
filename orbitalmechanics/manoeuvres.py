import orbitalmechanics.orbits as orbits
import orbitalmechanics.bodies as bodies

import abc


class BaseManoeuvre(metaclass=abc.ABCMeta):
    """An abstract bidirectional 1-burn manoeuvre between 2 orbits with a certain Delta-V cost.

    Attributes:
        orbit1: orbit on one 'end' of the manoeuvre.
        orbit2: orbit on other 'end' of the manoeuvre.
        dv: Delta-V cost."""
    def __init__(self, orbit1: orbits.Orbit, orbit2: orbits.Orbit, insect_r):
        """Initialize instance with orbit1, orbit2, dv attributes.

        Non-attribute args:
            insect_r: the attitude at which the 2 orbits intersect (and the manoeuvre is performed)."""
        self.orbit1: orbits.Orbit = orbit1
        self.orbit2: orbits.Orbit = orbit2
        self.dv = self._delta_v(insect_r)

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


class ProRetroGradeManoeuvre(BaseManoeuvre):
    """Bidirectional 1-burn pro- or retrograde manoeuvre at apoapsis or periapsis.

    Consult parent documentation for full attribute documentation."""
    def __init__(self, orbit1: orbits.Orbit, orbit2: orbits.Orbit, insect_r):
        """Initialize instance with orbit1, orbit2, dv attributes.

        Consult parent method documentation for full documentation."""
        super().__init__(orbit1, orbit2, insect_r)

    def _delta_v(self, insect_r):
        """Compute the manoeuvre's Delta-V cost.

        Consult parent method documentation for full documentation."""
        return abs(self.orbit1.v_at(insect_r) - self.orbit2.v_at(insect_r))