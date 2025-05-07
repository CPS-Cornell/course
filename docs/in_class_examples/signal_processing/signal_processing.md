# Building Accelerometer Signal Processing ([`signal_processing.py`](signal_processing.py))

This document explains how the `signal_processing.py` script works to analyze vibration data from buildings.

## Overview

The script demonstrates common signal processing techniques applied to building accelerometer data, including:
- Generating synthetic accelerometer data with multiple resonant frequencies
- Performing Fast Fourier Transform (FFT) analysis
- Applying filters to isolate frequencies of interest
- Visualizing signals in time domain, frequency domain, and time-frequency domain (spectrograms)

## Function Breakdown

### Data Generation

The `generate_building_accelerometer_data()` function creates synthetic acceleration data that mimics what might be captured from a building's structural monitoring system. It:

1. Creates sinusoidal waves at specified resonant frequencies (typically 1.5Hz, 3.8Hz, and 7.2Hz for buildings)
2. Adds random Gaussian noise to simulate sensor noise
3. Inserts occasional spikes to simulate impulse disturbances (like door slams or equipment impacts)

### Signal Processing Techniques

#### FFT Analysis
The `calculate_fft()` function converts the time-domain signal to the frequency domain using Fast Fourier Transform, allowing identification of dominant frequencies in the building's response.

#### Filtering
Two filtering approaches are demonstrated:
- `apply_bandpass_filter()`: Isolates a specific frequency range (e.g., around the fundamental frequency)
- Lowpass filtering: Removes high-frequency noise while preserving the structural response

### Visualization

The script provides three visualization functions:
- `plot_time_domain()`: Shows acceleration vs. time
- `plot_freq_domain()`: Shows the frequency spectrum (magnitude vs. frequency)
- `plot_spectrogram()`: Shows how frequency content changes over time

### Main Workflow

The `signal_processing_demo()` function ties everything together:

1. Generates 60 seconds of synthetic building accelerometer data at 1000Hz sampling rate
2. Performs FFT to identify frequency components
3. Applies filters to clean the signal and isolate frequencies of interest
4. Creates visualizations of both raw and processed data
5. Saves the data to a CSV file for further analysis

## Applications

This type of signal processing is valuable for:
- Structural health monitoring
- Identifying building resonant frequencies
- Detecting changes in structural behavior over time
- Filtering out noise from meaningful structural responses

## Usage

Run the script directly to see all visualizations and generate the CSV file:

```python
python signal_processing.py
```
