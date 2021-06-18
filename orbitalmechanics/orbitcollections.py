import orbitalmechanics.bodies as bodies
import orbitalmechanics.orbits as orbits
import orbitalmechanics.manoeuvres as manoeuvres

import loadingbar.loadingbar as loadingbar


class OrbitCollection:
    """A collection of orbits around 1 central body.

    Attributes:
        central_body: the body the orbits are around.
        apside_map: dictionary with apsides as keys, and list containing every orbit with that apside as value.
        orbits: all the orbits in this collection.
        manoeuvre_types: all types of manoeuvres (subclass of Manoeuvre) that can be performed between self.orbits."""

    def __init__(self, central_body: bodies.CentralBodyInOrbit, manoeuvre_types: list[type]):
        """Initialize instance with central_body, apside_map and orbits.

        Args:
            central_body: the body the orbits are around."""
        self.central_body = central_body
        self.apside_map = {}
        self.orbits = []
        self.manoeuvre_types = manoeuvre_types

    def add_orbit(self, orbit: orbits.Orbit):
        """Add an orbit to self.orbits, and add it to self.apside_map according to it's own apsides.

        Args:
            orbit: orbit to add."""
        for apside in orbit.apsides:
            if apside not in self.apside_map:
                self.apside_map[apside] = [orbit]
            else:
                self.apside_map[apside].append(orbit)

    def _create_orbits_on_one_inclination(self,
                                          radia: list[int],
                                          inclination: int):
        """Create a significant amount of possible orbits around the CentralBody on one inclination,
        divided into sections, and assign them to self.orbits.

        Will create #(radia) ^2 orbits.

        Args:
            radia: the radia that should be used as apoapsis/periapsis.
            inclination: the inclination to create the orbits at."""
        for per_i in range(len(radia)):
            for apo_i in range(per_i, len(radia)):
                self.add_orbit(orbits.Orbit(self.central_body, apo=radia[apo_i], per=radia[per_i], i=inclination))

    def create_orbits(self,
                      permutations_per_section: int,
                      section_limiters: list[int] = None,
                      inclination_increment: int = 1):
        """Generate a significant amount of possible orbits around the CentralBody, divided into sections.
        Calls CentralBody.compute_radia with central_body.min_viable_orbit_r and central_body.max_viable_orbit_r as
        extra limits. Consult CentralBody.compute_radia for detailed section_limiters information.
        Will call self._create_orbits_on_one_inclination for every inclination (0 - 180).

        Args:
            permutations_per_section:
                the amount of attitudes that should be used for apoapsis/periapsis in every section.
            section_limiters:
                the limits between sections. Consult CentralBody.compute_radia() for detailed documentation.
            inclination_increment:
                how big the gap between inclinations between orbits should be.
                1 will create orbits at 180 different inclinations, 5 will create orbits at 36 different inclinations.
                """
        radia = self.central_body.compute_radia(permutations_per_section, section_limiters)
        for i in range(0, 181, inclination_increment):
            self._create_orbits_on_one_inclination(radia, i)

    def compute_all_manoeuvres(self, visualize: bool = False):
        """Compute all possible
         manoeuvres between all orbits that share an apside.

        Manoeuvres assign themselves to corresponding orbits, so no return value.

        Args:
            visualize: whether the progress should be visualised by loadingbar.LoadingBar."""
        # The 'else None' doesn't really change anything, but it just prevents a pointless Warning from showing up.
        lb = loadingbar.LoadingBar(len(self.apside_map)) if visualize else None
        for r, orbits in self.apside_map.items():
            if visualize: lb.increment()
            for i in range(len(orbits)):
                for j in range(i + 1, len(orbits)):
                    for manoeuvre_type in self.manoeuvre_types:
                        if manoeuvre_type.evaluate(orbits[i], orbits[j]):
                            manoeuvre_type(orbits[i], orbits[j], r)
                            break
