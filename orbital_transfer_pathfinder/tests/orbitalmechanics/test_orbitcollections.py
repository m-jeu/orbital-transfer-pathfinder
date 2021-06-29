from unittest import TestCase

import orbital_transfer_pathfinder.lib.orbitalmechanics.bodies as bodies
import orbital_transfer_pathfinder.lib.orbitalmechanics.orbits as orbits
import orbital_transfer_pathfinder.lib.orbitalmechanics.manoeuvres as manoeuvres
import orbital_transfer_pathfinder.lib.orbitalmechanics.orbitcollections as orbitcollections


class TestOrbitCollection(TestCase):
    def setUp(self):
        sun = bodies.CentralBody(1.989E30,
                                 696349999,
                                 mu=1.32712440018E20)

        self.earth = bodies.CentralBodyInOrbit(5.9736E24,
                                               6371000,
                                               orbits.Orbit(sun,
                                                            a=149598023000,
                                                            e=0.0167086,
                                                            i=7),
                                               160000,
                                               3.986004418E14)

    def test_add_orbit(self):
        test_orbit = orbits.Orbit(self.earth,
                                  apo=2000000,
                                  per=500000,
                                  i=28)

        test_collection = orbitcollections.OrbitCollection(self.earth, [])

        test_collection.add_orbit(test_orbit)

        self.assertEqual(test_collection.orbits,
                         {test_orbit},
                         msg="""OrbitCollection.add_orbit() should add passed orbit to self.orbits.""")

        self.assertEqual(test_collection.apside_map,
                         {500000: [test_orbit],
                          2000000: [test_orbit]},
                         msg="""OrbitCollection.add_orbit() should add passed orbit to self.apside_map under the orbit's
                         apsides.""")

        self.assertEqual(test_collection.inclination_map,
                         {28: [test_orbit]},
                         msg="""OrbitCollection.add_orbit() should add passed orbit to self.inclination_map
                         under the orbit's inclination.""")

    def test_create_orbits(self):
        test_orbit = orbits.Orbit(self.earth,
                                  apo=2000000,
                                  per=123456,
                                  i=28)

        test_collection_1 = orbitcollections.OrbitCollection(self.earth, [])
        test_collection_1.add_orbit(test_orbit)
        test_collection_1.create_orbits(5, inclination_increment=10)

        self.assertTrue(len(test_collection_1.inclination_map[28]) > 1,
                        msg="""OrbitCollection.create_orbits() should create more orbits on inclinations already
established in self.inclination_map.""")

        self.assertTrue(len(test_collection_1.apside_map[123456]) > 1,
                        msg="""OrbitCollection.create_orbits() should create more orbits on apsides already
established in self.apside_map.""")

        self.assertTrue(len(test_collection_1.inclination_map) > 1,
                        msg="""OrbitCollection.create_orbits() should create orbits on more inclinations then just the
ones already established in self.inclination_map.""")

        self.assertTrue(len(test_collection_1.apside_map) > 2,
                        msg="""OrbitCollection.create_orbits() should create orbits on more apsides then just the ones
already established in self.apside_map.""")

    def test_compute_all_manoeuvres(self):
        test_orbit_1 = orbits.Orbit(self.earth,
                                    apo=2000000,
                                    per=500000,
                                    i=28)

        test_orbit_2 = orbits.Orbit(self.earth,
                                    apo=2000000,
                                    per=500000,
                                    i=0)

        test_orbit_3 = orbits.Orbit(self.earth,
                                    apo=20000000,
                                    per=2000000,
                                    i=28)

        test_collection_1 = orbitcollections.OrbitCollection(self.earth,
                                                             [manoeuvres.ProRetroGradeManoeuvre,
                                                              manoeuvres.InclinationChange])
        test_collection_1.add_orbit(test_orbit_1)
        test_collection_1.add_orbit(test_orbit_2)
        test_collection_1.add_orbit(test_orbit_3)
        test_collection_1.compute_all_manoeuvres()

        self.assertTrue(len(test_orbit_1.manoeuvres) == 2,
                        msg="""OrbitCollection.compute_all_manoeuvres() should compute and create all possible
manoeuvres between stored orbits.""")