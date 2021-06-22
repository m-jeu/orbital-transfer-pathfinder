from unittest import TestCase

import orbital_transfer_pathfinder.lib.mmath.math as mmath


class Test(TestCase):
    def test_v_avg(self):
        self.assertEqual(mmath.v_avg(10), 10,
                         "v_avg() should be able to calculate average for 1 parameter.")

        self.assertEqual(mmath.v_avg(5, 10, 15), 10,
                         "v_avg() should be able to calculate average for variable amount of integers.")

        self.assertAlmostEqual(mmath.v_avg(0.2, 0.3), 0.25,
                               "v_avg() should be able to calculate average for floating-point numbers.")

        self.assertEqual(mmath.v_avg(-10, -20), -15,
                         "v_avg() should be able to calculate average for negative numbers.")

    def test_cosine_rule(self):
        self.assertAlmostEqual(mmath.cosine_rule(6.5, 9.4, 131), 14.51827859,
                               msg="""cosine_rule() should be able to get triangle side length based on 2 other sides
                               and angle measured in degrees.""")

        self.assertNotAlmostEqual(mmath.cosine_rule(6.5, 9.4, 2.28638132), 14.51827859,
                                  msg="cosine_rule() should not measure angle_dif in radians.")
