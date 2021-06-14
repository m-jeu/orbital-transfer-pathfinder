import orbitalmechanics.bodies as bodies
import orbitalmechanics.orbits as orbits
import orbitalmechanics.manoeuvres as manoeuvres


class OrbitCollection:
    """A collection of orbits around 1 central body.

    Attributes:
        central_body: the body the orbits are around.
        apside_map: dictionary with apsides as keys, and list containing every orbit with that apside as value.
        orbits: all the orbits in this collection.
        manoeuvre_types: all types of manoeuvres (subclass of Manoeuvre) that can be performed between self.orbits."""

    def __init__(self, central_body: bodies.CentralBody, manoeuvre_types: list[type]):
        """Initialize instance with central_body, apside_map and orbits.

        Args:
            central_body: the body the orbits are around."""
        self.central_body = central_body
        self.apside_map = {}
        self.orbits = []
        self.manoeuvre_types = manoeuvre_types # TODO: For later use, unused for now.

    def add_orbit(self, orbit: orbits.Orbit):
        """Add an orbit to self.orbits, and add it to self.apside_map according to it's own apsides.

        Args:
            orbit: orbit to add."""
        for apside in orbit.apsides:
            if apside not in self.apside_map:
                self.apside_map[apside] = [orbit]
            else:
                self.apside_map[apside].append(orbit)
        self.orbits.append(orbit)

    def create_orbits(self,
                      permutations_per_section: int,
                      section_limiters: list[int] = None):
        """Generate a significant amount of possible orbits around the CentralBody, divided into sections.
        Calls CentralBody.compute_radia with central_body.min_viable_orbit_r and central_body.max_viable_orbit_r as
        extra limits. Consult CentralBody.compute_radia for detailed section_limiters information.

        Args:
            permutations_per_section:
                the amount of attitudes that should be used for apoapsis/periapsis in every section.
            section_limiters:
                the limits between sections. Consult CentralBody.compute_radia() for detailed documentation.
                """
        radia = self.central_body.compute_radia(permutations_per_section, section_limiters)
        for per_i in range(len(radia)):
            for apo_i in range(per_i, len(radia)):
                self.add_orbit(orbits.Orbit(self.central_body, apo=radia[apo_i], per=radia[per_i]))

    def compute_all_manoeuvres(self): # FIXME: Not very modular.
        """Compute all possible 1-burn pro- retrograde manoeuvres between all orbits that share an apside.

        Manoeuvres assign themselves to corresponding orbits, so no return value."""
        for r, orbits in self.apside_map.items():
            for i in range(0, len(orbits)):
                for j in range(i + 1, len(orbits)):
                    manoeuvres.ProRetroGradeManoeuvre(orbits[i], orbits[j], r)


