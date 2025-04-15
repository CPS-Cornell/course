import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

class Car:
    def __init__(self, mass=1500, drag_coefficient=0.3, frontal_area=2.2):
        """
        Car model with physics
        :param mass: Mass of the car (kg)
        :param drag_coefficient: Aerodynamic drag coefficient
        :param frontal_area: Frontal area of the car (m^2)
        """
        self.mass = mass  # kg
        self.drag_coefficient = drag_coefficient
        self.frontal_area = frontal_area  # m^2
        self.speed = 0  # m/s
        self.air_density = 1.225  # kg/m^3 at sea level
    
    def update(self, force, dt):
        """
        Update car state for one time step
        :param force: Force applied to the car (N)
        :param dt: Time step (s)
        """
        # Calculate drag force: F_drag = 0.5 * Cd * A * rho * v^2
        drag_force = 0.5 * self.drag_coefficient * self.frontal_area * self.air_density * self.speed**2
        
        # Net force = applied force - drag force
        net_force = force - drag_force
        
        # Calculate acceleration (F = ma)
        acceleration = net_force / self.mass
        
        # Update speed using v = v0 + a*t
        self.speed += acceleration * dt
        
        # Ensure speed doesn't go negative
        self.speed = max(0, self.speed)
        
        return self.speed

class PIDController:
    def __init__(self, kp, ki, kd, setpoint):
        """
        PID controller
        :param kp: Proportional gain
        :param ki: Integral gain
        :param kd: Derivative gain
        :param setpoint: Target value
        """
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.prev_error = 0
        self.prev_measured = 0  # Store previous measurement to avoid derivative kick
        self.integral = 0
        
        # Store individual terms for plotting
        self.p_term = 0
        self.i_term = 0
        self.d_term = 0
        
    def compute(self, measured_value, dt):
        """
        Compute control output
        :param measured_value: Current measured value
        :param dt: Time step
        :return: Control output
        """
        # Calculate error
        error = self.setpoint - measured_value
        
        # Proportional term
        self.p_term = self.kp * error
        
        # Integral term with anti-windup
        self.integral += error * dt
        self.i_term = self.ki * self.integral
        
        # Derivative term calculated on measurement (not error) to avoid derivative kick
        derivative = (self.prev_measured - measured_value) / dt if dt > 0 else 0
        self.d_term = self.kd * derivative
        
        # Save values for next iteration
        self.prev_error = error
        self.prev_measured = measured_value
        
        # Total control output
        output = self.p_term + self.i_term + self.d_term
        
        return output

def run_simulation(car, controller, target_speed, simulation_time=100, dt=0.1, wind_disturbance=None):
    """
    Run simulation
    :param car: Car instance
    :param controller: PID controller instance
    :param target_speed: Target speed in m/s
    :param simulation_time: Total simulation time in seconds
    :param dt: Time step in seconds
    :param wind_disturbance: Function that returns wind force at time t
    :return: Time and recorded data for plotting
    """
    # Convert target speed to m/s (assuming input is km/h)
    target_speed_ms = target_speed / 3.6
    controller.setpoint = target_speed_ms
    
    # Prepare arrays to store data
    time_points = np.arange(0, simulation_time, dt)
    speeds = np.zeros_like(time_points)
    control_outputs = np.zeros_like(time_points)
    p_terms = np.zeros_like(time_points)
    i_terms = np.zeros_like(time_points)
    d_terms = np.zeros_like(time_points)
    
    # Run simulation
    for i, t in enumerate(time_points):
        # Record current state
        speeds[i] = car.speed
        
        # Compute control output
        control_output = controller.compute(car.speed, dt)
        control_outputs[i] = control_output
        
        # Record PID terms
        p_terms[i] = controller.p_term
        i_terms[i] = controller.i_term
        d_terms[i] = controller.d_term
        
        # Apply wind disturbance if provided
        wind_force = 0
        if wind_disturbance is not None:
            wind_force = wind_disturbance(t)
            
        # Update car state with control force and wind disturbance
        car.update(control_output + wind_force, dt)
    
    # Convert speeds back to km/h for plotting
    speeds_kmh = speeds * 3.6
    setpoint_kmh = target_speed
    
    return time_points, speeds_kmh, control_outputs, p_terms, i_terms, d_terms, setpoint_kmh

def plot_results(time, speeds, control_outputs, p_terms, i_terms, d_terms, setpoint):
    """Plot simulation results"""
    fig = plt.figure(figsize=(12, 10))
    gs = GridSpec(3, 1, height_ratios=[2, 1, 1])
    
    # Plot car speed
    ax1 = plt.subplot(gs[0])
    ax1.plot(time, speeds, 'b-', linewidth=2, label='Car Speed')
    ax1.axhline(y=setpoint, color='r', linestyle='--', label=f'Target Speed ({setpoint} km/h)')
    ax1.set_ylabel('Speed (km/h)')
    ax1.set_title('Car Cruise Control PID Simulation')
    ax1.grid(True)
    ax1.legend()
    
    # Plot control output
    ax2 = plt.subplot(gs[1], sharex=ax1)
    ax2.plot(time, control_outputs, 'g-', linewidth=2)
    ax2.set_ylabel('Control Force (N)')
    ax2.set_title('Controller Output')
    ax2.grid(True)
    
    # Plot individual PID terms
    ax3 = plt.subplot(gs[2], sharex=ax1)
    ax3.plot(time, p_terms, 'r-', label='P Term')
    ax3.plot(time, i_terms, 'g-', label='I Term')
    ax3.plot(time, d_terms, 'b-', label='D Term')
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Term Value')
    ax3.set_title('PID Components')
    ax3.grid(True)
    ax3.legend()
    
    plt.tight_layout()
    plt.show()

def wind_gust(t):
    return 0
    """Generate random wind gusts"""
    if 30 < t < 35 or 60 < t < 70:
        return -1000  # Strong headwind (negative force)
    elif 40 < t < 45 or 80 < t < 85:
        return 500   # Tailwind (positive force)
    else:
        return 0

def main():
    # Create car instance
    car = Car()
    
    # Create PID controller (tune these values as needed)
    kp = 5000  # Proportional gain
    ki = 0   # Integral gain
    ki = 500   # Integral gain
    #kd = 0  # Derivative gain
    kd = 1500  # Derivative gain
    target_speed = 10  # km/h
    controller = PIDController(kp, ki, kd, target_speed/3.6)  # Convert to m/s
    
    # Run simulation
    time, speeds, control_outputs, p_terms, i_terms, d_terms, setpoint = run_simulation(
        car, controller, target_speed, simulation_time=100, dt=0.001, wind_disturbance=wind_gust
    )
    
    # Plot results
    plot_results(time, speeds, control_outputs, p_terms, i_terms, d_terms, setpoint)

if __name__ == "__main__":
    main()
