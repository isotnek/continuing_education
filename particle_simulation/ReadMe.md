This repository contains:
  - A simulator, utilizing pygame, for modeling particle interactions
  - A set of helper functions to utilize alongside the simulator

ToDO:
 - generalize particle creation by creating an extensible particle class
 - Generalize the simulator through an extensible simulator class


The particle class will have information about individual particles, or groups of identical particles, such as:
 - mass
 - radius
 - color
 - initial position vector
 - initial velocity vector


The simulator class will have information about both the global state space, as well as rules governing the interaction of particles of the same and different types, such as:
 - Simulation screen size
 - Number and type of particles being modeled
 - Wall collision dynamics
 - Particle collision dynamics
   - Elastic collisions / inelastic collisions
 - Particle attraction and repulsion dynamics
 - Global and local forces (e.g. gravity, curl fields, etc.)
 - Performance optimizations for modeling large numbers of particles