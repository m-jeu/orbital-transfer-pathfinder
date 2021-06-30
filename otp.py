import orbital_transfer_pathfinder.lib.orbitalmechanics.known_objects as known_objects
import orbital_transfer_pathfinder.lib.orbitalmechanics.orbitcollections as orbitcollections
import orbital_transfer_pathfinder.lib.orbitalmechanics.manoeuvres as manoeuvres
import orbital_transfer_pathfinder.lib.shortpathfinding.custom_dijkstras_algorithm as custom_dijkstras_algorithm


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
    central_body = pick_from_choices(known_objects.celestial_bodies)
    start_orbit = pick_from_choices(known_objects.known_orbits)
    target_orbit = pick_from_choices(known_objects.known_orbits)

    print("Configuring orbits & manoeuvres.")

    orbits_collection = orbitcollections.OrbitCollection(central_body,
                                                         [manoeuvres.ProRetroGradeManoeuvre,
                                                          manoeuvres.InclinationChange,
                                                          manoeuvres.InclinationAndProRetroGradeManoeuvre])

    orbits_collection.add_orbit(start_orbit)
    orbits_collection.add_orbit(target_orbit)

    orbits_collection.create_orbits(30, inclination_increment=5)
    orbits_collection.compute_all_manoeuvres(True)

    print("Looking for shortest path.")

    graph = custom_dijkstras_algorithm.CDijkstraGraph(list(orbits_collection.orbits))

    distance, path = graph.find_shortest_path(start_orbit, target_orbit, True)

    print(f"\nFound plan for {distance} m/s Delta-V:")
    print(f"Start: {start_orbit}.")
    print(f"Target: {target_orbit}.")
    print("Path:")
    for manoeuvre in path:
        print(f"  {manoeuvre}.")
