import orbitalmechanics.bodies as bodies
import orbitalmechanics.orbits as orbits
import orbitalmechanics.manoeuvres as manoeuvres
import orbitalmechanics.orbitcollections as orbitcollections


sun = bodies.CentralBody(1.989E30,
                         696349999,
                         0,
                         1.32712440018E20)

earth_orbit = orbits.Orbit(sun,
                           a=149598023000,
                           e=0.0167086)

earth = bodies.CentralBodyInOrbit(5.9736E24,
                                  6371000,
                                  160000,
                                  3.986004418E14,
                                  earth_orbit)

if __name__ == "__main__":
    print("""Below are the calculations for the Delta-V cost of a simple example mission from
the kennedy space center (28 degree inclination) to a geostationary orbit through a 200km LEO parking orbit.\n""")

    leo = orbits.Orbit(earth, a=earth.add_radius(200000), e=0, i=28)
    gto = orbits.Orbit(earth, a=24367500, e=0.730337539, i=28)
    geo = orbits.Orbit(earth, a=42164000, e=0)

    leo_to_gto = manoeuvres.ProRetroGradeManoeuvre(leo, gto, leo.apsides.intersection(gto.apsides).pop())
    gto_to_geo = manoeuvres.InclinationAndProRetroGradeManoeuvre(gto, geo, gto.apsides.intersection(geo.apsides).pop())

    print(f"Costs approx. {leo_to_gto.dv + gto_to_geo.dv} m/s Delta-V.", end="\n\n")

    # Example of how to compute all orbits in 1 inclination, and all possible manoeuvres between them.
    possible_orbits = orbitcollections.OrbitCollection(earth, [manoeuvres.ProRetroGradeManoeuvre])

    possible_orbits.create_orbits(100, [150000, 20000000])

    possible_orbits.compute_all_manoeuvres()
