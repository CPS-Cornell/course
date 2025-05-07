import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 1. Generate Data
np.random.seed(42) # for reproducibility
signal_length = 100
# Create a step signal
signal = np.zeros(signal_length)
signal[signal_length // 3 : 2 * signal_length // 3] = 1.0
# Add noise
noise = np.random.normal(0, 0.2, signal_length)
noisy_signal = signal + noise
time = np.arange(signal_length)

# 2. Define Edge Detection Kernel
# Introduce variable kernel length (must be even)
edge_kernel_length = 14 # Example: length 6 -> [1, 1, 1, -1, -1, -1]
if edge_kernel_length % 2 != 0:
    raise ValueError("edge_kernel_length must be an even number")

half_len = edge_kernel_length // 2
edge_kernel = np.concatenate([-np.ones(half_len), np.ones(half_len)])/(edge_kernel_length/2)

# Update kernel size and radius based on the new kernel
kernel_size = len(edge_kernel)
kernel_radius = kernel_size // 2 # Note: For even kernels, the 'center' is between elements
# Adjust kernel_plot_indices if precise centering visualization is needed for even kernels
# For simplicity, we keep the previous definition, which works but might look slightly off-center visually
kernel_plot_indices = np.arange(kernel_size) - kernel_radius


# Create the output array for edge detection results, initialized to zeros
edge_signal = np.zeros_like(noisy_signal)

# 3. Set up Plot
# Change to 2 subplots
fig, axs = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
# Update title
fig.suptitle('1D Edge Detection Convolution Demo')

# Plot 0: Original Noisy Signal and Sliding Kernel Shape
# Change plot to scatter-like points
axs[0].plot(time, noisy_signal, 'bo', markersize=4, alpha=0.7, label='Noisy Signal')
# Line to show the kernel's position/influence on the signal points
kernel_influence_line, = axs[0].plot([], [], color='red', lw=2, alpha=0.6, label='Kernel Influence')
# Line to show the actual kernel shape sliding
sliding_kernel_line, = axs[0].plot([], [], color='orange', lw=2, label='Sliding Edge Kernel')
axs[0].set_ylabel('Amplitude')
axs[0].legend(loc='upper left')
axs[0].grid(True)
# Adjust ylim to make space for kernel shape visualization if needed
ymin, ymax = axs[0].get_ylim()
axs[0].set_ylim(ymin - 0.5, ymax + 0.5) # Add some padding

# Plot 1: Edge Detection Result
axs[1].plot(time, np.zeros_like(time), 'k--', alpha=0.5) # Add a zero line for reference
# Update labels and plot variables
edge_line, = axs[1].plot([], [], color='purple', lw=2, label='Detected Edges')
current_edge_point_marker, = axs[1].plot([], [], 'mo', markersize=8) # Marker for the current point being calculated
axs[1].set_xlabel('Time / Index')
axs[1].set_ylabel('Edge Strength') # Update y-label
axs[1].legend(loc='upper left')
axs[1].grid(True)
# Adjust ylim for edge signal which can be positive or negative
axs[1].set_ylim(-1.5, 1.5) # Adjust based on expected edge strength range

plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Adjust layout

# 4. Animation Function
def update(frame):
    # frame represents the center index of the kernel on the signal
    center_index = frame

    # --- Update Plot 0: Kernel Influence and Sliding Shape ---
    # Adjust index calculation for potentially even kernel size if needed
    # The current calculation might slightly shift the visual center for even kernels
    start_idx = center_index - kernel_radius + 1 # Adjust start for even kernel centering if needed
    end_idx = center_index + kernel_radius + 1 # Adjust end for even kernel centering if needed
    kernel_indices_signal = np.arange(start_idx, end_idx)
    valid_indices_mask = (kernel_indices_signal >= 0) & (kernel_indices_signal < signal_length)

    # Update the line showing which signal points are under the kernel
    kernel_influence_line.set_data(kernel_indices_signal[valid_indices_mask],
                                   noisy_signal[kernel_indices_signal[valid_indices_mask]])

    # Update the sliding kernel shape
    kernel_y_offset = 0.0 # Place kernel shape base at y=0
    scaled_kernel = edge_kernel * 0.5 # Keep scaling or adjust as needed
    # Adjust x-position for visual centering with even kernel if desired
    sliding_kernel_line.set_data(kernel_plot_indices + center_index + 0.5, scaled_kernel + kernel_y_offset) # Added 0.5 offset

    # --- Calculate Convolution Step (Edge Detection) ---
    signal_segment = np.zeros(kernel_size)
    # Adjust loop range for potentially even kernel size if needed
    for i, k_idx in enumerate(range(-kernel_radius + 1, kernel_radius + 1)): # Adjusted range potentially
        signal_idx = center_index + k_idx
        if 0 <= signal_idx < signal_length:
            # Map kernel index 'i' correctly to signal segment index
            segment_idx = i # Check if this mapping is correct for the adjusted range
            signal_segment[segment_idx] = noisy_signal[signal_idx]
        # else: signal_segment remains 0 (zero-padding)

    # Element-wise multiplication and Summation for edge detection
    # Ensure signal_segment aligns correctly with edge_kernel for multiplication
    edge_value = np.sum(signal_segment * edge_kernel)
    edge_signal[center_index] = edge_value

    # --- Update Plot 1: Edge Signal ---
    # Update plot variables
    edge_line.set_data(time[:center_index + 1], edge_signal[:center_index + 1])
    current_edge_point_marker.set_data([center_index], [edge_value])

    # Update titles
    axs[0].set_title(f'Kernel centered at index {center_index}')
    # Update title for edge value
    axs[1].set_title(f'Edge Detection Output (Value = {edge_value:.2f})')

    # Return the updated artists
    # Update returned artists
    return kernel_influence_line, sliding_kernel_line, edge_line, current_edge_point_marker

# 5. Run Animation
# We iterate through each possible center position of the kernel
# Blit=True requires the update function to return an iterable of all modified artists.
ani = animation.FuncAnimation(fig, update, frames=signal_length,
                              interval=200, blit=True, repeat=False)

# To save the animation (optional, requires ffmpeg or imagemagick)
# Update filename
# Ensure you have ffmpeg installed and in your system's PATH to save as mp4
ani.save('edge_detection_1d.gif', writer='imagemagick', fps=5)
# ani.save('edge_detection_1d.mp4', writer='ffmpeg', fps=15)

plt.show()
