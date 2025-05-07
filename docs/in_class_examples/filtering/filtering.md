# 1D Signal Filtering Examples

This directory contains interactive demonstrations of various 1D filtering techniques commonly used in signal processing.

## [`mean_filter.py`](mean_filter.py)

### Moving Average Filter Demonstration

This script demonstrates how a moving average filter (box filter) works on a 1D signal.

**Explanation:**
- **Signal Creation**: Generates a step signal with random Gaussian noise.
- **Filter Implementation**: Uses a uniform kernel (all coefficients equal) normalized to sum to 1.
- **Visualization**: Shows the filtering process step by step with animation:
  - Top plot: Shows the noisy signal with the sliding kernel/window.
  - Bottom plot: Shows the filtered output being built as the kernel moves through the signal.
- **How it Works**: As the kernel slides across the input signal, each output point is calculated as the average of signal values within the window.
- **Effect**: Moving average smooths the signal by reducing high-frequency noise, but also blurs edges.

**Mathematical Process**: The output at each position is the weighted sum of neighboring input values, with all weights equal to 1/window_size.

## [`gaussian_filter.py`](gaussian_filter.py)

### Gaussian Filter Demonstration

This script demonstrates how a Gaussian filter works on a 1D signal.

**Explanation:**
- **Signal Creation**: Same step signal with noise as in the mean filter.
- **Filter Implementation**: Uses a Gaussian kernel where weights follow a Gaussian (normal) distribution.
- **Visualization**: Similar animation to the mean filter:
  - Top plot: Shows the noisy signal with the bell-shaped Gaussian kernel sliding across.
  - Bottom plot: Shows the filtered output.
- **How it Works**: Similar to moving average, but input values closer to the center are weighted more heavily.
- **Effect**: Smooths noise while better preserving edges compared to the moving average filter.

**Mathematical Process**: The Gaussian filter applies weights according to a Gaussian distribution, giving more importance to pixels near the center of the kernel.

## [`edge_detection.py`](edge_detection.py)

### Edge Detection Filter Demonstration

This script demonstrates how edge detection works using a simple edge detection kernel.

**Explanation:**
- **Signal Creation**: Same step signal with noise as previous examples.
- **Filter Implementation**: Uses a kernel with negative values on one side and positive values on the other side.
- **Visualization**:
  - Top plot: Shows the noisy signal with the bipolar edge kernel sliding across.
  - Bottom plot: Shows the edge detection output.
- **How it Works**: The kernel responds strongly at points where the signal changes rapidly (edges).
  - Positive peaks: Rising edges
  - Negative peaks: Falling edges
  - Near-zero values: Flat regions
- **Effect**: Highlights areas of rapid change in the signal.

**Mathematical Process**: The edge detection works by calculating the difference between signal regions on either side of the current position, emphasizing discontinuities.

## Key Differences Between Filters

1. **Moving Average Filter**: Simple averaging with equal weights; good noise reduction but blurs edges.
2. **Gaussian Filter**: Weighted averaging with bell curve distribution; better edge preservation than box filter.
3. **Edge Detection**: Highlights changes in the signal; amplifies edges rather than smoothing them.

All three examples use the convolution operation, which is fundamental to signal and image processing.
