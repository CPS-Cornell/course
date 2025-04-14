# Systems of Sensors and Actuators

## Noise Modeling and Reduction in Sensor Systems

Sensor networks consist of multiple interconnected sensors that work together to collect, process, and communicate data about physical environments. By providing real-time insights and facilitating data-driven decision-making, sensor networks play a key role in improving efficiency, reliability, and responsiveness in various cyber-physical systems. Sensors are important for three main reasons: mitigating sensor noise, overcoming environmental factors, and increasing reliability and redundancy.

### Mitigating Sensor Noise

Mitigating noise is essential for ensuring that sensor readings are accurate and reliable. Noise can come from various sources, such as electrical interference or thermal fluctuations, and can significantly affect data quality.

-   **Importance of Sensor Noise Models**: a sensor noise model allows you to know how much you can rely on a sensor reading.

-   **Sensor Noise Models:**

-   **Gaussian Noise**: The most common noise model, assuming that noise follows a normal distribution.

-   **Uniform Noise**: Describes noise with a constant probability distribution over a specific range.

-   **Poisson Noise**: Used for sensors that count events, such as photon sensors, particularly when measuring low-intensity signals.

-   **Shot Noise**: Occurs due to discrete charge carriers, often seen in electronic components and photon detection, especially in weak signals.

-   **Quantization Noise**: Results from analog-to-digital conversion and is influenced by the precision of the digital representation.

-   **1/f Noise (Pink Noise)**: A type of noise where power decreases as frequency increases, commonly seen in electronic circuits and long-term measurements.

-   **White Noise**: Characterized by a flat spectral density, affecting all frequencies equally and representing random, uncorrelated noise.

-   **Fusing Data Based on Sensor Noise**: If you have multiple independent sensor readings, as long as the variance of each reading is finite, the variance of the average of those readings will decrease. Mathematically, if each sensor has a variance \\\sigma^2\\, the variance of the average of independent sensor readings is given by:

$$\sigma^2_{avg} = \frac{\sigma^2}{N}$$

Where $\sigma^2_{avg}$ is the variance of the average of the sensor readings, and \\N\\ is the number of sensors.

### Overcoming Environmental Factors

Environmental conditions, like temperature, humidity, or electromagnetic interference, can impact sensor performance. Properly designed sensor networks can adapt to and compensate for these factors to maintain accurate data collection. It is important to consider **complementary sensors**, or sets of sensors that aren’t impacted by the same environmental variables.

Examples:

-   Example 1: Consider **ultrasonic** and **infrared** proximity sensors. Ultrasonic sensors are susceptible to the texture of an object (due to sound absorption), and infrared sensors are susceptible to the color of an object (due to light absorption). Relying on both can reduce failure modes of the system.

-   Example 2: Many driverless cars use both **LiDAR** and **computer vision**. LiDAR is effective for creating detailed 3D maps, but can be less reliable in heavy rain or fog, while computer vision can be affected by lighting conditions such as shadows or glare. By combining both technologies, the system can compensate for each sensor’s limitations. 

Key Takeaways:

-   **Sensors Measurement Independence:** If two sensors are impacted by the same environmental factors, **their measurement noise cannot be considered independent**.

-   **Sensor Selection:** it is critical to select sensors that are not susceptible to the same environmental factors.

### Increasing Reliability and Redundancy

Reliability and redundancy are crucial in sensor networks to prevent data loss or system failures. By using multiple sensors for the same measurement, systems can ensure continued operation even if some sensors fail.

#### Why Sensor Systems are Critical for Reliability:

1.  **Sensor Vs Actuator Failure**: It tends to be easier to engineer reliability into an actuator by using more robust materials and mechanical designs than it is to engineer reliability into a sensor because many sensors require delicate physical mechanism for proper sensitivity.

    -   For many systems, actuation failure is not as critical as sensor failure.

    -   Example from Agriculture: In climate control systems, such as used in livestock housing or crop storage, a failure of the heating or cooling element could be detected and reported by the temperature sensor leading to rapid repair. Alternatively, a faulty temperature sensor that is off by a few degrees could be difficult to detect until after the livestock or crop is damaged or killed.

2.  **Failure Detection**: Sensors can often report actuator failures, but not vise versa. Multiple sensors are needed in order to be able to detect anomalies due to failure in a single sensor.

## Simulating Sensor Interfaces

Simulating sensor interfaces in the design of cyber-physical systems is crucial for testing and validating algorithms, such as sensor fusion techniques, before deploying them on actual hardware. This process can be broken down into three main steps:

### 1. Modeling the System Dynamics

**Objective**: Create a mathematical representation of the physical system to generate realistic data that sensors would detect.

#### Define the Physical Model

-   **Kinematics and Dynamics**: Establish equations of motion for the system (e.g., Newton’s laws for linear motion, rotational dynamics for angular motion).

-   **State Variables**: Identify key variables such as position, velocity, acceleration, orientation, and angular velocity.

-   **External Forces**: Include forces like gravity, friction, and control inputs that affect the system’s movement.

#### Implement Numerical Simulation

-   **Time Discretization**: Choose a suitable time step (`dt`) for the simulation to balance accuracy and computational efficiency.

-   **Integration Methods**: Use numerical integration techniques (e.g., Euler, Runge-Kutta methods) to update the state variables over time.

-   **Scenario Design**: Define specific movements or maneuvers (e.g., straight-line motion, rotations) that the system will perform during the simulation.

#### Validation

-   **Sanity Checks**: Ensure the simulated motion adheres to physical laws and expected behavior.

-   **Visualization**: Plot trajectories and state variables to visually inspect the system’s dynamics.

### 2. Modeling the Sensor Noise

**Objective**: Simulate realistic sensor outputs by adding noise and imperfections to the ideal measurements.

#### Identify Sensor Characteristics

-   **Sensor Types**: Determine which sensors are being simulated (e.g., accelerometers, gyroscopes).

-   **Specifications**: Gather data on sensor specifications such as range, sensitivity, resolution, and noise characteristics from datasheets.

#### Implement Noise Models

-   **Random Noise**:

    -   **Gaussian Noise**: Add zero-mean Gaussian noise to simulate white noise commonly present in sensors.

    -   **Standard Deviation**: Set the noise level based on the sensor’s noise density specification.

-   **Bias and Drift**:

    -   **Constant Bias**: Include a fixed offset that represents calibration errors.

    -   **Temperature Effects**: Model drift that can occur due to temperature changes over time.

-   **Quantization Error**:

    -   **Resolution Limitations**: Simulate the effects of finite sensor resolution by quantizing the sensor outputs.

-   **Other Noise Types**:

    -   A more extensive list of noise models is given in Mitigating Sensor Noise section.

#### Generate Noisy Sensor Data

-   **Transform True States**: Convert the system dynamics into sensor measurements (e.g., acceleration, angular velocity) in the sensor’s frame of reference.

-   **Apply Noise**: Add the modeled noise to the ideal sensor readings to obtain simulated measurements.

-   **Environmental Factors**: Optionally include effects like vibrations or electromagnetic interference if relevant.

#### Validation

-   **Statistical Analysis**: Check that the noise-added data matches expected statistical properties.

-   **Comparison with Real Data**: If possible, compare simulated sensor data with real-world measurements for accuracy.

### 3. Simulating the Communication Interface (Optional)

**Objective**: Emulate the data transmission between sensors and processing units, including communication protocols.

#### Understand the Communication Protocol

-   **Protocol Specifications**: Familiarize yourself with the communication protocol used by the sensors (e.g., I²C, SPI) and all relevant factors, for example:

    -   **Addressing**: Know how sensors are addressed on the bus.

    -   **Data Format**: Understand how data is formatted and transmitted.

    -   **Clock Speed**: Determine the clock frequency and data rate of the communication.

    -   **Timings**: Be aware of the timing requirements for start/stop conditions and data transfer.

    -   **Other Sensors**: If multiple sensors are involved, understand how they interact on the bus, including impacts on data throughput.

    -   **Master-Slave Architecture**: Recognize the roles of master and slave devices in communication.

#### Implement Protocol Simulation

-   **Software Simulation**:

-   **Libraries and Tools**: Use programming libraries or simulation tools to emulate the communication protocol.

-   **Virtual Devices**: Create virtual sensor devices that behaves as if it were the real sensor.

-   **Data Packaging**:

-   **Registers and Buffers**: Simulate sensor registers where data is stored and retrieved.

-   **Data Formats**: Ensure data is formatted correctly (e.g., two’s complement, bit packing, endianess).

#### Simulate Communication Timing and Behavior (for features not handled by the communication protocol)

-   **Clock Synchronization**: Emulate the clock signals and ensure proper timing between the master and slave.

-   **Start/Stop Conditions**: Implement the start and stop conditions as per the protocol.

-   **Acknowledgment Bits**: Handle acknowledgments after each byte transferred.

-   **Error Handling**: Simulate potential communication errors, such as NACK responses or bus contention.

#### Integrate with Sensor Data

-   **Data Retrieval**: Program the virtual sensor to provide the noisy sensor data upon request.

-   **Command Processing**: Implement handling of specific commands or configurations sent over the interface.

#### Testing and Validation

-   **Protocol Analyzers**: Use software tools to monitor and verify the correctness of the simulated communication.

-   **Integration Testing**: Connect the simulated interface with the sensor fusion algorithm to test end-to-end functionality.

### Conclusion

By following these three steps, you create a comprehensive simulation environment that allows you to:

-   **Test Algorithms**: Evaluate sensor fusion or data processing algorithms using realistic sensor data and communication protocols.

-   **Identify Issues Early**: Detect and correct potential problems in the system design before hardware implementation.

-   **Optimize Performance**: Experiment with different system parameters, sensor specifications, and communication settings to optimize system performance.

#### Additional Tips

-   **Modular Design**: Keep the simulation components modular to allow easy updates and reuse in different projects.

-   **Documentation**: Document your models and assumptions thoroughly to aid in debugging and future development.

-   **Collaboration**: If working in a team, ensure that interfaces between modules are well-defined to facilitate collaboration.

## Reliability and Redundancy in Cyber-Physical Systems

### Terminology

The reliability of cyber-physical systems is paramount, especially in applications like autonomous vehicles, medical devices, and industrial automation. This module explores how to model and enhance the reliability and redundancy of CPS using probabilistic methods and system architecture considerations.

#### Reliability, Availability, Maintainability

-   **Reliability $R$**: The probability that a system or component performs its required functions under stated conditions for a specified period.

-   **Availability $A$**: The proportion of time a system is in a functioning condition. It considers both reliability and maintainability.

-   **Maintainability $M$**: The probability that a failed system will be restored to operational effectiveness within a given period.

#### Failure Modes

Understanding how components can fail is crucial for modeling reliability.

-   **Hardware Failures**: Physical component degradation or sudden breakdown.

-   **Software Failures**: Bugs, errors in code logic, or unexpected inputs leading to crashes.

-   **Network Failures**: Communication breakdowns, latency issues, or data loss.

#### Mean Time to Failure (MTTF)

-   **Definition**: The average expected time to the first failure of a non-repairable system.

-   **Calculation**: For a large number of identical components:

$$MTTF = \frac{Total\ operational\ time}{Number\ of\ failures}$$

#### Mean Time Between Failures (MTBF)

-   **Definition**: The average time between consecutive failures in a repairable system.

-   **Calculation**: $MTBF = MTTF + MTTR$ (Mean Time to Repair), but often $MTTR$ is negligible.

#### Failure Rate $\lambda$

-   **Definition**: The frequency with which an engineered system or component fails, expressed in failures per unit of time.

-   **Relation to $MTTF$**: $\lambda = \frac{1}{MTTF}$.

## Probabilistic Modeling of Reliability

Failure and Reliability functions are can use different distributions to model the behavior of components and systems. The most common models for reliability are based on constant failure rates or time-dependent failure rates. 
- **Constant Failure Rate**: Assumes that the failure rate $\lambda$ is constant over time (exponential distribution). 
- **Time-Dependent Failure Rate**: Uses distributions like Weibull to model systems where failure rates change over time.

### Constant Failure Rate Reliability Function

The failure rate, $\lambda$, is the reciprocal of the MTTF, and is assumed to be constant over time. We use an exponential distribution to model the probability that a component survives until time $t$ without failure.

-   **Reliability Function $R(t)$**: The probability that a component survives until time $t$ without failure.

    $$R(t) = e^{-\lambda t}$$

-   **Failure Function $F(t)$**: The probability that a component fails by time t.

    $$F(t) = 1 - R(t) = 1 - e^{-\lambda t}$$

-   **Probability Density Function $f(t)$**: The rate at which failures occur at time t.

#### Example: Estimating the Probability of Sensor Failure Within 5 Years

To estimate the probability that a sensor will fail within 5 years when its mean time to failure (MTTF) is 12 years, we can use the exponential reliability function, which is commonly used for electronic components with a constant failure rate.

##### Step-by-Step Calculation

1. **Calculate the Failure Rate ($\lambda$):**

    - The failure rate $\lambda$ is the reciprocal of the MTTF.

    $$\lambda = \frac{1}{\text{MTTF}} = \frac{1}{12 \text{ years}} \approx 0.08333 \text{ failures/year}$$

2. **Use the Reliability Function:**

    - The reliability function for an exponential distribution is:

    $$R(t) = e^{-\lambda t}$$

    - Where:
        - $R(t)$ is the probability that the sensor **survives** up to time $t$.
        - $t$ is the time in years.

3. **Calculate the Reliability at $t = 5$ Years:**

    $$R(5) = e^{-0.08333 \times 5} = e^{-0.41665} \approx 0.65924$$

    - This means there’s approximately a 65.92% chance the sensor will **survive** for 5 years.

4. **Calculate the Probability of Failure Within 5 Years:**

    - The probability that the sensor **fails** within 5 years is:

    $$P(\text{Failure within 5 years}) = 1 - R(5) = 1 - 0.65924 = 0.34076 = \boxed{34.08\%}$$

    - So there’s approximately a **34.08%** chance the sensor will fail within 5 years.

### Time-dependent Failure Rate Reliability Function (Weibull Distribution)

The failure rate $\lambda(t)$ is a function of time, allowing for varying failure rates over the lifetime of a component. The **Weibull distribution** is commonly used to model such behavior. It is particularly useful because it can represent increasing, decreasing, or constant failure rates, which correspond to different phases of a product’s lifecycle.

#### Key Parameters

1.  **Shape Parameter ($\beta$)**

    -   **Interpretation:** Determines how the failure rate changes over time.

    -   **Values and Implications:**

        -   $\beta < 1$: Decreasing failure rate

            -   **Implications:** Early-life failures or "infant mortality."

            -   **Causes:** Manufacturing defects or early wear-in issues.

            -   **Failure Rate Behavior:** Decreases over time.

        -   $\beta = 1$: Constant failure rate

            -   **Implications:** Random failures, no aging effect.

            -   **Causes:** External random events, constant risk over time.

            -   **Failure Rate Behavior:** Remains constant.

            -   **Note:** Weibull distribution reduces to the exponential distribution.

        -   $\beta > 1$: Increasing failure rate

            -   **Implications:** Wear-out failures or aging products.

            -   **Causes:** Material fatigue, wear and tear, degradation.

            -   **Failure Rate Behavior:** Increases over time.

2.  **Scale Parameter ($\eta$)**

    -   **Implications:** A scale factor that stretches or compresses the distribution along the time axis.

    -   **Higher $\eta$:** Longer life products.

    -   **Lower $\eta$:** Shorter life products.

    -   **Note**: when $\beta = 1$, the Weibull distribution reduces to the exponential distribution with $\lambda = \frac{1}{\eta}$.

#### Mathematical Functions

-   **Reliability Function**: The probability that a unit will survive beyond time $t$:

    $$R(t) = e^{-\left(\frac{t}{\eta}\right)^\beta}$$

-   **Failure Function $F(t)$**: The probability that a component fails by time $t$:

    $$F(t) = 1 - e^{-\left( \frac{t}{\eta}\right)^\beta }$$

-   **Probability Density Function (PDF)**: The likelihood of failure at a specific time $t$:

    $$f(t) = \frac{\beta}{\eta} \left( \frac{t}{\eta}\right)^{\beta - 1} e^{-\left( \frac{t}{\eta}\right)^\beta }$$

-   **Hazard Function** (Failure Rate Function): The instantaneous failure rate at time $t$:

    $$h(t) = \frac{f(t)}{R(t)} = \frac{\beta}{\eta} \left( \frac{t}{\eta} \right)^{\beta - 1}$$

#### Example

**Scenario:** Suppose you have collected failure data for a type of sensor and estimated the Weibull parameters as $\beta = 1.5$ and $\eta = 1,000$ hours.

**Calculations:**

1. **Reliability:** Calculate the reliability of a sensor at $t = 500$ hours.

    $$R(500) = e^{- \left( \frac{500}{1,000} \right)^{1.5}} = e^{- \left( 0.5 \right)^{1.5}} = e^{-0.3536} \approx 0.7022$$

    **Interpretation:** Approximately 70.22% of sensors are expected to survive beyond 500 hours.

2. **Probability of Failure:** Calculate the probability that a sensor will fail by $t = 1,500$ hours.

    $$F(1,500) = 1 - e^{- \left( \frac{1,500}{1,000} \right)^{1.5}} = 1 - e^{- \left( 1.5 \right)^{1.5}} = 1 - e^{-1.8371} \approx 1 - 0.1590 = 0.8410$$

    **Interpretation:** Approximately 84.10% of sensors are expected to fail by 1,500 hours.

3. **Hazard Function:** Calculate the effective failure rate at $t = 1,000$ hours.

    $$h(1,000) = \frac{1.5}{1,000} \left( \frac{1,000}{1,000} \right)^{1.5 - 1} = \frac{1.5}{1,000} (1)^{0.5} = 0.0015 \text{ failures/hour}$$

    **Interpretation:** The instantaneous failure rate at 1,000 hours is 0.0015 failures per hour.

### Visual Representation

While we cannot display graphs here, in practice, you can plot:

-   **PDF:** Shows the distribution of failure times.

-   **CDF:** Illustrates the cumulative probability of failure over time.

-   **Reliability Function R(t):** Depicts the probability of survival over time.

-   **Hazard Function h(t):** Visualizes how the failure rate changes with time.

### When to Use Weibull Distribution

When purchasing parts from a distributer, you may often receive information on the mean time to failure. You can use the constant failure rate model to calculate how the reliability of the part decreases with wear and tear, but **you can not account for early failure due to manufacturing defects**. However, the Weibull distribution can account for changing failure rates over time, which can be useful in the following scenarios:

-   If a component has a high failure rate at the beginning of its life, you may want to add a "burn-in" period to your testing procedures to weed out faulty components before shipping the product to the customer.

-   If you are designing a maintenance testing schedule, you may want add additional calibration and testing earlier in the life of the component to catch any early failures, and then reduce the frequency of testing after a certain age, until it reaches the end of its life where you may want to begin testing more frequently again.

-   When designing warranty policies, you may want the policy to cover the period of time where the components are most likely to prematurely fail due to manufacturing defects, but not cover the period of time where the component is most likely to fail due to wear and tear.

Generally, if you are collecting data to characterize the reliability of a component, it is best to also account for manufacturing defects and early life failures by using the Weibull distribution. If you are using a component that has already been characterized by the manufacturer and only the mean time to failure is provided, you can use the constant failure rate model to estimate the reliability of the component over time.

## Modeling Reliability in Cyber-Physical Systems

Understanding **series** and **parallel systems** is fundamental in reliability engineering, as it helps in designing systems with desired reliability levels. This document explains these concepts in detail and provides examples of how sensors or actuators can be configured in series or parallel to affect system reliability.

### Series Systems

-   **Definition**: The system fails if any component fails.

-   **Reliability Calculation**:

    $$R_{\text{series}} = \prod_{i=1}^{n} R_i$$

-   **Interpretation**: Reliability decreases as more components are added in series.

### Parallel Systems

-   **Definition**: The system functions as long as at least one component functions.

-   **Reliability Calculation**:

    $$R_{\text{parallel}} = 1 - \prod_{i=1}^{n} (1 - R_i)$$

-   **Interpretation**: Adding components in parallel increases system reliability.

### k-out-of-n Systems

-   **Definition**: The system functions if at least $k$ out of $n$ components function.

-   **Reliability Calculation**:

    $$R = \sum_{i=k}^{n} \binom{n}{i} R_i^i (1 - R_i)^{n - i}$$

-   **Interpretation**: Adding more components than is needed to operate the system increases reliability, and allows for broken components to be replaced without system failure.

## Implications for Systems Modeling

The calculations show that the system maintains high reliability over the first two years, primarily due to the redundancy in both the temperature sensors and heating elements.

**Recommendations to Maintain High System Reliability:**

1.  **Regular Maintenance:**

    -   Schedule periodic inspections to identify and replace any failing components.

2.  **Monitoring Systems:**

    -   Install real-time monitoring to detect early signs of component degradation.

3.  **Environmental Controls:**

    -   Ensure optimal operating conditions to minimize stress on components.

4.  **Future Planning:**

    -   As time progresses beyond two years, consider strategies to address the gradual decline in reliability, such as proactive replacements or increased redundancy.

### Examples of Series and Parallel Systems in Reliability Engineering

#### Actuators in Series

-   **Scenario:** Consider a robotic arm with multiple joints, each powered by an actuator. The proper functioning of the robotic arm requires all actuators to operate correctly.

-   **System Requirement:** Failure of any actuator leads to failure of the entire robotic arm’s operation.

-   **Reliability Calculation:** Assuming each actuator has reliability $R_a(t)$:

-   **Total System Reliability for *N* Actuators in Series:**

    $$R_{\text{system}}(t) = [R_a(t)]^N$$

-   **Example Calculation:** If each actuator has a reliability of 95% ($R_a(t) = 0.95$):

-   **With 3 Actuators in Series:** The system reliability is about 85.74%.

    $$R_{\text{system}}(t) = (0.95)^3 = 0.8574$$

-   **Implication:** The more actuators connected in series, the lower the overall system reliability.

#### Sensors in Parallel (Redundant Sensors)

-   **Scenario:** You have multiple sensors measuring the same parameter, and the system requires only one functioning sensor to operate. This is common in critical systems where sensor failure can have significant consequences (e.g., in aerospace or medical devices).

-   **System Configuration:**

    -   Primary Sensor
    -   Redundant Backup Sensors

-   **Reliability Calculation:** If each sensor has reliability $R_s(t)$:

    -   **Total System Reliability with *N* Sensors:**

        $$R_{\text{system}}(t) = 1 - [1 - R_s(t)]^N$$

-   **Example Calculation:** Suppose each sensor has a reliability of 90% ($R_s(t) = 0.9$) over a mission time.

    -   **With 1 Sensor:**

        $$R_{\text{system}}(t) = R_s(t) = 0.9$$

    -   **With 2 Sensors in Parallel:** The system reliability increases to 99% with one redundant sensor.

        $$R_{\text{system}}(t) = 1 - [1 - 0.9]^2 = 1 - (0.1)^2 = 1 - 0.01 = 0.99$$

    -   **With 3 Sensors in Parallel:** The system reliability increases to 99.9% with two redundant sensors.

        $$R_{\text{system}}(t) = 1 - [1 - 0.9]^3 = 1 - (0.1)^3 = 1 - 0.001 = 0.999$$

-   **Implication:** Adding redundant sensors in parallel significantly increases system reliability.

#### Example: Chicken Barn

A chicken barn has four temperature sensors and 15 heating elements to keep the chickens warm. The system needs at least two temperature sensors and 10 heating elements to fully work. The mean time between failures for the temperature sensors is 15 years and the mean time between failures for the heating elements is 10 years. Calculate the probability that the system will fail within one year and two years of operation.

##### System Overview

-   **Temperature Sensors:**

    -   Quantity: **4**

    -   Requirement: At least **2** must be operational.

    -   Mean Time Between Failures (MTBF): **15 years**

-   **Heating Elements:**

    -   Quantity: **15**

    -   Requirement: At least **10** must be operational.

    -   Mean Time Between Failures (MTBF): **10 years**

##### Assumptions

1.  Constant Failure Rate: The failure rates are constant over time (exponential distribution).

2.  Independence: Failures are independent events.

3.  Binary State Components: Components are either fully operational or failed (no partial failures).

##### Calculation Steps

##### Calculation Steps

1. **Calculate Failure Rates ($\lambda$)**

The failure rate $\lambda$ is the reciprocal of the MTBF:

- Temperature Sensors:
    $$\lambda_{\text{sensor}} = \frac{1}{\text{MTBF}_{\text{sensor}}} = \frac{1}{15} \approx 0.0667 \text{ failures/year}$$

- Heating Elements:
    $$\lambda_{\text{element}} = \frac{1}{\text{MTBF}_{\text{element}}} = \frac{1}{10} = 0.1 \text{ failures/year}$$

2. **Compute Individual Component Reliability ($R(t)$)**

The reliability function for an exponential distribution is:
$$R(t) = e^{-\lambda t}$$

- At $t = 1$ Year:
    - Temperature Sensors:
        $$R_{\text{sensor}}(1) = e^{-0.0667 \times 1} = e^{-0.0667} \approx 0.9355$$
    - Heating Elements:
        $$R_{\text{element}}(1) = e^{-0.1 \times 1} = e^{-0.1} \approx 0.9048$$

- At $t = 2$ Years:
    - Temperature Sensors:
        $$R_{\text{sensor}}(2) = e^{-0.0667 \times 2} = e^{-0.1334} \approx 0.8752$$
    - Heating Elements:
        $$R_{\text{element}}(2) = e^{-0.1 \times 2} = e^{-0.2} \approx 0.8187$$

3. **Calculate Probabilities for Components**

**Temperature Sensors**: We need the probability that at least 2 out of 4 sensors are operational.

Let:
- $p_s = R_{\text{sensor}}(t)$ (probability a sensor is operational)
- $q_s = 1 - p_s$ (probability a sensor has failed)

Possible Successful Scenarios:
1. Exactly 2 Sensors Operational:
     $$P(\text{2 working}) = {4 \choose 2} p_s^2 q_s^2 = 6 p_s^2 q_s^2$$
2. Exactly 3 Sensors Operational:
     $$P(\text{3 working}) = {4 \choose 3} p_s^3 q_s = 4 p_s^3 q_s$$
3. Exactly 4 Sensors Operational:
     $$P(\text{4 working}) = {4 \choose 4} p_s^4 = p_s^4$$

Total Probability:
$$P_{\text{sensor}}(t) = P(\text{2 working}) + P(\text{3 working}) + P(\text{4 working})$$

**Heating Elements**: We need the probability that at least 10 out of 15 elements are operational.

Let:
- $p_e = R_{\text{element}}(t)$ (probability an element is operational)
- $q_e = 1 - p_e$ (probability an element has failed)

Total Probability:
$$P_{\text{element}}(t) = \sum_{k=10}^{15} {15 \choose k} p_e^k q_e^{15 - k}$$

4. **Calculate System Reliability**

The system functions only if both the sensors and heating elements meet their operational requirements.
$$R_{\text{system}}(t) = P_{\text{sensor}}(t) \cdot P_{\text{element}}(t)$$

**Temperature Sensors At $t = 1$ Year**:
- Values:
    - $p_s = 0.9355$
    - $q_s = 1 - 0.9355 = 0.0645$

Calculations:
1. $P(\text{2 working}) = 6 \times (0.9355)^2 \times (0.0645)^2 \approx 0.0218$
2. $P(\text{3 working}) = 4 \times (0.9355)^3 \times 0.0645 \approx 0.2114$
3. $P(\text{4 working}) = (0.9355)^4 \approx 0.7659$

Total Probability:
$$P_{\text{sensor}}(1) = 0.0218 + 0.2114 + 0.7659 = 0.9991$$

**Heating Elements At $t = 1$ Year**:
- Values:
    - $p_e = 0.9048$
    - $q_e = 1 - 0.9048 = 0.0952$

Calculations:
$$P_{\text{element}}(1) = \sum_{k=10}^{15} {15 \choose k} p_e^k q_e^{15 - k}$$

Compute Individual Probabilities:
1. $P(\text{10 working}) = {15 \choose 10} p_e^{10} q_e^5 \approx 0.0087$
2. $P(\text{11 working}) = {15 \choose 11} p_e^{11} q_e^4 \approx 0.0373$
3. $P(\text{12 working}) = {15 \choose 12} p_e^{12} q_e^3 \approx 0.1181$
4. $P(\text{13 working}) = {15 \choose 13} p_e^{13} q_e^2 \approx 0.2593$
5. $P(\text{14 working}) = {15 \choose 14} p_e^{14} q_e \approx 0.3521$
6. $P(\text{15 working}) = (0.9048)^{15} \approx 0.2231$

Total Probability:
$$P_{\text{element}}(1) = 0.0087 + 0.0373 + 0.1181 + 0.2593 + 0.3521 + 0.2231 = 0.9985$$

**System Reliability at 1 Year**:
$$R_{\text{system}}(1) = P_{\text{sensor}}(1) \cdot P_{\text{element}}(1) \approx 0.9991 \times 0.9985 \approx 0.9976$$

**Probability of Failure at 1 Year**:
$$P_{\text{failure}}(1) = 1 - R_{\text{system}}(1) \approx 1 - 0.9976 = 0.0024 = \boxed{0.24\%}$$
