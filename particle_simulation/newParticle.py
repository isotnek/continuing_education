import numpy as np

# Particle Factory for easy creation
class ParticleFactory:
    @staticmethod
    def create_particles(particle_type, n, *args, **kwargs):
        """
        Create `n` particles of a specified type

        Example:
        some_particle = ParticleFactory.create_particles(Particle, 
        5, # Number of particles
        100, # Starting X position
        100, # Starting Y position
        5, # Initial x velocity 
        5, # Initial y velocity
        10, # Mass of the particle
        10, # Radius of the particle
        (255, 0, 0)) # RGB color of the particle

        """
        return [particle_type(*args, **kwargs) for _ in range(n)]

# Base Particle Class
class Particle:
    """A class representing a 2D particle"""
    def __init__(self, x, y, vx, vy, mass, radius=10, color=(255, 255, 255)):
        self.position = np.array((float(x), float(y)))
        self.velocity = np.array((float(vx), float(vy)))
        self.mass = mass
        self.radius = radius
        self.color = color

        # TODO add atttraction and repulsion radii and attraction / repulsion forces

    @property
    def x(self):
        return self.position[0]

    @x.setter
    def x(self, value):
        self.position[0] = value

    @property
    def y(self):
        return self.position[1]

    @y.setter
    def y(self, value):
        self.position[1] = value

    @property
    def vx(self):
        return self.velocity[0]

    @vx.setter
    def vx(self, value):
        self.velocity[0] = value

    @property
    def vy(self):
        return self.velocity[1]

    @vy.setter
    def vy(self, value):
        self.velocity[1] = value

    def update_position(self, dt):
        self.position += self.velocity * dt
    
    def edge_collision(self, width, height):
        """Handle collisions with the edges of the screen."""
        if self.x - self.radius <= 0 or self.x + self.radius >= width:
            self.vx = -self.vx

        if self.y - self.radius <= 0 or self.y + self.radius >= height:
            self.vy = -self.vy
    
    def particle_collision(self, other):
        """Handle collisions with another particle. Default is elastic collision."""
        collision_vector = self.position - other.position
        distance = np.linalg.norm(collision_vector)

        # Check for collision and ensure distance is not too small
        if distance < self.radius + other.radius and distance > 1e-8:
            
            # Normalized direction vector
            normal_vector = collision_vector / distance
            tangent_vector = np.array([-normal_vector[1], normal_vector[0]])  # Rotate n by 90 degrees to get tangent vector

            # Resolve velocities into normal and tangent components
            v1n = np.dot(self.velocity, normal_vector)
            v1t = np.dot(self.velocity, tangent_vector)
            v2n = np.dot(other.velocity, normal_vector)
            v2t = np.dot(other.velocity, tangent_vector)

            # Calculate new normal velocities
            v1n_prime = (v1n * (self.mass - other.mass) + 2 * other.mass * v2n) / (self.mass + other.mass)
            v2n_prime = (v2n * (other.mass - self.mass) + 2 * self.mass * v1n) / (self.mass + other.mass)

            # Combine to get final velocities
            self.velocity = v1n_prime * normal_vector + v1t * tangent_vector
            other.velocity = v2n_prime * normal_vector + v2t * tangent_vector
            
# Example of Extended Particle Class
class ChargedParticle(Particle):
    def __init__(self, x, y, vx, vy, mass, charge, radius=10, color=(255, 255, 255)):
        super().__init__(x, y, vx, vy, mass, radius, color)
        self.charge = charge

# TODO lambda parameter for simulation class that allows a user the ability to pass in some function defining inter-particle dynamics
# Support modeling these dynamics with a Pandas df with coefficients of attraction / repulsion