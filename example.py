#
# An example script that computes and efficient flight-path from leo to geo.
# Can easily be modified to involve other celestial bodies / orbits / settings.
#


import orbital_transfer_pathfinder

import datetime


if __name__ == "__main__":

    leo = orbital_transfer_pathfinder.Orbit(orbital_transfer_pathfinder.earth,
                                            a=orbital_transfer_pathfinder.earth.add_radius(200000),
                                            e=0, i=28)
    geo = orbital_transfer_pathfinder.Orbit(orbital_transfer_pathfinder.earth, a=42164000, e=0)

    possible_orbits = orbital_transfer_pathfinder.OrbitCollection(orbital_transfer_pathfinder.earth,
                                                                  [orbital_transfer_pathfinder.InclinationChange,
                                                                   orbital_transfer_pathfinder.InclinationAndProRetroGradeManoeuvre,
                                                                   orbital_transfer_pathfinder.ProRetroGradeManoeuvre])

    print(f"Start orbit generation: {datetime.datetime.now().strftime('%H:%M:%S')}")

    possible_orbits.add_orbit(leo)
    possible_orbits.add_orbit(geo)

    #Create orbits at 5 attitudes in low_earth_orbit, 5 in medium_earth_orbit, and 5 in high_earth_orbit.
    possible_orbits.create_orbits(5, [orbital_transfer_pathfinder.earth.add_radius(150000),
                                      orbital_transfer_pathfinder.earth.add_radius(20000000)], 5)

    print(f"Finish orbit generation: {datetime.datetime.now().strftime('%H:%M:%S')}")

    possible_orbits.compute_all_manoeuvres(True)

    print(f"Finish manoeuvre generation: {datetime.datetime.now().strftime('%H:%M:%S')}")

    print(f"Find shortest path from orbits[0] to orbits[450]: {datetime.datetime.now().strftime('%H:%M:%S')}")

    dijkstra_graph = orbital_transfer_pathfinder.custom_dijkstras_algorithm.CDijkstraGraph(list(possible_orbits.orbits))

    dist, res_manoeuvres, res_orbits = dijkstra_graph.find_shortest_path(leo, geo, True)


    print(f"Found shortest path: {datetime.datetime.now().strftime('%H:%M:%S')}")
    print(f"Distance: {dist} m/s Delta-V")
    print(f"Start: {leo}")
    print(f"Target: {geo}")
    for i in range(len(res_orbits)):
        print(res_orbits[i])
        if i < len(res_manoeuvres):
            print(res_manoeuvres[i])

    orbital_transfer_pathfinder.visualize_orbits(res_orbits)