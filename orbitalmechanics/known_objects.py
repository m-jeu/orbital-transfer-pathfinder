#
# Simple script to initialize some objects like planets, stars, moons and orbits
# to make life easier for the end user.
#

import orbitalmechanics.bodies as bodies
import orbitalmechanics.orbits as orbits


# Solar system bodies.
sun = bodies.CentralBody(1.989E30,
                         696349999,
                         mu=1.32712440018E20)

earth = bodies.CentralBodyInOrbit(5.9736E24,
                                  6371000,
                                  160000,
                                  3.986004418E14,
                                  orbits.Orbit(sun,
                                               a=149598023000,
                                               e=0.0167086,
                                               i=7))

moon = bodies.CentralBodyInOrbit(7.34767309E22,
                                 1737400,
                                 mu=4.9048695E12,
                                 orbit=orbits.Orbit(earth,
                                                    apo=405400000,
                                                    per=363228900,
                                                    i=5))

# Bodies in the fictional world of Kerbal Space Program.
kerbol = bodies.CentralBody(1.7565459E28,
                            261600000,
                            mu=1.1723328E18)

kerbin = bodies.CentralBodyInOrbit(5.2915158E22,
                                   600000,
                                   70000,
                                   3.5316000E12,
                                   orbits.Orbit(kerbol,
                                                apo=13599840256,
                                                per=13599840256))

mun = bodies.CentralBodyInOrbit(9.7599066E20,
                                200000,
                                mu=6.5138398E10,
                                orbit=orbits.Orbit(kerbin,
                                                   a=12000000,
                                                   e=0))

minmus = bodies.CentralBodyInOrbit(2.6457580E19,
                                   60000,
                                   mu=1.7658000E9,
                                   orbit=orbits.Orbit(kerbin,
                                                      a=47000000,
                                                      e=0,
                                                      i=6))