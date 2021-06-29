import orbital_transfer_pathfinder.lib.orbitalmechanics.orbits as orbits
import orbital_transfer_pathfinder.lib.orbitalmechanics.manoeuvres as manoeuvres
import orbital_transfer_pathfinder.lib.orbitalmechanics.orbitcollections as orbitcollections

import orbital_transfer_pathfinder.lib.orbitalmechanics.known_objects as known_objects

import orbital_transfer_pathfinder.lib.shortpathfinding as shortpathfinding

import datetime


if __name__ == "__main__":
    leo = orbits.Orbit(known_objects.earth, a=known_objects.earth.add_radius(200000), e=0, i=28)
    geo = orbits.Orbit(known_objects.earth, a=42164000, e=0)

    possible_orbits = orbitcollections.OrbitCollection(known_objects.earth,
                                                       [manoeuvres.InclinationChange,
                                                        manoeuvres.InclinationAndProRetroGradeManoeuvre,
                                                        manoeuvres.ProRetroGradeManoeuvre])

    print(f"Start orbit generation: {datetime.datetime.now().strftime('%H:%M:%S')}")

    possible_orbits.add_orbit(leo)
    possible_orbits.add_orbit(geo)

    possible_orbits.create_orbits(5, [known_objects.earth.add_radius(150000),
                                      known_objects.earth.add_radius(20000000)], 5)

    print(f"Finish orbit generation: {datetime.datetime.now().strftime('%H:%M:%S')}")

    possible_orbits.compute_all_manoeuvres(True)

    print(f"Finish manoeuvre generation: {datetime.datetime.now().strftime('%H:%M:%S')}")

    print(f"Find shortest path from orbits[0] to orbits[450]: {datetime.datetime.now().strftime('%H:%M:%S')}")

    dijkstra_graph = shortpathfinding.custom_dijkstras_algorithm.CDijkstraGraph(list(possible_orbits.orbits))

    dist, path = dijkstra_graph.find_shortest_path(leo, geo, True)


    print(f"Found shortest path: {datetime.datetime.now().strftime('%H:%M:%S')}")
    print(f"Distance: {dist} m/s Delta-V")
    print(f"Start: {leo}")
    print(f"Target: {geo}")
    for m in path:
        print(m)