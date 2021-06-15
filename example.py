import orbitalmechanics.bodies as bodies
import orbitalmechanics.orbits as orbits
import orbitalmechanics.manoeuvres as manoeuvres
import orbitalmechanics.orbitscollections as orbitcollections


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
    leo = orbits.Orbit(earth, a=earth.add_radius(200000), e=0)
    gto = orbits.Orbit(earth, a=24367500, e=0.730337539)
    geo = orbits.Orbit(earth, a=42164000, e=0)

    m1 = manoeuvres.ProRetroGradeManoeuvre(leo, gto, manoeuvres.ProRetroGradeManoeuvre.evaluate(leo, gto))
    m2 = manoeuvres.ProRetroGradeManoeuvre(gto, geo, manoeuvres.ProRetroGradeManoeuvre.evaluate(gto, geo))

    print("200km LEO -> GTO -> GEO costs approx:")
    print(f"{m1.dv + m2.dv} Delta-V.")

    possible_orbits = orbitcollections.OrbitCollection(earth, [manoeuvres.ProRetroGradeManoeuvre])

    possible_orbits.create_orbits(100, [150000, 20000000])

    possible_orbits.compute_all_manoeuvres()