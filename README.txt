Authors:
- Anton Makasevych
- Ian Caruana


HOW TO USE THE PROGRAM
------------------------------------------
The program can be run in two ways:

1) Using the Menu Interface (suggested):
   - Launch the `menu.py` script to customize and start the Monte Carlo Localization simulation.
   - Command: python menu.py
   - This mode allows you to set:
     - Number of landmarks.
     - Motion noise (float).
     - Sensor noise (float).

2) Directly Running the Simulation:
   - Run `game.py` with predefined parameters.
   - Command: python game.py
   - Modify `main(num_landmarks, motion, sensor)` in `game.py` to set your desired parameters.

CONTROLS IN THE SIMULATION
------------------------------------------
- Movement:
  - Arrow keys or `W`, `A`, `S`, `D` to move the robot.
- Quit:
  - Close the simulation window to exit.

IMPLEMENTATION DETAILS
------------------------------------------
Language Used: Python
External Libraries:
- `pygame`: For graphical visualization.
- `numpy`: For numerical calculations.
- `random`: For generating random values.

The ZIP includes:
1) game.py       - Core Monte Carlo Localization simulation.
2) menu.py       - Menu interface for customizing simulation parameters.
3) README.txt    - Documentation explaining the implementation.

BRIEF SOURCE CODE EXPLANATION
------------------------------------------
1) game.py:
   - Implements Monte Carlo Localization using a particle filter.
   - Key Functions:
     - `motion_model`: Updates particle positions based on robot motion.
     - `measurement_model`: Adjusts particle weights based on distance from robot to each landmark
     - `resample_particles`: Resamples particles proportional to their weights.
     - `draw_*`: Functions for visualizing the robot, particles, landmarks, and LIDAR beams.

   - Visualization:
     - Robot: Red circle.
     - Particles: Green dots.
     - Landmarks: Blue circles.
     - LIDAR Beams: Black lines.

2) menu.py:
   - Provides a graphical interface for customizing simulation parameters.
   - Key Features:
     - Input boxes for setting the number of landmarks, motion noise, and sensor noise.
     - Buttons for starting the simulation and quitting the application.

HOW THE PARTICLE FILTER WORKS
------------------------------------------
Monte Carlo Localization (MCL) Steps:
1) Prediction:
   - Move particles based on robot's motion with added random noise.
2) Measurement Update:
   - Compute weights for each particle based on sensor measurements.
3) Resampling:
   - Resample particles based on their weights to retain high-probability particles.

VISUALIZATION ELEMENTS:
- Landmarks:
  - Blue circles randomly distributed in the environment.
- Robot:
  - Red circle representing the actual position.
- Particles:
  - Green dots representing the estimated positions.
- LIDAR Beams:
  - Black lines visualizing simulated distance measurements from the robot to landmarks.
  - Note: These are for visual representation only and do not influence the algorithm, which uses Euclidean distance for sensor readings.


REFERENCES
------------------------------------------
1) Evaluation error inspired by:
   https://fjp.at/posts/localization/mcl/
2) Pygame usage tutorials:
   https://www.pygame.org/docs/
3) Python and NumPy documentation:
   https://numpy.org/doc/
