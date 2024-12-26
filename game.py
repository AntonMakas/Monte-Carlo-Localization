import pygame
import numpy as np
import random

pygame.init()

WIDTH, HEIGHT = 800, 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Monte Carlo Localization")

robot_pos = np.array([WIDTH // 2, HEIGHT // 2])
robot_speed = 5

# Particle filter parameters
num_particles = 1000
particles = np.array([np.array([random.uniform(0, WIDTH), random.uniform(0, HEIGHT)]) for _ in range(num_particles)])
weights = np.ones(num_particles) / num_particles

def draw_robot(position):
    pygame.draw.circle(screen, RED, position.astype(int), 10)

def draw_landmarks():
    for lm in landmarks:
        pygame.draw.circle(screen, BLUE, lm, 5)

def draw_particles(particles):
    for p in particles:
        pygame.draw.circle(screen, GREEN, p.astype(int), 5)

def draw_lidar_sensors(robot_position, landmarks, num_beams=15, beam_length=200):
    angle_step = 360 / num_beams
    for i in range(num_beams):
        angle = np.radians(i * angle_step)
        end_x = robot_position[0] + beam_length * np.cos(angle)
        end_y = robot_position[1] + beam_length * np.sin(angle)
        closest_distance = beam_length
        closest_point = None

        for lm in landmarks:
            lm_vector = np.array(lm) - robot_position
            lm_distance = np.linalg.norm(lm_vector)
            lm_angle = np.arctan2(lm_vector[1], lm_vector[0])

            if lm_distance <= beam_length and abs(np.sin(lm_angle - angle)) < 0.1:
                if lm_distance < closest_distance:
                    closest_distance = lm_distance
                    closest_point = lm

        if closest_point is not None:
            pygame.draw.line(screen, BLACK, robot_position.astype(int), np.array(closest_point).astype(int), 1)
        else:
            pygame.draw.line(screen, BLACK, robot_position.astype(int), (int(end_x), int(end_y)), 1)

def measure_distances(robot_position, landmarks):
    distances = []
    for lm in landmarks:
        distance = np.linalg.norm(robot_position - np.array(lm))
        distances.append(distance)
    return distances

def motion_model(particles, dx, dy):
    noise = np.random.normal(0, motion_noise, particles.shape)
    particles += np.array([dx, dy]) + noise
    particles[:, 0] = np.clip(particles[:, 0], 0, WIDTH)
    particles[:, 1] = np.clip(particles[:, 1], 0, HEIGHT)
    return particles

def measurement_model(particles, landmarks, robot_distances):
    weights = np.ones(len(particles))
    for i, particle in enumerate(particles):
        particle_distances = measure_distances(particle, landmarks)
        weight = 1.0
        for pd, rd in zip(particle_distances, robot_distances):
            weight *= np.exp(-((pd - rd) ** 2) / (2 * sensor_noise ** 2))
        weights[i] = weight
    weights += 1e-300  # Avoid division by zero
    weights /= sum(weights)
    return weights

def resample_particles(particles, weights):
    indices = np.random.choice(range(len(particles)), size=len(particles), p=weights)
    return particles[indices]

def main(num_landmarks, motion, sensor):
    global robot_pos, particles, weights, landmarks, motion_noise, sensor_noise

    motion_noise = motion
    sensor_noise = sensor
    landmarks = [(np.random.randint(50, WIDTH - 50), np.random.randint(50, HEIGHT - 50)) for _ in range(num_landmarks)]

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -robot_speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = robot_speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -robot_speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = robot_speed


        # Move robot and particles
        robot_pos += np.array([dx, dy])

        # Ensure robot stays within bounds
        robot_pos[0] = np.clip(robot_pos[0], 0, WIDTH)
        robot_pos[1] = np.clip(robot_pos[1], 0, HEIGHT)

        particles = motion_model(particles, dx, dy)

        # Measure distances to landmarks
        robot_distances = measure_distances(robot_pos, landmarks)

        # Update weights based on measurements
        weights = measurement_model(particles, landmarks, robot_distances)

        # Resample particles
        particles = resample_particles(particles, weights)

        # Draw elements
        draw_landmarks()
        draw_particles(particles)
        draw_robot(robot_pos)
        draw_lidar_sensors(robot_pos, landmarks)

        # Update display
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()