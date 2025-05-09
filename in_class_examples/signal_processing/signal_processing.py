import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd

def generate_building_accelerometer_data(duration=60, fs=1000, 
                                         resonant_freqs=[1.5, 3.8, 7.2], 
                                         amplitudes=[0.8, 0.5, 0.3], 
                                         noise_level=0.8):
    """
    Generate synthetic accelerometer data from a building with multiple resonant frequencies and noise.
    
    Parameters:
    -----------
    duration : float
        Duration of the signal in seconds
    fs : int
        Sampling frequency in Hz
    resonant_freqs : list
        List of resonant frequencies of the building in Hz
    amplitudes : list
        Amplitudes for each resonant frequency
    noise_level : float
        Standard deviation of the Gaussian noise
    
    Returns:
    --------
    time : ndarray
        Time vector
    accel : ndarray
        Accelerometer data in m/s^2
    """
    # Create time vector
    t = np.arange(0, duration, 1/fs)
    
    # Initialize acceleration signal
    accel = np.zeros_like(t)
    
    # Add each resonant frequency component
    for freq, amp in zip(resonant_freqs, amplitudes):
        # Add some randomness to the phase
        phase = np.random.uniform(0, 2*np.pi)
        # Add sinusoidal component
        accel += amp * np.sin(2 * np.pi * freq * t + phase)
    
    # Add random Gaussian noise
    noise = np.random.normal(0, noise_level, len(t))
    accel += noise
    
    # Add some random spikes to simulate impulse disturbances
    num_spikes = int(duration / 10)  # One spike every 10 seconds on average
    spike_indices = np.random.choice(len(t), num_spikes, replace=False)
    spike_amplitudes = np.random.uniform(1.0, 2.0, num_spikes) * np.random.choice([-1, 1], num_spikes)
    accel[spike_indices] += spike_amplitudes
    
    return t, accel

def calculate_fft(signal_data, fs):
    """
    Calculate the FFT of a signal.
    
    Parameters:
    -----------
    signal_data : ndarray
        Input signal
    fs : int
        Sampling frequency in Hz
    
    Returns:
    --------
    freq : ndarray
        Frequency vector
    magnitude : ndarray
        Magnitude of the FFT
    """
    n = len(signal_data)
    fft_result = np.fft.fft(signal_data)
    # Take only the first half (positive frequencies)
    magnitude = 2.0/n * np.abs(fft_result[:n//2])
    freq = np.fft.fftfreq(n, 1/fs)[:n//2]
    
    return freq, magnitude

def apply_bandpass_filter(signal_data, fs, lowcut, highcut, order=4):
    """
    Apply a bandpass filter to the signal.
    
    Parameters:
    -----------
    signal_data : ndarray
        Input signal
    fs : int
        Sampling frequency in Hz
    lowcut : float
        Low cutoff frequency in Hz
    highcut : float
        High cutoff frequency in Hz
    order : int
        Filter order
        
    Returns:
    --------
    filtered_signal : ndarray
        Filtered signal
    """
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = signal.butter(order, [low, high], btype='band')
    filtered_signal = signal.filtfilt(b, a, signal_data)
    return filtered_signal

def plot_time_domain(t, accel, title="Building Acceleration Time Series"):
    """Plot time domain signal"""
    plt.figure(figsize=(10, 4))
    plt.plot(t, accel)
    plt.xlabel("Time (s)")
    plt.ylabel("Acceleration (m/s²)")
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()

def plot_freq_domain(freq, magnitude, title="Frequency Spectrum"):
    """Plot frequency domain signal"""
    plt.figure(figsize=(10, 4))
    plt.plot(freq, magnitude)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.title(title)
    plt.grid(True)
    plt.xlim(0, 20)  # Limiting to 20 Hz for better visualization
    plt.tight_layout()

def plot_spectrogram(signal_data, fs, title="Spectrogram"):
    """Plot spectrogram of the signal"""
    plt.figure(figsize=(10, 6))
    plt.specgram(signal_data, Fs=fs, NFFT=1024, noverlap=512, cmap='jet')
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.title(title)
    plt.ylim(0, 20)  # Limiting to 20 Hz for better visualization
    plt.colorbar(label="Power/Frequency (dB/Hz)")
    plt.tight_layout()

def signal_processing_demo():
    """Main function to demonstrate signal processing on building accelerometer data"""
    # Parameters
    duration = 60  # seconds
    fs = 1000      # Hz (samples per second)
    
    # Generate synthetic data
    print("Generating synthetic accelerometer data...")
    t, accel = generate_building_accelerometer_data(
        duration=duration, 
        fs=fs, 
        resonant_freqs=[1.5, 3.8, 7.2],  # Building resonant frequencies in Hz
        amplitudes=[0.8, 0.5, 0.3],      # Amplitudes for each frequency
        noise_level=5                  # Noise level
    )
    
    # Perform FFT analysis
    print("Performing frequency domain analysis...")
    freq, magnitude = calculate_fft(accel, fs)
    
    # Apply bandpass filter to isolate main resonant frequency
    print("Applying bandpass filter...")
    filtered_signal = apply_bandpass_filter(accel, fs, 1.0, 2.0, order=4)
    
    # Apply low-pass filter to remove high-frequency noise
    print("Applying low-pass filter...")
    nyquist = 0.5 * fs
    cutoff = 10.0 / nyquist
    b, a = signal.butter(4, cutoff, btype='low')
    lowpass_filtered = signal.filtfilt(b, a, accel)

    freq_filtered, magnitude_filtered = calculate_fft(lowpass_filtered, fs)
    
    # Plot results
    print("Plotting results...")
    plot_time_domain(t, accel, "Raw Building Accelerometer Data")
    plot_freq_domain(freq, magnitude, "Frequency Spectrum of Accelerometer Data")
    plot_freq_domain(freq_filtered, magnitude_filtered, "Frequency Spectrum of Filtered Accelerometer Data")
    plot_time_domain(t, lowpass_filtered, "Low-pass Filtered (10 Hz cutoff)")
    plot_spectrogram(accel, fs, "Spectrogram of Building Accelerometer Data")
    
    # Save data to CSV for students to use
    df = pd.DataFrame({'time': t, 'acceleration': accel})
    df.to_csv('building_accelerometer_data.csv', index=False)
    print("Data saved to 'building_accelerometer_data.csv'")
    
    plt.show()

if __name__ == "__main__":
    signal_processing_demo()
