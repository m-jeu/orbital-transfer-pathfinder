A package capable of handling a wide variety of orbital mechanics problems, specifically designed for the
use-case of finding efficient flight plans through 2-body systems.

This package abstracts from reality to limit project scope by implementing a limited amount
of Keplerian elements for orbits. For many real-world problems, like finding good approaches to drastic
inclination-changes, these will be enough. Currently, the following Keplerian elements are implemented:
1. Semi-major axis.
2. Eccentricity.
3. Inclination.

**Dependencies:**

1. loadingbar package for visualising manoeuvre generation progress.
2. shortpathfinding package for actually finding efficient flight-plans.
