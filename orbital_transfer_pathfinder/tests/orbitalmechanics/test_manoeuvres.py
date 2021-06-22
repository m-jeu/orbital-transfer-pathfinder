from unittest import TestCase

import orbital_transfer_pathfinder.lib.orbitalmechanics.bodies as bodies
import orbital_transfer_pathfinder.lib.orbitalmechanics.orbits as orbits
import orbital_transfer_pathfinder.lib.orbitalmechanics.manoeuvres as manoeuvres


# Normally, testing abstract classes is not standard practice.
# In this case, there's some quite essential behaviour that would be strange to test in concrete subclasses.
# Because module modularity is based on creating many subclasses of BaseManoeuvre.

class TestBaseManoeuvre(TestCase):

    # Concrete implementation of Abstract BaseManoeuvre so that objects can be initialized.
    # Abstract methods must be implemented, but these don't have to be tested.
    class ConcreteManoeuvre(manoeuvres.BaseManoeuvre):
        def _delta_v(self, insect_r):
            return insect_r * 10

        @staticmethod
        def evaluate(orbit1: orbits.Orbit, orbit2: orbits.Orbit) -> bool:
            return True

    # Actual tests
    def setUp(self):
        self.central_body = bodies.CentralBody(0, 0, 0, 0)
        self.orbit1 = orbits.Orbit(self.central_body, apo=1000, per=1000)
        self.orbit2 = orbits.Orbit(self.central_body, apo=2000, per=2000)

        self.testcase = TestBaseManoeuvre.ConcreteManoeuvre(self.orbit1, self.orbit2, 555)

    def test_constructor(self):
        self.assertEqual(len(self.orbit1.manoeuvres), 1,
                         "BaseManoeuvre constructor should add self to orbit1.manoeuvres.")

        self.assertEqual(len(self.orbit2.manoeuvres), 1,
                         "BaseManoeuvre constructor should add self to orbit2.manoeuvres.")

        self.assertEqual(5550, self.testcase.dv,
                         """BaseManoeuvre constructor should pass insect_r to
_delta_v() that's implemented by subclass to compute Delta-V.""")

    def test_get_other(self):
        self.assertEqual(self.testcase.get_other(self.orbit1), self.orbit2,
                         "BaseManoeuvre.get_other() should return orbit2 when passed orbit1.")

        self.assertEqual(self.testcase.get_other(self.orbit2), self.orbit1,
                         "BaseManoeuvre.get_other() should return orbit1 when passed orbit2.")


class TestProRetroGradeManoeuvre(TestCase):

    def setUp(self):
        self.earth = bodies.CentralBody(5.972E24,
                                        6371000,
                                        200000,
                                        3.986004418E14)

    def test__delta_v(self):
        orbit_1 = orbits.Orbit(self.earth,
                               a=6531000,
                               e=0,
                               i=0)

        orbit_2 = orbits.Orbit(self.earth,
                               apo=255254440,
                               per=6531000,
                               i=0)

        manoeuvre = manoeuvres.ProRetroGradeManoeuvre(orbit_1, orbit_2, 6531000)

        self.assertAlmostEqual(manoeuvre.dv, 3097.2756082,
                               msg="""ProRetroGradeManoeuvre should be able to calculate Delta-V through
speed difference of orbits using vis-viva equation.""")

    def test_evaluate(self):
        orbit_1_testcase_1 = orbits.Orbit(self.earth,
                                          apo=10000,
                                          per=10000,
                                          i=60)

        orbit_2_testcase_1 = orbits.Orbit(self.earth,
                                          apo=20000,
                                          per=10000,
                                          i=60)

        self.assertTrue(manoeuvres.ProRetroGradeManoeuvre.evaluate(orbit_1_testcase_1,
                                                                   orbit_2_testcase_1),
                        msg="ProRetroGradeManoeuvre should evaluate as possible between 2 orbits"
                            "that share an apside and inclination.")

        orbit_1_testcase_2 = orbits.Orbit(self.earth,
                                          apo=10000,
                                          per=10000,
                                          i=0)

        orbit_2_testcase_2 = orbits.Orbit(self.earth,
                                          apo=20000,
                                          per=10000,
                                          i=60)

        self.assertFalse(manoeuvres.ProRetroGradeManoeuvre.evaluate(orbit_1_testcase_2,
                                                                    orbit_2_testcase_2),
                         msg="ProRetroGradeManoeuvre should evaluate as impossible between 2 orbits"
                            "that share an apside, but don't share their inclination.")

        orbit_1_testcase_3 = orbits.Orbit(self.earth,
                                          apo=10000,
                                          per=10000,
                                          i=60)

        orbit_2_testcase_3 = orbits.Orbit(self.earth,
                                          apo=20000,
                                          per=20000,
                                          i=60)

        self.assertFalse(manoeuvres.ProRetroGradeManoeuvre.evaluate(orbit_1_testcase_3,
                                                                    orbit_2_testcase_3),
                         msg="ProRetroGradeManoeuvre should evaluate as impossible between 2 orbits"
                             "that share their inclination but don't share an apside.")


class TestInclinationChange(TestCase):

    def setUp(self):
        self.earth = bodies.CentralBody(5.972E24,
                                        6371000,
                                        200000,
                                        3.986004418E14)

    def test__delta_v(self):
        orbit_1 = orbits.Orbit(self.earth,
                               a=6531000,
                               e=0,
                               i=0)

        orbit_2 = orbits.Orbit(self.earth,
                               a=6531000,
                               e=0,
                               i=60)

        manoeuvre = manoeuvres.InclinationChange(orbit_1, orbit_2, 6531000)

        self.assertAlmostEqual(manoeuvre.dv, orbit_1.v_at(6531000),
                               msg="""InclinationChange should be able to calculate Delta-V through cosine_rule
and speed difference calculated through vis-viva equation.""")

    def test_evaluate(self):
        orbit_1_testcase_1 = orbits.Orbit(self.earth,
                                          apo=15000,
                                          per=25000,
                                          i=0)

        orbit_2_testcase_1 = orbits.Orbit(self.earth,
                                          apo=15000,
                                          per=25000,
                                          i=40)

        self.assertTrue(manoeuvres.InclinationChange.evaluate(orbit_1_testcase_1, orbit_2_testcase_1),
                        msg="InclinationChange should evaluate to True between orbits that share all their apsides."
                            " but have different inclination.")

        orbit_1_testcase_2 = orbits.Orbit(self.earth,
                                          apo=15000,
                                          per=25000,
                                          i=0)

        orbit_2_testcase_2 = orbits.Orbit(self.earth,
                                          apo=15000,
                                          per=25000,
                                          i=0)

        self.assertFalse(manoeuvres.InclinationChange.evaluate(orbit_1_testcase_2, orbit_2_testcase_2),
                         msg="InclinationChange should evaluate to False between orbits that share all their apsides."
                             " and their inclination.")

        orbit_1_testcase_3 = orbits.Orbit(self.earth,
                                          apo=15000,
                                          per=25000,
                                          i=40)

        orbit_2_testcase_3 = orbits.Orbit(self.earth,
                                          apo=20000,
                                          per=30000,
                                          i=0)

        self.assertFalse(manoeuvres.InclinationChange.evaluate(orbit_1_testcase_3, orbit_2_testcase_3),
                         msg="InclinationChange should evaluate to False between orbits that don't share an apside.")


class TestInclinationAndProRetroGradeManoeuvre(TestCase):

    def setUp(self):
        self.earth = bodies.CentralBody(5.972E24,
                                        6371000,
                                        200000,
                                        3.986004418E14)

    def test__delta_v(self):
        orbit_1 = orbits.Orbit(self.earth,
                               apo=1000000,
                               per=1000,
                               i=0)

        orbit_2 = orbits.Orbit(self.earth,
                               a=1000000,
                               e=0,
                               i=60)

        manoeuvre = manoeuvres.InclinationAndProRetroGradeManoeuvre(orbit_1, orbit_2, 1000000)

        self.assertAlmostEqual(manoeuvre.dv, 19534.06764865,
                               msg="""InclinationChangeAndProRetroGradeManoeuvre should be able to calculate
Delta-V through speed difference of orbits using vis-viva equation and cosine-rule.""")

    def test_evaluate(self):
        orbit_1_testcase_1 = orbits.Orbit(self.earth,
                                          apo=50000,
                                          per=10000,
                                          i=30)

        orbit_2_testcase_1 = orbits.Orbit(self.earth,
                                          apo=50000,
                                          per=20000,
                                          i=60)

        self.assertTrue(manoeuvres.InclinationAndProRetroGradeManoeuvre.evaluate(orbit_1_testcase_1,
                                                                                 orbit_2_testcase_1),
                        msg="InclinationAndProRetroGradeManoeuvre should evaluate to True for orbits that share"
                            " an apside, and don't share their inclination.")

        orbit_1_testcase_2 = orbits.Orbit(self.earth,
                                          apo=50000,
                                          per=10000,
                                          i=30)

        orbit_2_testcase_2 = orbits.Orbit(self.earth,
                                          apo=50000,
                                          per=20000,
                                          i=30)

        self.assertFalse(manoeuvres.InclinationAndProRetroGradeManoeuvre.evaluate(orbit_1_testcase_2,
                                                                                  orbit_2_testcase_2),
                         msg="InclinationAndProRetroGradeManoeuvre should evaluate to False for orbits that share"
                             " their inclination.")

        orbit_1_testcase_3 = orbits.Orbit(self.earth,
                                          apo=40000,
                                          per=10000,
                                          i=60)

        orbit_2_testcase_3 = orbits.Orbit(self.earth,
                                          apo=50000,
                                          per=20000,
                                          i=30)

        self.assertFalse(manoeuvres.InclinationAndProRetroGradeManoeuvre.evaluate(orbit_1_testcase_2,
                                                                                  orbit_2_testcase_2),
                         msg="InclinationAndProRetroGradeManoeuvre should evaluate to False for orbits that"
                             " don't share an apside.")