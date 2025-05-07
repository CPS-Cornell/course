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

# 2. Define Moving Average Kernel (Window)
window_size = 18 # Define the size of the moving average window (must be odd)
if window_size % 2 == 0:
    window_size += 1 # Ensure window size is odd

# Create a uniform kernel (all elements equal)
kernel = np.ones(window_size)
kernel /= np.sum(kernel) # Normalize the kernel (sum = 1)
kernel_radius = window_size // 2
kernel_plot_indices = np.arange(window_size) - kernel_radius # x-values for kernel plot (-radius to +radius)


# Create the output array, initialized to zeros
filtered_signal = np.zeros_like(noisy_signal)

# 3. Set up Plot
# Change to 2 subplots
fig, axs = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
# Update title
fig.suptitle('1D Moving Average Filter Demo')

# Plot 0: Original Noisy Signal and Sliding Kernel Shape
# Change plot to scatter-like points
axs[0].plot(time, noisy_signal, 'bo', markersize=4, alpha=0.7, label='Noisy Signal')
# Line to show the kernel's position/influence on the signal points
kernel_influence_line, = axs[0].plot([], [], color='red', lw=2, alpha=0.6, label='Window Influence')
# Line to show the actual kernel shape sliding
sliding_kernel_line, = axs[0].plot([], [], color='orange', lw=2, label='Sliding Window Shape')
axs[0].set_ylabel('Amplitude')
axs[0].legend(loc='upper left')
axs[0].grid(True)
# Adjust ylim to make space for kernel shape visualization if needed
ymin, ymax = axs[0].get_ylim()
axs[0].set_ylim(ymin - 0.5, ymax + 0.5) # Add some padding

# Plot 1: Filtered Signal (previously Plot 2)
axs[1].plot(time, noisy_signal, label='Noisy Signal', color='blue', alpha=0.3) # Show original for reference
filtered_line, = axs[1].plot([], [], color='green', lw=2, label='Filtered Signal (Moving Avg)')
current_point_marker, = axs[1].plot([], [], 'go', markersize=8) # Marker for the current point being calculated
axs[1].set_xlabel('Time / Index')
axs[1].set_ylabel('Amplitude')
axs[1].legend(loc='upper left')
axs[1].grid(True)

plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Adjust layout

# 4. Animation Function
def update(frame):
    # frame represents the center index of the kernel on the signal
    center_index = frame

    # --- Update Plot 0: Kernel Influence and Sliding Shape ---
    kernel_indices_signal = np.arange(center_index - kernel_radius, center_index + kernel_radius + 1)
    valid_indices_mask = (kernel_indices_signal >= 0) & (kernel_indices_signal < signal_length)

    # Update the line showing which signal points are under the kernel
    kernel_influence_line.set_data(kernel_indices_signal[valid_indices_mask],
                                   noisy_signal[kernel_indices_signal[valid_indices_mask]])

    # Update the sliding kernel shape
    # Scale kernel values to be visible on the signal plot, place it at y=0
    kernel_y_offset = 0.0 # Place kernel shape base at y=0
    # Adjust scaling if needed for uniform kernel visibility
    scaled_kernel = kernel * 2.0 # Scale kernel height for visibility
    sliding_kernel_line.set_data(kernel_plot_indices + center_index, scaled_kernel + kernel_y_offset)

    # --- Calculate Convolution Step (Moving Average) ---
    # Get the segment of the signal under the kernel, handling boundaries with zero-padding
    signal_segment = np.zeros(window_size) # Use window_size
    for i, k_idx in enumerate(range(-kernel_radius, kernel_radius + 1)):
        signal_idx = center_index + k_idx
        if 0 <= signal_idx < signal_length:
            signal_segment[i] = noisy_signal[signal_idx]
        # else: signal_segment[i] remains 0 (zero-padding)

    # Element-wise multiplication and Summation (effectively averaging due to normalized kernel)
    convolution_value = np.sum(signal_segment * kernel)
    filtered_signal[center_index] = convolution_value

    # --- Update Plot 1: Filtered Signal ---
    filtered_line.set_data(time[:center_index + 1], filtered_signal[:center_index + 1])
    current_point_marker.set_data([center_index], [convolution_value])

    # Update titles
    axs[0].set_title(f'Window centered at index {center_index}')
    axs[1].set_title(f'Filtered Output (Value = {convolution_value:.2f})')

    # Return the updated artists
    return kernel_influence_line, sliding_kernel_line, filtered_line, current_point_marker

# 5. Run Animation
# We iterate through each possible center position of the kernel
# Blit=True requires the update function to return an iterable of all modified artists.
ani = animation.FuncAnimation(fig, update, frames=signal_length,
                              interval=100, blit=True, repeat=False) # Slightly faster interval

# To save the animation (optional, requires ffmpeg or imagemagick)
# Ensure you have ffmpeg installed and in your system's PATH to save as mp4
# Update filename
ani.save('moving_average_filter_1d.gif', writer='imagemagick', fps=5)
# ani.save('moving_average_filter_1d.mp4', writer='ffmpeg', fps=15)

plt.show()
