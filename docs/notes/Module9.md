# Feedback Control in Cyber-Physical Systems (CPS)

## Key Components of Feedback Control 

### 1. Plant (System to be Controlled)

**Definition and Role**  
The plant is the physical system or process that we want to control. In CPS, the plant could be anything from a robotic arm, autonomous vehicle, smart building HVAC system, to a chemical process in a manufacturing plant.

**CPS Context**  
- The plant typically has dynamics governed by physics (e.g., mechanical, electrical, thermal).  
- It interacts with the environment and may experience significant external disturbances.  
- In a CPS, the plant’s operational details are often digitized via sensors and fed to a controller.

### 2. Reference Input (Setpoint)

**Definition and Role**  
The reference input, or setpoint, is the desired goal or target state for the plant’s output.

**CPS Context**  
- The reference may be set by a user or a higher-level system.  
- In CPS, references can change dynamically based on context or autonomy.

### 3. Sensor (Measurement System)

**Definition and Role**  
Sensors provide measurements of relevant physical quantities. These are used in feedback loops to estimate system state.

**CPS Context**  
- Sensors convert physical signals into digital data via ADCs.  
- Examples include IMUs, thermocouples, GPS modules, etc.  
- Communication may occur via I2C, SPI, UART, or wireless methods.  
- Sensor data can be noisy or delayed due to hardware/software limitations.

### 4. Controller (Control Algorithm)

**Definition and Role**  
The controller calculates the control signal to drive the plant toward the setpoint based on the error signal.

**CPS Context**  
- Implemented on microcontrollers, SBCs, or FPGAs.  
- Chosen algorithms depend on system complexity, performance, and resource constraints.  
- Controllers may include decision-making or learning components.

### 5. Actuator

**Definition and Role**  
Actuators convert control signals into physical actions.

**CPS Context**  
- Examples: motors, pumps, valves, heaters.  
- Actuated using PWM, DAC, or digital I/O.  
- Interface must be carefully managed to ensure fast, accurate response.

### 6. Error Signal

**Definition and Role**  
The error signal is defined as:

``e(t) = r(t) - y(t)``

Where:
- ``r(t)`` is the reference input
- ``y(t)`` is the measured output

**CPS Context**  
- Drives the control computation.  
- May be scalar or vector-valued in MIMO systems.  
- Computed in real time, possibly across a distributed system.

### 7. Feedback Loop

**Definition and Role**  
A closed-loop system where output measurements influence the input through the controller.

**CPS Context**  
- May span multiple nodes (e.g., cloud-controller with remote sensors).  
- Must consider communication latency and synchronization.  
- Timing guarantees are critical for stability and performance.

### 8. Disturbances and Noise

**Definition and Role**  
Disturbances are unmodeled external inputs; noise is unwanted variability in measurements.

**CPS Context**  
- Sources: environmental factors, communication errors, hardware limitations.  
- Requires robust controller design and filtering (e.g., Kalman filters).

### 9. Computational System

**Definition and Role**  
The digital platform that executes control logic and coordinates sensing/actuation.

**CPS Context**  
- Real-time constraints (e.g., hard deadlines).  
- Implemented on microcontrollers, FPGAs, or distributed cloud systems.  
- Use of real-time OS (e.g., FreeRTOS) to manage scheduling and latency.

## Proportional-Integral-Derivative (PID) Control

PID control is a classical control strategy used to regulate the output of a system to a desired reference (setpoint). It combines three terms—proportional, integral, and derivative—to adjust the control input based on the error between the measured output and the reference.

### 1.1 PID Equation (Continuous Time)

The PID controller output $u(t)$ is defined as:

$$
u(t) = K_p e(t) + K_i \int_{0}^{t} e(\tau)\,d\tau + K_d \frac{d}{dt} e(t),
$$

where:
- $e(t) = r(t) - y(t)$ is the error (the difference between the reference $r(t)$ and the measured output $y(t)$).
- $K_p$ is the proportional gain.
- $K_i$ is the integral gain.
- $K_d$ is the derivative gain.

### 1.2 PID Equation (Discrete Time)

In a digital implementation, the controller calculates values at discrete time steps $ t = nT_s $, where $ T_s $ is the sampling period. A common discrete approximation is:

$$
u[n] = K_p e[n] + K_i T_s \sum_{k=0}^{n} e[k] + K_d \frac{e[n] - e[n-1]}{T_s}.
$$

These integrals and derivatives are approximated numerically. Additional refinements (such as filters on the derivative term) can be applied to improve performance and stability.

---

### 2. Roles of Each Term

Each PID term handles a different aspect of the control action:

### 2.1 Proportional (P)
- **Function**: Produces an output that is directly proportional to the current error $e(t)$.
- **Effect**: A large proportional gain $ K_p $ improves the responsiveness of the system but can cause overshoot and oscillations if set too high.

### 2.2 Integral (I)
- **Function**: Accumulates past error, effectively summing up the area under the error curve over time.
- **Effect**: Helps eliminate steady-state error by increasing the control output until the error is driven to zero. However, excessive integral gain $ K_i $ can lead to slow response and overshoot, and may cause integrator windup.

### 2.3 Derivative (D)
- **Function**: Reacts to the rate of change of the error, effectively predicting the future trend of the error.
- **Effect**: Helps dampen oscillations and anticipate overshoots. However, it is sensitive to noise because sudden changes in the measured error can amplify the derivative term. Often, a low-pass filter is applied to the derivative term to mitigate noise issues.


### 3.1 Numerical Implementation of Integrals and Derivatives

#### Integral
A common approach to implementing the integral term in code is to accumulate the error in a variable at each sample time:

```cpp
// Pseudocode for the integral term
accumulatedError += e[n] * Ts;  // approximate integral by summing error over time
```

#### Derivative
The derivative is typically approximated using a finite difference method:

```cpp
// Pseudocode for the derivative term
derivative = (e[n] - e[n-1]) / Ts;
```

To reduce noise amplification, a filtered derivative may be used:

```cpp
// Pseudocode using a low-pass filter for the derivative term
derivativeRaw = (e[n] - e[n-1]) / Ts;
derivativeFiltered = alpha * derivativeFiltered + (1 - alpha) * derivativeRaw;
```
where `0 < alpha < 1` controls the filtering aggressiveness.

### 3.2 Integrator Windup

**Definition:**  
Integrator windup occurs when the integral term accumulates a large error during periods when the control output is saturated by hardware limits (e.g., maximum voltage to a motor). When the error subsequently changes sign, the large accumulated integral term can cause excessive overshoot or sluggish recovery.

**Mitigation Strategies:**

1. **Integral Clamping (Saturation):**
   - Monitor the control output for saturation.
   - Prevent further accumulation of the integral term when limits are reached.

2. **Anti-Windup Back-Calculation:**
   - Calculate the discrepancy between the computed control signal and the actual saturated output.
   - Adjust the integrator to account for this difference.

3. **Conditional Integration:**
   - Only integrate when the control output is not at the saturation limit, or when the error maintains the same sign as the integral term.

### 3.3 Control Loop Timing

#### Sampling Rate Relative to System Dynamics
- **Nyquist Criterion:** Sampling should be at least twice the highest frequency of interest.
- **Rule of Thumb:** The sampling rate is often set to 10–20 times the dominant bandwidth of the system, ensuring that all relevant dynamics are captured without introducing excessive noise.

#### Real-Time Constraints
- **Deterministic Execution:** The control loop must run at fixed intervals with minimal jitter.
- **Implementation:** Real-time operating systems (RTOS) or hardware timers in microcontrollers are typically used to maintain consistent loop timing.
- **Trade-offs:** Faster control loops increase responsiveness but can also introduce more noise and higher computational load.

### 4. Example PID Structure (Pseudocode)

Below is a sample pseudocode for a PID controller implementation:
```python
# Define PID Gains
Kp = 1.0
Ki = 0.5
Kd = 0.1

# Controller state variables
integral = 0.0
prev_error = 0.0
Ts = 0.01  # Sampling period (e.g., 100 Hz)

# Control loop (runs every Ts seconds)
while True:
    # 1. Read sensor value
    measured_value = read_sensor()

    # 2. Compute error between setpoint and measurement
    error = setpoint - measured_value

    # 3. Update the integral term
    integral += error * Ts

    # 4. Compute the derivative term
    derivative = (error - prev_error) / Ts

    # 5. Compute the PID output
    control_output = Kp * error + Ki * integral + Kd * derivative

    # 6. Apply saturation limits (e.g., motor voltage limits) and implement anti-windup if necessary
    saturation_limit = 255  # Example: 8-bit actuator value limit
    if control_output > saturation_limit:
        control_output = saturation_limit
        # Optionally apply anti-windup mechanism here
    elif control_output < -saturation_limit:
        control_output = -saturation_limit
        # Optionally apply anti-windup mechanism here

    # 7. Output command to actuator
    write_actuator(control_output)

    # 8. Update previous error for the next iteration
    prev_error = error

    # 9. Wait until the next sampling period (e.g., using a timer or sleep)
    time.sleep(Ts)
```

## 5. Key Takeaways

1. **Balancing the Terms:**
   - **Proportional ($K_p$)**: Adjusts the control output proportionally to the current error.
   - **Integral ($K_i$)**: Addresses accumulated past errors to eliminate steady-state error, but care must be taken to avoid integrator windup.
   - **Derivative ($K_d$)**: Predicts future error trends to dampen oscillations, requiring filtering to manage noise sensitivity.

2. **Implementation Considerations:**
   - Discrete approximations for the integral and derivative terms must be carefully designed to reflect the desired continuous behavior.
   - Implement strategies to prevent integrator windup when the actuator saturates.
   - The control loop should run at a frequency high enough to accurately capture system dynamics (typically 10–20× the dominant frequency), while maintaining real-time execution.

3. **Real-World Challenges:**
   - Sensor noise, actuator limits, communication delays, and computational constraints all affect the performance of a PID controller.
   - Proper tuning of PID gains is crucial for maintaining system stability and achieving desired performance.

---

## State-Space Control

### 1. What is State-Space Control?

**State-space control** models a physical system using a set of **first-order differential (or difference) equations**. Instead of focusing solely on the system's output, it treats the internal state of the system as a vector, which can be estimated and controlled.

This approach is especially useful for:
- **Multi-variable systems** (multiple inputs and outputs)
- Systems with **internal constraints or dynamics**
- Advanced control techniques such as **LQR, pole placement, observers, and MPC**

### 2.1 Continuous-Time State-Space Representation

$$
\dot{x}(t) = A x(t) + B u(t) \\
y(t) = C x(t) + D u(t)
$$

Where:
- $x(t) \in \mathbb{R}^n$: state vector (e.g., position, velocity, temperature)
- $u(t) \in \mathbb{R}^m$: input/control vector
- $y(t) \in \mathbb{R}^p$: output vector
- $A \in \mathbb{R}^{n \times n}$: system dynamics matrix
- $B \in \mathbb{R}^{n \times m}$: input matrix
- $C \in \mathbb{R}^{p \times n}$: output matrix
- $D \in \mathbb{R}^{p \times m}$: feedthrough matrix

### 2.2 Discrete-Time State-Space Representation

$$
x[k+1] = A x[k] + B u[k] \\
y[k] = C x[k] + D u[k]
$$

---

### 3. State Feedback Control

The goal is to design a control law:

$$
u(t) = -K x(t) + r(t)
$$

- $K \in \mathbb{R}^{m \times n}$: **state feedback gain matrix**
- $r(t)$: optional reference signal

This means the control input is computed from the full state $x(t)$. The matrix $K$ is designed to place the **closed-loop poles** (eigenvalues of $A - BK$) in desired locations in the complex plane.

### 3.1 Closed-Loop Dynamics

$$
\dot{x}(t) = (A - BK) x(t)
$$

---

### 4. Designing the Gain Matrix $K$

#### Pole Placement

- Choose desired closed-loop poles.
- Solve for $K$ such that $\text{eig}(A - BK) =$ desired poles.
- Works if the system is **controllable**.

#### Linear Quadratic Regulator (LQR)

Minimizes a cost function:

$$
J = \int_0^\infty \left( x(t)^T Q x(t) + u(t)^T R u(t) \right) dt
$$

Where:
- $Q$: state penalty matrix (positive semi-definite)
- $R$: control penalty matrix (positive definite)

LQR finds the optimal $K$ that minimizes $J$.

### 5. State Estimation and Observers

In many cases, **not all states are measurable**. Instead, an **observer** (or **state estimator**) is used to estimate $x(t)$ from the output $y(t)$.

### 5.1 Luenberger Observer

$$
\hat{x}'(t) = A \hat{x}(t) + B u(t) + L (y(t) - C \hat{x}(t))
$$

- $\hat{x}(t)$: estimated state
- $L$: observer gain

**Intuition**
- Used to estimate aspects of the state that aren't directly measureable
- For example, used to estimate velocity when only position is directly measured
- Does not account of process or sensor uncertainty

### 5.2 Kalman Filter

**Prediction Step**

Uses the system's model to predict the next state and its uncertainty.

$$
\hat{x}_{k|k-1} = A \hat{x}_{k-1|k-1} + B u_{k-1}
$$
$$
P_{k|k-1} = A P_{k-1|k-1} A^T + Q
$$

- $\hat{x}_{k|k-1}$: predicted state at time \( k \)  
- $P_{k|k-1}$: predicted error covariance  
- $Q$: process noise covariance  

**Update (Correction) Step**

Incorporates the measurement to update the state estimate and reduce uncertainty.

$$
K_k = P_{k|k-1} C^T (C P_{k|k-1} C^T + R)^{-1}
$$
$$
\hat{x}_{k|k} = \hat{x}_{k|k-1} + K_k (y_k - C \hat{x}_{k|k-1})
$$
$$
P_{k|k} = (I - K_k C) P_{k|k-1}
$$

- $K_k$: Kalman gain — balances model vs. measurement  
- $y_k$: actual measurement at time $k$
- $R$: measurement noise covariance  

**Intuition**

- If your **model is very accurate**, the filter trusts it more.
- If your **measurements are very accurate**, the filter gives them more weight.
- The Kalman gain $K_k$ determines how much to correct based on the uncertainty in the prediction and the measurement.


### 6. Practical Implications for CPS

- **Higher Design Overhead**: Requires accurate system modeling.
- **Stronger Performance**: Better control of transient and steady-state behavior.
- **Hardware Requirements**: Slightly more computationally intensive than PID, but easily handled by most microcontrollers for modest state sizes.
- **Reference Tracking**: Often implemented with a feedforward term to ensure the system follows a reference trajectory correctly.

$$
u(t) = -Kx(t) + K_r r(t)
$$

Where $K_r$ is calculated to eliminate steady-state error.

### 7. Extensions

- **Kalman Filter**: Optimal observer under Gaussian noise.
- **Model Predictive Control (MPC)**: Solves a constrained optimization problem in real time using state-space dynamics.
- **Nonlinear State-Space Control**: For systems that violate linear assumptions (e.g., feedback linearization, Lyapunov-based methods).

### Summary

State-space control offers a comprehensive, scalable approach to feedback control—particularly well-suited for complex or multi-variable systems found in modern cyber-physical systems. While it requires more upfront modeling effort than PID, it provides superior tools for managing internal dynamics, optimizing performance, and integrating state estimation into feedback loops. It forms the foundation of many advanced control strategies used in robotics, aerospace, automotive systems, and industrial automation.

---

### 3. Adaptive Control
- Controller parameters adjust in real time.
- Handles changes in system dynamics or operating conditions.

### 4. Robust Control
- Designed to tolerate bounded modeling uncertainties.
- Examples: H-infinity control, μ-synthesis.
- Used in safety-critical CPS applications.

### 5. Model Predictive Control (MPC)
- Predicts future behavior over a time horizon using a model.
- Optimizes a cost function subject to constraints.
- High computational load; used in advanced CPS like autonomous vehicles.

### 6. Event-Based or Self-Triggered Control
- Updates only when needed based on certain conditions.
- Reduces computation and communication load in embedded networks.

### 7. Distributed or Decentralized Control
- Multiple controllers operate over subsystems or agents.
- Suitable for large-scale CPS (e.g., smart grids, multi-robot systems).

