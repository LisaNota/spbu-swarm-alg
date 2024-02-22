# Swarm Intelligence Algorithm Implementation

## Project Objective:
The objective of this project is to investigate the characteristics of swarm intelligence algorithms for solving global optimization problems and compare them with genetic algorithms.

## Project Components:
The project consists of the following components:

### `Piece` Class:
**Attributes**:
  - `curr_position`: Current position of the particle.
  - `local_best_position`: Best position of the particle.
  - `local_best_fitness`: Best fitness value of the particle.
  - `velocity`: Velocity of the particle.
**Methods**:
  - `init_velocity(swarm)`: Initializes the velocity of the particle.
  - `next_iteration(swarm)`: Moves the particle to the next position.
  
### `Swarm` Class:
**Attributes**:
  - `swarmsize`: Size of the swarm.
  - `minvalues`, `maxvalues`: Lower and upper bounds for search.
  - `curr_velocity_ratio`, `local_velocity_ratio`, `global_velocity_ratio`: Coefficients for velocity calculations.
  - `global_best_fitness`: Best fitness value found by the swarm.
  - `global_best_position`: Best position found by the swarm.
**Methods**:
  - `create_swarm()`: Creates the swarm of particles.
  - `next_iteration()`: Moves each particle in the swarm.
  - `final_finc(position)`: Target function to minimize.
  - `get_final_finc(position)`: Determines the best position and fitness value of a particle.

### User Interface:
The user interface is implemented using Tkinter and matplotlib, providing options to set parameters for the swarm algorithm and visualize the movement of particles.

## Usage:
1. Set the parameters in the GUI, including coefficients for velocity calculation and the number of particles.
2. Click on the "Create Particles" button to initialize the swarm.
3. Adjust the number of iterations using the spinbox or predefined buttons.
4. Click on the "Calculate" button to perform iterations and visualize the movement of particles.
5. The best solution found by the swarm and its fitness value will be displayed in the interface.

## Dependencies:
- Python 3.x
- NumPy
- Tkinter (standard Python library)
- Matplotlib

## How to Run:
- Ensure Python 3.x and the required dependencies are installed.
- Run the Python script `swarm_intelligence.py`.
- Adjust the parameters as needed in the GUI and click on the buttons to run the algorithm.
