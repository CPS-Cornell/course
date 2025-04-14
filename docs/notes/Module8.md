# State Estimation for Cyber-physical Systems

## Signal Processing Concepts for Cyber-Physical Systems

### 1. Digital vs Analog Signals

In signal processing, it is important to understand the difference between analog and digital signals.

**Analog signals**  
Analog signals are continuous in both time and amplitude, representing real-world phenomena like sound, temperature, or light. Computation can be performed with analog components such as capacitors, resistors, and inductors, which can be used to implement mathematical operations like integration, differentiation, and filtering.

**Digital signals**  
Digital signals are discrete in nature, meaning they are represented by a sequence of distinct values. To process analog signals in digital systems, they need to be sampled and quantized. Most signal processing within cyber-physical systems has been shifted to computational systems due to their flexibility and ease of implementation.

Deciding whether to implement signal processing on an analog signal or convert it to a digital signal for processing is crucial in cyber-physical systems. This decision often depends on factors such as cost, space, reliability, timing constraints, and performance. Environmental conditions like temperature, humidity, and electromagnetic interference can affect both analog and digital components, potentially leading to early failure. Although analog components, such as resistors and capacitors, are often easier to replace compared to surface-mount microprocessors, the low cost of microcontrollers and circuit board production may make replacing the entire circuit board more economical. For this reason, careful analysis is required when designing signal processing systems.

### 2. Sampling and Quantization

In signal processing, sampling and quantization are key steps in converting an analog signal to a digital signal.

#### Aliasing and the Nyquist Frequency

##### What Is Aliasing?

**Aliasing** is a phenomenon that occurs when a continuous signal is sampled at a rate that is insufficient to accurately capture its frequency content. When the sampling rate is too low, high-frequency components of the signal are "misinterpreted" as lower frequencies in the sampled data, causing distortion. This effect is called aliasing because the high-frequency components appear as "aliases" of lower frequencies in the sampled signal.

##### How Does Aliasing Occur?

When a signal is sampled, it is multiplied by a series of evenly spaced pulses (the sampling rate). This multiplication produces replicas of the signal’s spectrum centered around multiples of the sampling frequency $f_s$. If the sampling rate is too low, the replicas overlap, causing different frequency components to blend together, which leads to aliasing.

##### The Nyquist Frequency

The **Nyquist frequency** is defined as half of the sampling rate:

$$f_{\text{Nyquist}} = \frac{f_s}{2}$$

- **Sampling Theorem (Nyquist-Shannon Theorem):** To avoid aliasing, a continuous signal must be sampled at a rate greater than twice its highest frequency component. This required rate is known as the **Nyquist rate**.

- **Condition:** If a signal contains frequencies up to $f_{\max}$, then the sampling rate $f_s$ should satisfy:

$$f_s > 2 f_{\max}$$

This ensures that all frequency components are below the Nyquist frequency $f_{\text{Nyquist}}$, and no aliasing occurs.

##### Relationship Between Aliasing and the Nyquist Frequency

- **Frequencies Above the Nyquist Frequency:** When sampling a signal, any frequency component above the Nyquist frequency will "fold" back and appear as a lower frequency in the sampled signal. For example, if a frequency component in the original signal is slightly above $f_{\text{Nyquist}}$, it will be interpreted as a frequency just below $f_{\text{Nyquist}}$ in the sampled data.

- **Frequency "Folding":** The effect of aliasing can be thought of as a mirroring or folding around the Nyquist frequency. Frequencies above the Nyquist frequency will "reflect" into the range from $0$ to $f_{\text{Nyquist}}$, creating incorrect low-frequency representations.

##### Example of Aliasing with the Nyquist Frequency

Consider a continuous signal with a frequency component at $f = 1.5 f_{\text{Nyquist}}$. When sampled:

- **Expected Frequency Representation:** Without aliasing, this component would be represented at $f = 1.5 f_{\text{Nyquist}}$.

- **Aliased Frequency Representation:** Since it exceeds the Nyquist frequency, it folds back to appear as a frequency at $f_{\text{alias}} = 0.5 f_{\text{Nyquist}}$.

This lower frequency (alias) is not present in the original signal, leading to distortion in the sampled signal’s frequency content.

##### Preventing Aliasing

1.  **Use a Higher Sampling Rate:** Increase the sampling rate so that it exceeds twice the maximum frequency of the signal.

2.  **Apply an Anti-Aliasing Filter:** Before sampling, apply a low-pass filter to the continuous signal to remove frequency components above the Nyquist frequency. This filter, known as an **anti-aliasing filter**, ensures that only frequencies within the allowable range are sampled, preventing aliasing.

##### Summary

-   **Aliasing** is the distortion that occurs when sampling a signal at a rate that is insufficient to capture its high-frequency content.

-   **Nyquist Frequency** is half of the sampling rate and represents the highest frequency that can be accurately represented in sampled data without aliasing.

-   **Relation:** To avoid aliasing, the signal must be sampled at a rate greater than twice the highest frequency in the signal (the Nyquist rate).

-   **Prevention:** Use a high enough sampling rate and/or an anti-aliasing filter to remove high-frequency components before sampling.

#### Quantization:

**Quantization**  
The process of mapping the sampled values to discrete levels. This introduces a level of **quantization error** due to the rounding of values to the nearest level.

**Quantization Error**  
The difference between the original analog value and the quantized digital value. It is a form of distortion that affects the accuracy of the digital representation of the signal.

The resolution of quantization determines how accurately the analog value can be represented digitally. This can be determined by the ADC, or by the computational system during storage after the data is collected. While it might seem better to have the highest resolution possible, there are a number of trade-offs to consider. Higher resolution data takes more memory, longer to transfer, is more computationally expensive to process, and might not match the architecture of the processor.

For example, the Raspberry Pi Pico’s processor only supports 32-bit numbers. Adding or subtracting any two numbers takes the same amount of time regardless of the number, as long the numbers are 32 bits. When a number is so large it needs to be presented by 64 bits, there will be a slow down when doing computations on a 32-bit processor.

### 3. Frequency Analysis

Understanding the frequency components of signals is fundamental for many applications in cyber-physical systems. Different transforms help analyze signals in the frequency domain:

#### **Digital Fourier Transform (DFT)**

The Digital Fourier Transform is a mathematical technique used to convert a discrete signal from its original domain (often time or space) into the frequency domain. It decomposes a sequence of values into components of different frequencies, effectively revealing the frequency spectrum of the signal. The DFT is defined for a sequence of $N$ complex numbers and produces an $N$-point frequency spectrum.

### Overview of the DFT:

- **Basis Functions:** The DFT uses complex exponentials (sines and cosines) as its basis functions. These functions extend infinitely in time, meaning they are not localized.
- **Global Analysis:** Because the basis functions are not localized, the DFT analyzes the signal globally. It considers the entire time domain to compute each frequency component.
- **Stationary Signals:** The DFT is most effective for stationary signals—signals whose statistical properties do not change over time—because it assumes the frequency content does not vary with time.
- **Resolution:** It provides uniform resolution across all frequencies, which can be a limitation when dealing with signals that have both high-frequency and low-frequency components of interest.

### Equation of the Digital Fourier Transform

The DFT of a discrete-time signal $x[n]$ of length $N$ is defined by the equation:

$$
X[k] = \sum_{n=0}^{N-1} x[n] \cdot e^{-j \frac{2\pi}{N} k n}
$$

- $X[k]$: The $k$-th element of the transformed sequence in the frequency domain.
- $x[n]$: The $n$-th element of the original sequence in the time (or spatial) domain.
- $N$: The total number of samples in the sequence.
- $k$: The index of the frequency component, ranging from $0$ to $N-1$.
- $n$: The index of the time-domain sample, ranging from $0$ to $N-1$.
- $j$: The imaginary unit ($j = \sqrt{-1}$).

The exponential term can also be expanded using Euler’s formula:

$$
e^{-j \frac{2\pi}{N} k n} = \cos\left( \frac{2\pi}{N} k n \right) - j \sin\left( \frac{2\pi}{N} k n \right)
$$

### Explanation

- **Frequency Components:** The DFT decomposes the input sequence into its constituent frequencies. Each $X[k]$ represents the amplitude and phase of a specific frequency component.
- **Discrete Frequencies:** The frequencies are discrete and are integer multiples of the fundamental frequency $f_0 = \frac{1}{N T}$, where $T$ is the sampling interval.
- **Complex Numbers:** The result $X[k]$ is generally a complex number, encoding both amplitude and phase information.

### Inverse Digital Fourier Transform

To reconstruct the original time-domain sequence from its frequency-domain representation, the inverse DFT is used:

$$
x[n] = \frac{1}{N} \sum_{k=0}^{N-1} X[k] \cdot e^{j \frac{2\pi}{N} k n}
$$

- The inverse transform uses a positive exponent in the exponential term.
- The factor $\frac{1}{N}$ ensures proper scaling of the amplitude.

### Key Points

- **Periodicity:** Both $x[n]$ and $X[k]$ are assumed to be periodic with period $N$.
- **Orthogonality:** The exponential functions used in the DFT are orthogonal over the interval $N$, which allows for the unique decomposition of the signal.
- **Computational Efficiency:** The Fast Fourier Transform (FFT) is an algorithm to compute the DFT efficiently, reducing the computational complexity from $O(N^2)$ to $O(N \log N)$.

#### Short-Time Fourier Transform (STFT)

Analyzes the frequency content of a signal over short windows of time, providing a time-frequency representation. It is useful when the signal’s frequency components change over time. The STFT is computed by breaking the signal into short segments and applying the Fourier Transform to each segment. It is commonly used in speech processing, music analysis, and vibration analysis, as well as visualization tools such as spectrograms.

#### Wavelet Transform:

Unlike STFT, wavelets provide a multi-resolution analysis of a signal, allowing for good frequency resolution for low frequencies and good time resolution for high frequencies. This makes it particularly useful for non-stationary signals. 
- **Basis Functions:** Wavelets use small waves, called wavelets, as their basis functions. These wavelets are localized in time (they have finite duration) and can be stretched or compressed to analyze different frequency components. 
- **Time-Frequency Localization:** Wavelets provide a time-frequency representation of the signal, making them ideal for analyzing non-stationary signals where frequency components change over time. 
- **Multi-Resolution Analysis:** Wavelets can analyze signals at various scales. High-frequency (short-scale) components are analyzed with good time resolution, while low-frequency (long-scale) components are analyzed with good frequency resolution. 
- **Adaptability:** Because of their ability to focus on specific time intervals and frequency bands, wavelets are useful in applications like image compression, denoising, and feature extraction in signals.

### 4. Filtering

**Filtering** is used to manipulate the frequency content of a signal. Three common types of filters are: **low-pass**, **high-pass**, and **band-pass** filters.

#### Low-Pass Filter

##### Implementation
To implement a simple digital low-pass filter, you can use a **first-order Infinite Impulse Response (IIR) filter**, also known as a recursive filter. This type of filter is efficient and easy to implement, making it suitable for real-time applications. The filter operates using the following difference equation:

$$
y[n] = \alpha \cdot x[n] + (1 - \alpha) \cdot y[n - 1]
$$

Where:
- **$y[n]$**: Current output sample
- **$x[n]$**: Current input sample
- **$y[n - 1]$**: Previous output sample
- **$\alpha$**: Filter coefficient (between 0 and 1)

This equation calculates the output by taking a weighted average of the current input and the previous output, effectively smoothing the signal by attenuating high-frequency components.

##### Main Parameter

The primary parameter of this filter is the **filter coefficient $\alpha$**. This coefficient determines how much the filter responds to new input samples versus the accumulated past outputs.

- **When $\alpha$ is close to 1**: The filter responds more quickly to changes, allowing higher frequencies to pass through.
- **When $\alpha$ is close to 0**: The filter responds more slowly, attenuating higher frequencies and providing smoother output.

##### Relationship Between $\alpha$ and Cutoff Frequency

The cutoff frequency $f_c$ of the filter defines the frequency at which the output signal’s amplitude is reduced to 70.7% (or -3 dB) of the input signal’s amplitude. The relationship between $\alpha$, the cutoff frequency $f_c$, and the sampling frequency $f_s$ is given by:

$$
\alpha = \frac{2\pi f_c T}{2\pi f_c T + 1}
$$

Where:
- **$T$** is the sampling period ($T = \frac{1}{f_s}$).

Alternatively, solving for the cutoff frequency:

$$
f_c = \frac{1}{2\pi T} \left( \frac{\alpha}{1 - \alpha} \right)
$$

**Explanation:**

- **Low $\alpha$** (close to 0): Lower cutoff frequency, more smoothing.
- **High $\alpha$** (close to 1): Higher cutoff frequency, less smoothing.

##### Equivalent Analog Circuit

The digital low-pass filter described is analogous to a **first-order RC (resistor-capacitor) low-pass filter** in the analog domain.

**Analog RC Low-Pass Filter:**

- **Components:**
    - **Resistor (R)**
    - **Capacitor (C)**

- **Configuration:**
    - The resistor is connected in series with the input signal.
    - The capacitor is connected between the output node and ground.
    - The output is taken across the capacitor.

**Cutoff Frequency in Analog Filter:**

$$
f_c = \frac{1}{2\pi RC}
$$

**Relationship to Digital Filter:**

The time constant $\tau$ in the analog filter ($\tau = RC$) is analogous to the digital filter’s response determined by $\alpha$. By matching the time constants, you can relate the digital filter coefficient to the analog filter’s components.

#### Summary

- **Implementation:**
    - Use the recursive formula to calculate each output sample based on the current input and previous output.
- **Main Parameter:**
    - The filter coefficient $\alpha$, which controls the balance between the input and the previous output.
- **Cutoff Frequency Relation:**
    - $\alpha$ is directly related to the cutoff frequency $f_c$ and sampling frequency $f_s$.
    - Adjusting $\alpha$ changes $f_c$, allowing you to control the filter’s frequency response.
- **Equivalent Analog Circuit:**
    - A first-order RC low-pass filter with a resistor and capacitor.
    - The digital filter mimics the behavior of this analog circuit in processing discrete signals.

#### **High-pass filter**

##### Implementation

A simple digital high-pass filter can be implemented using a **first-order Infinite Impulse Response (IIR) filter** with the following difference equation:
$$
y[n] = \alpha \cdot y[n - 1] + \alpha \cdot (x[n] - x[n - 1])
$$

- **$y[n]$**: Current output sample
- **$x[n]$**: Current input sample
- **$y[n - 1]$**: Previous output sample
- **$x[n - 1]$**: Previous input sample
- **$\alpha$**: Filter coefficient (between 0 and 1)

This equation calculates the output by combining the difference between the current and previous input samples with a scaled version of the previous output. This effectively allows high-frequency components to pass through while attenuating low-frequency components.

##### Main Parameter

The primary parameter of this filter is the **filter coefficient $\alpha$**. This coefficient determines the filter’s response characteristics, particularly its cutoff frequency.

- **When $\alpha$ is close to 0**: The filter attenuates most frequencies, including higher frequencies.
- **When $\alpha$ is close to 1**: The filter allows higher frequencies to pass through more effectively, providing less attenuation of high-frequency components.

##### Relationship Between $\alpha$ and Cutoff Frequency

The cutoff frequency $f_c$ defines the frequency at which the output signal’s amplitude is reduced to 70.7% (or -3 dB) of the input signal’s amplitude. The relationship between the filter coefficient $\alpha$, the cutoff frequency $f_c$, and the sampling frequency $f_s$ is given by:

$$
\alpha = \frac{\tau}{\tau + T}
$$

Where:

- **$\tau$** is the time constant of the filter ($\tau = \frac{1}{2\pi f_c}$)
- **$T$** is the sampling period ($T = \frac{1}{f_s}$)

Substituting $\tau$ into the equation:

$$
\alpha = \frac{1}{1 + \frac{1}{2\pi f_c T}}
$$

This can also be expressed in terms of $f_c$ and $f_s$:

$$
\alpha = \frac{1}{1 + \frac{f_s}{2\pi f_c}}
$$

**Explanation:**

- **Low $\alpha$** (close to 0): Lower cutoff frequency, more attenuation of low frequencies.
- **High $\alpha$** (close to 1): Higher cutoff frequency, allowing more high-frequency components to pass.

##### Equivalent Analog Circuit

The digital high-pass filter described is analogous to a **first-order RC (resistor-capacitor) high-pass filter** in the analog domain.

**Analog RC High-Pass Filter:**

- **Components:**
    - **Capacitor (C)**
    - **Resistor (R)**

- **Configuration:**
    - The capacitor is connected in series with the input signal.
    - The resistor is connected from the output node to ground.
    - The output is taken across the resistor.

**Cutoff Frequency in Analog Filter:**

$$
f_c = \frac{1}{2\pi RC}
$$

**Relationship to Digital Filter:**

The time constant $\tau$ in the analog filter ($\tau = RC$) is analogous to the digital filter’s response determined by $\alpha$. By matching the time constants, you can relate the digital filter coefficient to the analog filter’s components.

##### Summary

- **Implementation:**
    - Use the recursive formula involving current and previous input and output samples to calculate each output sample.

- **Main Parameter:**
    - The filter coefficient $\alpha$, which controls the cutoff frequency and the balance between attenuating low frequencies and allowing high frequencies to pass.

- **Cutoff Frequency Relation:**
    - $\alpha$ is directly related to the cutoff frequency $f_c$ and the sampling frequency $f_s$. Adjusting $\alpha$ changes $f_c$, allowing you to control the filter’s frequency response.

- **Equivalent Analog Circuit:**
    - A first-order RC high-pass filter with a capacitor and a resistor. The digital filter mimics the behavior of this analog circuit in processing discrete signals.

#### **Band-pass filter**

##### Implementation

To implement a simple digital band-pass filter, you can use a **second-order Infinite Impulse Response (IIR) filter**, commonly known as a biquad filter. This filter allows frequencies within a certain range to pass through while attenuating frequencies outside that range.

The difference equation for a digital band-pass filter is:

$$
y[n] = b_0 x[n] + b_1 x[n - 1] + b_2 x[n - 2] - a_1 y[n - 1] - a_2 y[n - 2]
$$

- **$y[n]$**: Current output sample
- **$x[n]$**: Current input sample
- **$b_0, b_1, b_2$**: Feedforward coefficients
- **$a_1, a_2$**: Feedback coefficients

These coefficients are calculated based on the desired center frequency ($f_0$), quality factor ($Q$), and the sampling frequency ($f_s$).

##### Coefficient Calculation

First, compute the intermediate variables:

$$
\omega_0 = 2\pi \frac{f_0}{f_s}
$$

$$
\alpha = \frac{\sin(\omega_0)}{2Q}
$$

Where:

- **$Q$**: Quality factor, which determines the filter’s bandwidth.

The coefficients for a **band-pass filter** (constant skirt gain, peak gain = $Q$) are:

$$
b_0 = \alpha \\
b_1 = 0 \\
b_2 = -\alpha \\
a_0 = 1 + \alpha \\
a_1 = -2 \cos(\omega_0) \\
a_2 = 1 - \alpha
$$

Normalize the coefficients by dividing each by $a_0$:

$$
b_0 = \frac{b_0}{a_0} \\
b_1 = \frac{b_1}{a_0} \\
b_2 = \frac{b_2}{a_0} \\
a_1 = \frac{a_1}{a_0} \\
a_2 = \frac{a_2}{a_0}
$$

The normalized coefficients are then used in the difference equation to process the input signal.

##### Main Parameters

The main parameters of the digital band-pass filter are:

1. **Center Frequency ($f_0$)**: The frequency at which the filter has maximum gain.
2. **Quality Factor ($Q$)**: Determines the sharpness or selectivity of the filter. A higher $Q$ results in a narrower bandwidth.
3. **Sampling Frequency ($f_s$)**: The rate at which the input signal is sampled.

##### Relationship Between Parameters and Cutoff Frequencies

The bandwidth (BW) of the filter is related to the center frequency and the quality factor:

$$
BW = \frac{f_0}{Q}
$$

The lower ($f_L$) and upper ($f_H$) cutoff frequencies are:

$$
f_L = f_0 - \frac{BW}{2} \\
f_H = f_0 + \frac{BW}{2}
$$

By adjusting $Q$, you control the bandwidth of the filter around the center frequency:

- **Higher $Q$**: Narrower bandwidth, more selective filtering.
- **Lower $Q$**: Wider bandwidth, less selective filtering.

##### Equivalent Analog Circuit

The equivalent analog circuit for a band-pass filter is a **series RLC circuit** or a **parallel RLC circuit**, depending on the design.

**Series RLC Band-Pass Filter:**

- **Components:**
    - **Resistor (R)**
    - **Inductor (L)**
    - **Capacitor (C)**

- **Configuration:**
    - The resistor, inductor, and capacitor are connected in series.
    - The output is taken across the resistor or the entire series circuit.

**Analog Band-Pass Filter Characteristics:**

- **Resonant Frequency ($f_0$):**

$$
f_0 = \frac{1}{2\pi \sqrt{LC}}
$$

- **Bandwidth (BW):**

$$
BW = \frac{R}{2\pi L}
$$

- **Quality Factor ($Q$):**

$$
Q = \frac{f_0}{BW} = \frac{1}{R} \sqrt{\frac{L}{C}}
$$

The digital band-pass filter emulates the frequency-selective behavior of the analog RLC circuit in the discrete-time domain.

##### Summary

- **Implementation:**
    - Use a second-order IIR (biquad) filter with coefficients calculated based on $f_0$, $Q$, and $f_s$.
- **Main Parameters:**
    - Center frequency ($f_0$), quality factor ($Q$), and sampling frequency ($f_s$).
- **Cutoff Frequency Relation:**
    - Bandwidth ($BW = f_0 / Q$) determines the range of frequencies passed.
    - Lower and upper cutoff frequencies are $f_L = f_0 - BW/2$ and $f_H = f_0 + BW/2$.
- **Equivalent Analog Circuit:**
    - A series or parallel RLC circuit acting as a band-pass filter.
    - The digital filter replicates the frequency-selective behavior of the analog RLC circuit.

#### Notch Filter

A notch filter can be composed by combining a low-pass and a high-pass filter. The low-pass filter is used to attenuate frequencies below the notch frequency, while the high-pass filter is used to attenuate frequencies above the notch frequency. The notch frequency is the frequency that is neither attenuated nor amplified by the filter.

### 5. Noise Reduction

Noise reduction is crucial for reliable signal interpretation in cyber-physical systems:

-   **Moving Average**: A simple technique that averages a window of successive samples to smooth out noise. It is effective against high-frequency noise but can introduce lag.

-   **Adaptive Filtering**: Adaptive filters, such as the Least Mean Squares (LMS) filter, Recursive Least Squares (RLS) filter, Kalman filter, and Normalized Least Mean Squares (NLMS) filter, change their parameters based on the incoming signal to effectively minimize the noise. They are useful when noise characteristics change over time.

### 6. Correlation

**Correlation** measures the similarity between two signals, which is particularly helpful in pattern recognition and synchronization tasks.

-   **Cross-correlation** measures the similarity between two different signals as a function of the time-lag applied to one of them, which can help identify repeating patterns or align signals.

-   **Autocorrelation** is used to find repeating patterns within a single signal, like identifying the fundamental period in a periodic signal.

-   Correlation can be performed using convolution, as it is mathematically equivalent to convolution with a time-reversed signal. Additionally, correlation can be computed efficiently in the frequency domain using Fourier transforms.

### 7. Autoregressive Modeling

**Autoregressive (AR) models** predict future values in a time series by using past values. An AR model uses a linear combination of previous data points to forecast future points.

-   In real-time applications, AR models are used for **predictive maintenance**, where future signal behavior is estimated based on historical data. This approach is also used in noise reduction and system identification.

### 8. Decimation and Interpolation

**Decimation** and **interpolation** are techniques used to change the sampling rate of a signal.

-   **Decimation** involves reducing the number of samples in a signal by a factor, effectively downsampling it. It is useful in reducing the amount of data for processing while maintaining the essential characteristics of the signal. Common methods for decimation include:

-   **Averaging Decimation**: Averaging a group of consecutive samples to reduce the sampling rate while preserving the overall signal characteristics.

-   **Decimation by a Factor**: Keeping every Nth sample and discarding the others, often followed by a low-pass filter to prevent aliasing.

-   **CIC (Cascaded Integrator-Comb) Filter**: A computationally efficient filter structure used in hardware implementations for decimation, especially in high-speed digital signal processing.

-   **Interpolation** involves increasing the number of samples in a signal, effectively upsampling it. It is used when a higher sampling rate is needed, often followed by low-pass filtering to smooth the upsampled signal. Common methods for interpolation include:

-   **Zero-Order Hold (ZOH)**: Repeats each sample value for the duration of the new sampling interval.

-   **Linear Interpolation**: Estimates intermediate values by linearly connecting adjacent samples.

-   **Polynomial Interpolation**: Uses higher-order polynomials to estimate new sample values, providing a smoother result compared to linear interpolation.

-   **Spline Interpolation**: Uses piecewise polynomials (splines) for interpolation, ensuring smoothness at the boundaries between intervals.

### 9. Modulation and Demodulation

**Modulation** is the process of altering a carrier signal to encode information, and **demodulation** is the reverse process to extract the information from the modulated signal.

-   **Amplitude Modulation (AM)** and **Frequency Modulation (FM)** are common techniques used for transmitting data over communication channels.

-   In cyber-physical systems, modulation is used for **wireless communication**, where sensor data is transmitted over a distance. Proper modulation helps in efficient and robust data transfer, especially in environments with significant interference.

## State Space

In a CPS, the "state" represents all the information required to describe the system’s current condition. This could include physical quantities like position, velocity, temperature, and electrical currents, as well as digital aspects like mode states or error conditions.

-   **Coordinate System Selection**: Selecting an appropriate coordinate system is crucial for accurately representing the system state. The choice of coordinate system can simplify the representation of system dynamics and facilitate efficient state estimation, especially for complex systems with multiple degrees of freedom.

-   **Degrees of Freedom (DoF)**: Degrees of freedom represent the number of independent variables that define the state of a system. Understanding and correctly modeling the DoF is essential to accurately describe the system state and effectively estimate it in real-time applications.

-   **State-Space vs. Configuration Space**: The system state can be represented in different forms, such as **state-space** or **configuration space**. State-space representation includes all the dynamic variables (e.g., positions and velocities), whereas configuration space focuses on the possible positions or configurations of the system. Choosing the appropriate representation depends on the application and the nature of the system being analyzed.

### Modeling State Space

**State space representation** is a mathematical framework used to model and analyze dynamic systems. It expresses a system’s dynamics using a set of first-order differential (or difference) equations in terms of state variables, inputs, and outputs. This representation is particularly powerful for complex systems, especially those with multiple inputs and outputs (MIMO systems), time-varying parameters, or nonlinearities.

### Key Components:

1. **State Variables ($\mathbf{x}(t)$ or $\mathbf{x}[k]$)**:

    - Represent the smallest set of variables that describe the system’s current state.
    - Capture all the necessary information to predict future behavior, given the inputs.

2. **Input Variables ($\mathbf{u}(t)$ or $\mathbf{u}[k]$)**:

    - External signals or controls applied to the system.

3. **Output Variables ($\mathbf{y}(t)$ or $\mathbf{y}[k]$)**:

    - Measurable signals or quantities of interest derived from the system.

4. **System Matrices**:

    - **$\mathbf{A}$**: State matrix (defines the system dynamics).
    - **$\mathbf{B}$**: Input matrix (how inputs affect states).
    - **$\mathbf{C}$**: Output matrix (how states affect outputs).
    - **$\mathbf{D}$**: Feedthrough (or direct transmission) matrix (direct input-output relationship).

### General Form:

#### Continuous-Time Systems:

**State Equation**:

$$\dot{\mathbf{x}}(t) = \mathbf{A}\mathbf{x}(t) + \mathbf{B}\mathbf{u}(t)$$

**Output Equation**:

$$\mathbf{y}(t) = \mathbf{C}\mathbf{x}(t) + \mathbf{D}\mathbf{u}(t)$$

#### Discrete-Time Systems:

**State Equation**:

$$\mathbf{x}[k+1] = \mathbf{A}\mathbf{x}[k] + \mathbf{B}\mathbf{u}[k]$$

**Output Equation**:

$$\mathbf{y}[k] = \mathbf{C}\mathbf{x}[k] + \mathbf{D}\mathbf{u}[k]$$

### Advantages of State Space Representation:
- Handles complex systems with multiple inputs and outputs.
- Suitable for time-varying and nonlinear systems.
- Facilitates modern control design techniques like state feedback and observers.

-   **Handles Complex Systems**: Suitable for MIMO systems and higher-order systems without the complexity of transfer functions.

-   **Time-Varying and Nonlinear Systems**: Can model systems where parameters change over time or with the state.

-   **Modern Control Design**: Facilitates advanced control strategies like state feedback, observers, and optimal control.

### Example: Mass-Spring-Damper System

Consider a mechanical system described by the second-order differential equation:

$$m\ddot{x}(t) + c\dot{x}(t) + kx(t) = u(t)$$

Where:

-   $x(t)$: Position of the mass.
-   $u(t)$: External force applied.
-   $m$: Mass.
-   $c$: Damping coefficient.
-   $k$: Spring constant.

**Step 1: Define State Variables**

Let:

-   $x_1(t) = x(t)$ (Position)
-   $x_2(t) = \dot{x}(t)$ (Velocity)

**Step 2: Derive State Equations**

Express the system as first-order differential equations:

1.  $\dot{x}_1(t) = x_2(t)$
2.  $\dot{x}_2(t) = -\dfrac{k}{m} x_1(t) - \dfrac{c}{m} x_2(t) + \dfrac{1}{m} u(t)$

**Step 3: Write in Matrix Form**

$$
\begin{bmatrix} 
\dot{x}_1(t) \\ 
\dot{x}_2(t) 
\end{bmatrix} = 
\begin{bmatrix} 
0 & 1 \\ 
-\dfrac{k}{m} & -\dfrac{c}{m} 
\end{bmatrix} 
\begin{bmatrix} 
x_1(t) \\ 
x_2(t) 
\end{bmatrix} + 
\begin{bmatrix} 
0 \\ 
\dfrac{1}{m} 
\end{bmatrix} u(t)
$$

**Output Equation** (Assuming output is position):

$$
y(t) = \begin{bmatrix} 1 & 0 \end{bmatrix} 
\begin{bmatrix} 
x_1(t) \\ 
x_2(t) 
\end{bmatrix}
$$

### Interpretation:

-   **State Vector** ($\mathbf{x}(t)$): Encapsulates the system’s current position and velocity.

-   **State Matrix** ($\mathbf{A}$): Describes how the current state affects the rate of change of the state.

-   **Input Matrix** ($\mathbf{B}$): Shows how the external force influences the state.

-   **Output Matrix** ($\mathbf{C}$): Relates the state to the measurable output.

-   **Feedthrough Matrix** ($\mathbf{D}$): Zero in this case, indicating no direct input-to-output path.

### Why Use State Space Representation?

-   **Unified Framework**: Offers a consistent method to model various types of systems.

-   **Computational Efficiency**: Suitable for numerical simulations and computer-based analysis.

-   **Control Design**: Essential for designing controllers that modify the system’s behavior based on its state (e.g., feedback control).

### Observability

The ability to estimate the complete internal state of the system based on the available sensor measurements is known as **observability**. State estimation aims to make sure the state of the system is accurately tracked, even when some internal variables are not directly measurable.

## Observability in State Space Representation

**Observability** is a fundamental concept in control theory and state-space analysis. It determines whether the internal states of a dynamic system can be inferred by observing its external outputs over time. In both continuous-time and discrete-time systems, observability plays a crucial role in system analysis, controller design, and state estimation.

-   **Observable System**: A system is said to be observable if the current state can be determined in finite time using only the outputs and inputs.

-   **Unobservable System**: If some states cannot be reconstructed from the outputs and inputs, the system is unobservable.

Consider a linear time-invariant (LTI) system represented in state-space form for both continuous-time and discrete-time systems, where the system is given by the state vector ($\mathbf{x}(t)$), state matrix ($\mathbf{A}$), input matrix ($\mathbf{B}$), output matrix ($\mathbf{C}$), and feedthrough matrix ($\mathbf{D}$).

The steps for determining observability are as follows:

1. **Construct Observability Matrix $\mathcal{O}$**:
    - Calculate $\mathbf{C}$, $\mathbf{C}\mathbf{A}$, $\mathbf{C}\mathbf{A}^2$, …​, $\mathbf{C}\mathbf{A}^{n-1}$.

2. **Calculate Rank of $\mathcal{O}$**:
    - Use matrix rank determination methods (e.g., Gaussian elimination, singular value decomposition).

3. **Assess Observability**:
    - If rank $\mathcal{O} = n$, the system is observable.
    - If rank $\mathcal{O} < n$, the system is unobservable.

### Observability Matrix

The observability of a system can be assessed using the **Observability Matrix**, $\mathcal{O}$, which is constructed as:

$$
\mathcal{O} = \begin{bmatrix} 
\mathbf{C} \\ 
\mathbf{C}\mathbf{A} \\ 
\mathbf{C}\mathbf{A}^2 \\ 
\vdots \\ 
\mathbf{C}\mathbf{A}^{n-1} 
\end{bmatrix}
$$

- $n$ is the number of state variables in the system.
- The matrix $\mathcal{O}$ has dimensions $n \times n$ for single-output systems.

### Observability Criterion

- **A system is observable if and only if** the observability matrix $\mathcal{O}$ has full rank (i.e., rank $n$).
- If $\mathcal{O}$ is rank-deficient (rank less than $n$), the system is unobservable.

### Interpretation

-   **Full Rank**: Every state contributes uniquely to the output, allowing reconstruction of the entire state vector.

-   **Rank Deficient**: Some states do not influence the output sufficiently, making them unobservable.

### Examples

#### Continuous-Time System Example

**System Matrices**:

$$\mathbf{A} = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}, \quad \mathbf{C} = \begin{bmatrix} 1 & 0 \end{bmatrix}$$

**Construct Observability Matrix**:

$$\mathcal{O} = \begin{bmatrix} \mathbf{C} \\ \mathbf{C}\mathbf{A} \end{bmatrix} = \begin{bmatrix} 1 & 0 \\ 1 \times 0 + 0 \times (-2) & 1 \times 1 + 0 \times (-3) \end{bmatrix} = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}$$

**Analysis**:

- The observability matrix $\mathcal{O}$ has full rank (rank 2).

- **Conclusion**: The system is observable.

#### Discrete-Time System Example

**System Matrices**:

$$\mathbf{A} = \begin{bmatrix} 1 & 0 \\ 0 & \lambda \end{bmatrix}, \quad \mathbf{C} = \begin{bmatrix} 0 & 1 \end{bmatrix}$$

Assume $\lambda$ is a scalar.

**Construct Observability Matrix**:

$$\mathcal{O} = \begin{bmatrix} \mathbf{C} \\ \mathbf{C}\mathbf{A} \end{bmatrix} = \begin{bmatrix} 0 & 1 \\ 0 \times 1 + 1 \times 0 & 0 \times 0 + 1 \times \lambda \end{bmatrix} = \begin{bmatrix} 0 & 1 \\ 0 & \lambda \end{bmatrix}$$

**Analysis**:

- The rank of $\mathcal{O}$ depends on $\lambda$.

- If $\lambda \neq 0$, the rank is 2, and the system is observable.

- If $\lambda = 0$, the rank is 1, and the system is unobservable.

**Conclusion**:

- The system’s observability depends on the value of $\lambda$.

### Importance of Observability

-   **State Estimation**: Necessary for designing observers or estimators (e.g., Luenberger observer, Kalman filter) to estimate the internal states.

-   **Control Design**: Essential for implementing state feedback controllers when not all states are measured directly.

-   **System Diagnostics**: Helps in fault detection and system monitoring by ensuring that all states can be observed.

### Practical Considerations

-   **Sensor Placement**: Adequate and strategic placement of sensors can improve observability.

-   **Noise and Disturbances**: Real-world measurements are affected by noise, impacting state estimation accuracy.

-   **Time-Varying Systems**: For time-varying systems, observability may change over time and requires time-dependent analysis.

## Sensors and Uncertainty

Sensors provide data to estimate the system state, but real-world sensors often have inaccuracies, delays, and noise. State estimation techniques are used to reduce the impact of these uncertainties and provide a more reliable understanding of the system state.

### Kalman Filter

One of the most common methods for state estimation in CPS is the **Kalman Filter**. The Kalman Filter is used to estimate the state of a system by combining sensor measurements with a mathematical model of the system dynamics. It does this in two steps:

-   **Prediction**: The system model is used to predict the future state based on previous estimates.

-   **Update**: The prediction is adjusted using new sensor measurements, correcting the estimate based on observed data and uncertainty levels.

For non-linear systems, an **Extended Kalman Filter (EKF)** or **Unscented Kalman Filter (UKF)** may be used, which handle the non-linearities in the prediction or update steps.

### Particle Filter

In more complex, highly non-linear systems where the Kalman Filter cannot be effectively applied, **Particle Filters** can be used for state estimation. Particle filters use a set of random samples (particles) to approximate the probability distribution of the system state.

### State Estimation in Control

State estimation is crucial for feedback control. Many control systems require information about variables that cannot be directly measured, such as velocity or acceleration. For example, in an autonomous vehicle, a state estimator can predict the vehicle’s speed and orientation based on GPS, inertial sensors, and control inputs.

### State-Space Representation

State-space representation is a mathematical model that describes the internal state of a system using a set of first-order differential or difference equations. In a state-space model, the system is represented by state variables, input variables, and output variables, which are organized into vector form. This approach is particularly useful for modeling multi-input, multi-output (MIMO) systems, and provides a unified framework for analyzing both linear and non-linear dynamics. The state-space representation is essential for designing modern control systems and implementing state estimation techniques like the Kalman Filter, as it allows for a compact and efficient representation of the system’s dynamic behavior.

### Applications

-   **Robotics**: Estimating the position, velocity, and orientation of a robot in environments where direct measurement might not be possible.

-   **Automotive Systems**: State estimation for vehicle stability, adaptive cruise control, and other driver assistance systems.

-   **Power Systems**: Monitoring the internal state of power grids to ensure stability, detect faults, and adjust loads.

-   **Smart Manufacturing**: Estimating the health and operational state of machinery based on sensor data, which helps in predictive maintenance and process optimization.

State estimation is essential for achieving robustness, reliability, and real-time responsiveness in cyber-physical systems. By combining sensor data with system models, state estimation enables accurate monitoring, enhances control performance, and helps systems deal with sensor inaccuracies and unexpected disturbances.

