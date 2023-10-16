import numpy as np
import pygame

# Particle Factory for easy creation
class ParticleFactory:
    @staticmethod
    def create_particles(particle_type, n, *args, **kwargs):
        """Create `n` particles of a specified type"""
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
        r = self.position - other.position
        distance = np.linalg.norm(r)

        # Check for collision and ensure distance is not too small
        if distance < self.radius + other.radius and distance > 1e-8:
            # Normalized direction vector
            n = r / distance

            # Compute velocities along the direction of collision
            v1n = np.dot(self.velocity, n)
            v2n = np.dot(other.velocity, n)

            # Compute the impulse due to collision
            impulse = (2 * other.mass * v2n - 2 * self.mass * v1n) / (self.mass + other.mass)

            # Update velocities based on the impulse
            self.velocity = self.velocity + (impulse * n)
            other.velocity = other.velocity - (impulse * n)

# Example of Extended Particle Class
class ChargedParticle(Particle):
    def __init__(self, x, y, vx, vy, mass, charge, radius=10, color=(255, 255, 255)):
        super().__init__(x, y, vx, vy, mass, radius, color)
        self.charge = charge

# System Dynamics
class SystemDynamics:
    @staticmethod
    def gravitational_force(p1, p2, G=6.67430e-11):
        r_vector = p2.position - p1.position
        distance = np.linalg.norm(r_vector)
        force_magnitude = G * (p1.mass * p2.mass) / (distance ** 2)
        force_direction = r_vector / distance
        return force_direction * force_magnitude

    @staticmethod
    def electromagnetic_force(p1, p2, k=8.9875e9):  # Assuming p1 and p2 are ChargedParticles
        r_vector = p2.position - p1.position
        distance = np.linalg.norm(r_vector)
        force_magnitude = k * (p1.charge * p2.charge) / (distance ** 2)
        force_direction = r_vector / distance
        return force_direction * force_magnitude

# Particle Simulation with pygame
class ParticleSimulation:
    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Particle Simulator')
        self.particles = []
        self.width = width
        self.height = height

    def add_particles(self, particle_list):
        self.particles.extend(particle_list)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((0, 0, 0))
            
            # Update positions and check for collisions
            for particle in self.particles:
                particle.update_position(1)
                particle.edge_collision(self.width, self.height)
                for other_particle in self.particles:
                    if particle != other_particle:
                        particle.particle_collision(other_particle)

                pygame.draw.circle(self.screen, particle.color, (int(particle.x), int(particle.y)), particle.radius)

            pygame.display.flip()

# Example Usage:
sim = ParticleSimulation(800, 600)

# Create 5 red and 5 blue particles
red_particles = ParticleFactory.create_particles(Particle, 1, 0, 0, 0, 0, 0, 10, (255, 0, 0))
#blue_particles = ParticleFactory.create_particles(Particle, 5, 400, 400, -5, -5, 10, 10, (0, 0, 255))

sim.add_particles(red_particles)
#sim.add_particles(blue_particles)

sim.run()
