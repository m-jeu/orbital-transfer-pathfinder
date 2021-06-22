from unittest import TestCase

import orbitalmechanics.bodies
import orbitalmechanics.orbits

class TestCentralBody(TestCase):

    def setUp(self):
        self.test_body_with_mu = orbitalmechanics.bodies.CentralBody(1000000,
                                                                     10000,
                                                                     1000,
                                                                     123.45)

        self.test_body_without_mu = orbitalmechanics.bodies.CentralBody(1000000,
                                                                        10000,
                                                                        1000)

    def test_constructor(self):
        self.assertEqual(self.test_body_with_mu.mu, 123.45,
                         "When CentralBody is passed value in mu parameter, this should be used as mu attribute.")

        self.assertAlmostEqual(self.test_body_without_mu.mu, 6.6743E-05,
                               msg="""When CentralBody is not passed value in mu parameter
, this should be calculated using the gravitational constant.""")

        self.assertEqual(self.test_body_with_mu.min_viable_orbit_r, 11000,
                         """CentralBody constructor parameters radius and lowest_orbit_from_surface should be added
together to determine min_viable_orbit_r.""")

        with self.assertRaises(AttributeError, msg="CentralBody should not have attribute hill_sphere_radius set."):
            self.test_body_with_mu.hill_sphere_radius

        with self.assertRaises(AttributeError, msg="CentralBody should not have attribute max_viable_orbit_r set."):
            self.test_body_with_mu.max_viable_orbit_r

    def test_add_radius(self):
        self.assertEqual(10001, self.test_body_with_mu.add_radius(1),
                         "CentralBody.add_radius() should add the body's radius to passed parameter.")


class TestCentralBodyInOrbit(TestCase):

    def setUp(self):
        test_orbits_central_body = orbitalmechanics.bodies.CentralBody(1000000000,
                                                                       1000,
                                                                       0)

        orbit = orbitalmechanics.orbits.Orbit(test_orbits_central_body,
                                              a=1000000, e=0.1, i=0)

        self.test_body = orbitalmechanics.bodies.CentralBodyInOrbit(1000,
                                                                    100,
                                                                    0,
                                                                    orbit=orbit)

    def test_constructor(self):
        self.assertAlmostEqual(self.test_body.hill_sphere_radius,
                               6240.251469,
                               delta=6,
                               msg="""CentralBodyInOrbit constructor should approximate hill_sphere_radius
using provided orbit, and it's central body's attributes using the Hill sphere radius formula.""")

        self.assertAlmostEqual(self.test_body.max_viable_orbit_r,
                               2080.083823,
                               delta=6,
                               msg="""CentralBodyInOrbit constructor should approximate max viable orbit by
    dividing hill sphere radius by 3.""")


    def test_compute_radia(self):
        radia_testcase_1 = self.test_body.compute_radia(25)

        self.assertTrue(abs(len(radia_testcase_1) - 25) <= 1,
                        """When not passed any section limits, CentralBodyInOrbit should generate an amount of
radia equal to or with a maximum difference of 1 to permutations_per_sections.""")

        for i in range(len(radia_testcase_1) - 2):
            self.assertEqual(radia_testcase_1[i + 1] - radia_testcase_1[i],
                             radia_testcase_1[i + 2] - radia_testcase_1[i + 1],
                             msg="""Radia computed with CentralBodyInOrbit.compute_radia() should be
evenly spaced between section limits.""")

        radia_testcase_2 = self.test_body.compute_radia(10, [1200])

