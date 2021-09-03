import orbital_transfer_pathfinder


def pick_from_choices(choices: dict[str: object]) -> object:
    """Make a user pick an option out of a dictionary with strings as keys through keyboard input.

    Args:
        choices: the user's choices.

    Returns:
        whatever choice the user made."""
    print("Available choices:")
    for count, key in enumerate(choices.keys()):
        print(f"{count}: '{key}'")
    while ((user_input := input("Enter your choice:")) not in choices):
        print("Invalid choice.")
    return choices[user_input]


if __name__ == "__main__":
    print("WARNING: Orbit generation around any other body then earth currently not implemented.")
    print("Pick a central body:")
    central_body = pick_from_choices(orbital_transfer_pathfinder.celestial_bodies)

    if central_body != orbital_transfer_pathfinder.celestial_bodies["Earth"]:  # FIXME(m-jeu): Actually implement proper CLI
        raise NotImplementedError

    print("Pick a start orbit:")
    start_orbit = pick_from_choices(orbital_transfer_pathfinder.known_orbits)

    print("Pick a target orbit:")
    target_orbit = pick_from_choices(orbital_transfer_pathfinder.known_orbits)

    print("Pick precision:")
    permutations_per_section = pick_from_choices({"Low": 5,  # For 8gb of ram.
                                                  "High": 10})  # For 16gb of ram.

    print("Configuring orbits & manoeuvres.")

    orbits_collection = orbital_transfer_pathfinder.OrbitCollection(central_body,
                                                                    [orbital_transfer_pathfinder.ProRetroGradeManoeuvre,
                                                                     orbital_transfer_pathfinder.InclinationChange,
                                                                     orbital_transfer_pathfinder.InclinationAndProRetroGradeManoeuvre])

    orbits_collection.add_orbit(start_orbit)
    orbits_collection.add_orbit(target_orbit)

    orbits_collection.create_orbits(permutations_per_section,
                                    [orbital_transfer_pathfinder.earth.add_radius(150000),  # These numbers are specific to earth.
                                     orbital_transfer_pathfinder.earth.add_radius(20000000)],
                                    inclination_increment=5)

    orbits_collection.compute_all_manoeuvres(True)

    print("Looking for shortest path.")

    graph = orbital_transfer_pathfinder.CDijkstraGraph(list(orbits_collection.orbits))

    distance, path, nodes = graph.find_shortest_path(start_orbit, target_orbit, True)

    print(f"\nFound plan for {distance} m/s Delta-V:")
    print(f"Start: {start_orbit}.")
    print(f"Target: {target_orbit}.")
    print("Path:")
    for i in range(len(path)):
        print(nodes[i])
        print(path[i])
    print(nodes[-1])

    orbital_transfer_pathfinder.visualize_orbits(nodes)
