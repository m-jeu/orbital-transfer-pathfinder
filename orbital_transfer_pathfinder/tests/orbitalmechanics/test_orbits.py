from unittest import TestCase

import orbital_transfer_pathfinder.lib.orbitalmechanics.bodies as bodies
import orbital_transfer_pathfinder.lib.orbitalmechanics.orbits as orbits


class TestOrbit(TestCase):

    def test_constructor(self):
        central_body = bodies.CentralBody(1000,
                                          1000,
                                          0,
                                          1000)

        test_orbit_0 = orbits.Orbit(central_body,
                                    apo=10000,
                                    per=20000)

        self.assertEqual(test_orbit_0.apogee, 20000,
                         "Orbit constructor should switch around apogee and perigee when passed perigee is greater"
                         "then passed apogee.")


        test_orbit_1 = orbits.Orbit(central_body,
                                    a=10000,
                                    e=0.1)

        self.assertEqual(test_orbit_1.apogee, 11000,
                         "Orbit constructor should be able to calculate apogee when passed a and e.")

        self.assertEqual(test_orbit_1.perigee, 9000,
                         "Orbit constructor should be able to calculate perigee when passed a and e.")

        self.assertEqual(test_orbit_1.inclination, 0,
                         "Orbit inclination should be 0 by default.")

        test_orbit_2 = orbits.Orbit(central_body,
                                    apo=11000,
                                    per=9000)

        self.assertAlmostEqual(test_orbit_2.sm_axis,
                               10000,
                               msg="Orbit constructor should be able to calculate "
                                   "semimajor-axis when passed apo and per.")

        self.assertAlmostEqual(test_orbit_2.eccentricity,
                               0.1,
                               msg="Orbit constructor should be able to calculate "
                                   "eccentricity when passed apo and per.")

        with self.assertRaises(orbits.KeplerElementError,
                               msg="Orbit constructor should throw KeplerElementError when not passed"
                                   " correct parameters for orbit construction."):
            orbits.Orbit(central_body, a=1000, apo=11000, i=20)

    def test_v_at(self):
        earth = bodies.CentralBody(5.972E24,
                                   6371000,
                                   200000,
                                   3.986004418E14)

        gto = orbits.Orbit(earth, a=24367500, e=0.730337539)

        self.assertAlmostEqual(gto.v_at(gto.perigee), 10245.155848246606,
                               msg="Orbit.v_at should be able to compute speed at certain point in orbit using "
                                   "vis-viva equation.")
