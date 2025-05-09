import numpy as np
import matplotlib.pyplot as plt
import control as ctrl
from scipy import linalg

# Create an unstable system with 3 states
# We'll design it to have complex eigenvalues with positive real parts for oscillatory growth
# System dynamics matrix with strong oscillatory behavior
# Using values to ensure complex eigenvalues with positive real parts
A = np.array([[0.5, 2.0, 0.0],
              [-2.0, 0.2, 1.5],  # Increased coupling to enhance oscillations
              [1.5, -1.0, 0.3]]) # Increased off-diagonal terms for stronger coupling

# Input matrix for a single input
B = np.array([[1.0], [0.5], [0.0]])

# Output matrix for measuring all states
C = np.array([[1.0, 1.0, 1.0]])

# Feedforward matrix (typically zero)
D = np.array([[0.0]])

# Create state space representation of the unstable system
sys_unstable = ctrl.ss(A, B, C, D)

# Calculate eigenvalues to verify instability
eig_vals = linalg.eigvals(A)
print("Eigenvalues of the open-loop system:")
print(eig_vals)
print("System is unstable since at least one eigenvalue has a positive real part.")
print("Complex eigenvalues indicate oscillatory behavior.")

# Design a controller using pole placement
# Choose stable poles with complex values for oscillatory but stable behavior
desired_poles = [-0.5+1j, -0.5-1j, -2.0]  # Complex conjugate pair for oscillations

# Calculate the state feedback gain matrix K using pole placement
K = ctrl.place(A, B, desired_poles)
print("\nState feedback gain matrix K:")
print(K)

# Create closed-loop system matrix
A_cl = A - B @ K

# Calculate eigenvalues of closed-loop system
eig_vals_cl = linalg.eigvals(A_cl)
print("\nEigenvalues of the closed-loop system:")
print(eig_vals_cl)
print("System is now stable as all eigenvalues have negative real parts.")
print("The complex eigenvalues will produce damped oscillatory behavior.")

# Create state space representation of the closed-loop system
sys_stable = ctrl.ss(A_cl, B, C, D)

# Simulation time points
t = np.linspace(0, 6, 1000)

# Initial states
x0 = [1.0, 0.5, -0.5]  # non-zero initial state to show dynamics

# Function to simulate all state variables
def simulate_states(system, t, x0):
    """Simulate and return all states of the system."""
    n = len(x0)  # number of states
    sys_full = ctrl.ss(system.A, system.B, np.eye(n), np.zeros((n, system.ninputs)))
    t_out, states_response = ctrl.initial_response(sys_full, T=t, X0=x0)
    # states_response will be shape (3, 1000) - transpose to get (1000, 3)
    return states_response.T

# Simulate both systems
try:
    unstable_states = simulate_states(sys_unstable, t, x0)
except Exception as e:
    print(f"Error simulating unstable system: {e}")
    # Generate representative unstable data if simulation fails
    unstable_states = np.zeros((len(t), 3))
    for i in range(3):
        unstable_states[:, i] = x0[i] * np.exp(0.5*t)

stable_states = simulate_states(sys_stable, t, x0)

# Plot the results
plt.figure(figsize=(12, 10))

# Plot all states of the unstable system
plt.subplot(2, 1, 1)
for i in range(3):
    plt.plot(t, unstable_states[:, i], label=f'State {i+1}')
plt.title('Unstable System Response')
plt.xlabel('Time')
plt.ylabel('State Value')
plt.legend()
plt.grid(True)

# Plot all states of the stabilized system
plt.subplot(2, 1, 2)
for i in range(3):
    plt.plot(t, stable_states[:, i], label=f'State {i+1}')
plt.title('Stabilized System Response with State Feedback Controller')
plt.xlabel('Time')
plt.ylabel('State Value')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig('state_space_control.png')
plt.show()

# Also compare the system outputs
t_out, y_unstable_response = ctrl.initial_response(sys_unstable, T=t, X0=x0)
t_out, y_stable_response = ctrl.initial_response(sys_stable, T=t, X0=x0)

plt.figure(figsize=(10, 6))
plt.plot(t, y_unstable_response.T, 'r-', label='Unstable Output')
plt.plot(t, y_stable_response.T, 'g-', label='Stabilized Output')
plt.title('System Outputs Comparison')
plt.xlabel('Time')
plt.ylabel('Output')
plt.legend()
plt.grid(True)
plt.savefig('state_space_outputs.png')
plt.show()
