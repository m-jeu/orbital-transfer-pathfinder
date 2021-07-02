#
# Simple script to initialize some objects like planets, stars, moons and orbits
# to make life easier for the end user.
#

import orbital_transfer_pathfinder.lib.orbitalmechanics.bodies as bodies
import orbital_transfer_pathfinder.lib.orbitalmechanics.orbits as orbits


# Real world bodies.
sun = bodies.CentralBody(1.989E30,
                         696349999,
                         mu=1.32712440018E20)

earth = bodies.CentralBodyInOrbit(5.9736E24,
                                  6371000,
                                  orbits.Orbit(sun,
                                               a=149598023000,
                                               e=0.0167086,
                                               i=7),
                                  160000,
                                  3.986004418E14)

moon = bodies.CentralBodyInOrbit(7.34767309E22,
                                 1737400,
                                 mu=4.9048695E12,
                                 orbit=orbits.Orbit(earth,
                                                    apo=405400000,
                                                    per=363228900,
                                                    i=5))

# Real world orbits. Based on estimates.
iss = orbits.Orbit(earth,
                   per=earth.add_radius(418000),
                   apo=earth.add_radius(422000),
                   i=52)

geo = orbits.Orbit(earth,
                   a=42164000,
                   e=0,
                   i=0)

ksc_standard_parking = orbits.Orbit(earth,
                                    a=earth.add_radius(200000),
                                    e=0,
                                    i=28)

baikonur_standard_parking = orbits.Orbit(earth,
                                         a=earth.add_radius(200000),
                                         e=0,
                                         i=49)

equatorial_leo = orbits.Orbit(earth,
                              a=earth.add_radius(200000),
                              e=0,
                              i=0)

low_sun_synchronous = orbits.Orbit(earth,
                                   a=earth.add_radius(274000),
                                   e=0,
                                   i=97)



# Bodies in the fictional world of Kerbal Space Program.
kerbol = bodies.CentralBody(1.7565459E28,
                            261600000,
                            mu=1.1723328E18)

kerbin = bodies.CentralBodyInOrbit(5.2915158E22,
                                   600000,
                                   orbits.Orbit(kerbol,
                                                apo=13599840256,
                                                per=13599840256),
                                   70000,
                                   3.5316000E12)

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


# Convenience dictionaries for CLI.

celestial_bodies = {"Sun": sun,
                    "Earth": earth,
                    "Moon": moon,
                    "Kerbol": kerbol,
                    "Kerbin": kerbin,
                    "Mun": mun,
                    "Minmus": minmus}

known_orbits = {"ISS": iss,
                "GEO": geo,
                "KSC_Parking": ksc_standard_parking,
                "Baikonur_Parking": baikonur_standard_parking,
                "Sun_synchronous": low_sun_synchronous,
                "Leo_Equatorial": equatorial_leo}