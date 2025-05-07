# Control Systems Code Overview

## [`PID.py`](PID.py)
This file implements a cruise control simulation using a PID controller. It demonstrates how PID control can maintain a vehicle's speed despite external disturbances.

### Key Components:

#### Car Class
- Models a vehicle with realistic physics including mass and aerodynamic drag
- Parameters: mass (1500kg), drag coefficient (0.3), frontal area (2.2m²)
- Uses physics equations to calculate speed changes based on applied forces
- Includes drag force calculation: `F_drag = 0.5 * Cd * A * ρ * v²`

#### PIDController Class
- Implements classical PID control algorithm
- Three control components:
  - **Proportional (P)**: Responds to current error (difference between target and actual speed)
  - **Integral (I)**: Accumulates error over time to eliminate steady-state error
  - **Derivative (D)**: Responds to rate of change of error to reduce overshoot
- Stores individual P, I, and D terms for analysis
- Configurable gains (Kp, Ki, Kd) to tune controller behavior

#### Simulation Functions
- `run_simulation()`: Executes time-step simulation of the car with PID controller
- Includes wind disturbance simulation to test controller robustness
- Records speed, control output, and individual PID components for analysis

#### Visualization
- `plot_results()`: Creates a three-panel visualization:
  1. Car speed vs. target speed
  2. Control force output
  3. Individual P, I, and D component contributions

#### Default Configuration
- Controller parameters: Kp=700, Ki=300, Kd=1200
- Target speed: 10 km/h
- Simulation time: 100 seconds with 0.001s time steps
- Wind disturbance: Constant -200N headwind

### How It Works:
1. At each time step, the controller calculates the error between desired and actual speed
2. The PID algorithm computes the appropriate control force based on this error
3. This force is applied to the car, updating its speed according to physics
4. External disturbances (wind) can be added to test the controller's robustness
5. The control loop continues, constantly adjusting the force to maintain target speed

## [`state_space.py`](state_space.py)
This file implements a state space control model for dynamic systems. It represents a more comprehensive approach to modeling and controlling complex systems compared to PID control.

### Key Components:

#### StateSpaceSystem Class
- Models a dynamic system using state space representation (x' = Ax + Bu, y = Cx + Du)
- Supports both continuous and discrete-time systems
- Parameters: system matrices A, B, C, D defining system dynamics
- Includes methods for system analysis (stability, controllability, observability)
- Handles MIMO (Multiple-Input, Multiple-Output) systems naturally

#### StateSpaceController Class
- Implements full state feedback control law (u = -Kx + Nr)
- Includes state observer/estimator for systems with limited sensor measurements
- Supports pole placement for desired closed-loop dynamics
- Implements LQR (Linear Quadratic Regulator) for optimal control
- Provides reference tracking and disturbance rejection capabilities

#### Simulation Functions
- `simulate_system()`: Executes time-domain simulation of the controlled system
- Supports different input types (step, ramp, sinusoidal, custom)
- Handles process and measurement noise for realistic simulations
- Records state trajectories, control inputs, and outputs for analysis

#### Analysis Tools
- `system_analysis()`: Computes eigenvalues, transfer functions, and frequency responses
- `plot_response()`: Creates multi-panel visualizations of system behavior:
  1. State trajectories over time
  2. Control inputs and their magnitudes
  3. System outputs compared to reference signals
  4. Frequency domain characteristics (Bode, Nyquist plots)

#### Default Configuration
- Example system: second-order mechanical system (mass-spring-damper)
- Controller: LQR with customizable weighting matrices
- Simulation time: 10 seconds with adjustable step size
- Includes process noise and sensor noise models

### How It Works:
1. The system is defined by its state space matrices (A, B, C, D)
2. The controller design determines feedback gain matrix K based on design objectives
3. At each time step, the controller computes control inputs based on current (or estimated) state
4. The system state evolves according to the state differential equations
5. Advanced techniques like observers compensate for unmeasured states
6. The control loop maintains stability while achieving performance objectives
