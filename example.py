import orbitalmechanics.bodies as bodies
import orbitalmechanics.orbits as orbits
import orbitalmechanics.manoeuvres as manoeuvres
import orbitalmechanics.orbitcollections as orbitcollections
import shortpathfinding.dijkstras_algorithm

import datetime


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
the kennedy space center (28 degree inclination) to a geostationary orbit (0 degree inclination)
through a 200km LEO parking orbit.\n""")

    leo = orbits.Orbit(earth, a=earth.add_radius(200000), e=0, i=28)
    gto = orbits.Orbit(earth, a=24367500, e=0.730337539, i=28)
    geo = orbits.Orbit(earth, a=42164000, e=0)

    leo_to_gto = manoeuvres.ProRetroGradeManoeuvre(leo, gto, leo.apsides.intersection(gto.apsides).pop())
    gto_to_geo = manoeuvres.InclinationAndProRetroGradeManoeuvre(gto, geo, gto.apsides.intersection(geo.apsides).pop())

    print(f"Costs approx. {leo_to_gto.dv + gto_to_geo.dv} m/s Delta-V.", end="\n\n")
    # Example of how to compute all orbits in 1 inclination, and all possible manoeuvres between them.
    possible_orbits = orbitcollections.OrbitCollection(earth,
                                                       [manoeuvres.InclinationChange,
                                                        manoeuvres.InclinationAndProRetroGradeManoeuvre,
                                                        manoeuvres.ProRetroGradeManoeuvre])


    print(f"Start orbit generation: {datetime.datetime.now().strftime('%H:%M:%S')}")

    possible_orbits.add_orbit(leo)
    possible_orbits.add_orbit(geo)

    possible_orbits.create_orbits(5, [earth.add_radius(150000), earth.add_radius(20000000)], 5)

    print(f"Finish orbit generation: {datetime.datetime.now().strftime('%H:%M:%S')}")

    possible_orbits.compute_all_manoeuvres(True)

    print(f"Finish manoeuvre generation: {datetime.datetime.now().strftime('%H:%M:%S')}")

    print(f"Find shortest path from orbits[0] to orbits[450]: {datetime.datetime.now().strftime('%H:%M:%S')}")

    dijkstra_graph = shortpathfinding.dijkstras_algorithm.DijkstraGraph(list(possible_orbits.orbits))

    dist, path = dijkstra_graph.find_shortest_path(leo, geo, 5, True)


    print(f"Found shortest path: {datetime.datetime.now().strftime('%H:%M:%S')}")
    print(f"Distance: {dist} m/s Delta-V")
    print(f"Start: {leo}")
    print(f"Target: {geo}")
    for m in path:
        print(m)