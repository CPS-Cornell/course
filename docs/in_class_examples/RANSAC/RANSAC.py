import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def generate_ultrasonic_data(n_samples=1000, true_distance=100, echo_distance=150, 
                           primary_std=2, echo_std=4, echo_weight=0.3):
    """
    Generate simulated ultrasonic sensor data with bimodal distribution
    
    Parameters:
    - n_samples: Number of data points to generate
    - true_distance: Actual distance to the object (in cm)
    - echo_distance: Distance including the echo path (in cm)
    - primary_std: Standard deviation of the main reflection
    - echo_std: Standard deviation of the echo reflection
    - echo_weight: Weight of echo samples (0-1), represents proportion of echo readings
    
    Returns:
    - Array of simulated distance readings
    """
    # Generate primary reflection samples (dominant distribution)
    primary_samples = np.random.normal(true_distance, primary_std, 
                                     int(n_samples * (1 - echo_weight)))
    
    # Generate echo samples (weaker distribution)
    echo_samples = np.random.normal(echo_distance, echo_std, 
                                  int(n_samples * echo_weight))
    
    # Combine samples and shuffle
    all_samples = np.concatenate([primary_samples, echo_samples])
    np.random.shuffle(all_samples)
    
    return all_samples

def ransac_mean(data, num_iterations=100, sample_size=20, threshold=5.0):
    """
    RANSAC algorithm to find robust mean estimate
    
    Parameters:
    - data: Array of distance measurements
    - num_iterations: Number of RANSAC iterations
    - sample_size: Size of random subsample used in each iteration
    - threshold: Maximum deviation for a point to be considered an inlier
    
    Returns:
    - final_mean: Mean calculated from inliers of best model
    - best_inliers: Data points considered inliers for the best model
    """
    best_mean = None
    best_inlier_count = 0
    best_inliers = None
    
    for i in range(num_iterations):
        # Randomly select sample_size data points
        random_indices = np.random.choice(len(data), sample_size, replace=False)
        sample = data[random_indices]
        
        # Calculate mean of the sample
        sample_mean = np.mean(sample)
        
        # Find inliers (points within threshold of the mean)
        distances = np.abs(data - sample_mean)
        inliers = data[distances < threshold]
        inlier_count = len(inliers)
        
        # Update best model if this one has more inliers
        if inlier_count > best_inlier_count:
            best_inlier_count = inlier_count
            best_mean = sample_mean
            best_inliers = inliers
    
    # Recalculate mean using all inliers
    final_mean = np.mean(best_inliers)
    
    return final_mean, best_inliers

if __name__ == "__main__":
    # Parameters
    true_distance = 100  # cm
    echo_distance = 150  # cm
    n_samples = 1000
    
    # Generate data
    data = generate_ultrasonic_data(n_samples, true_distance, echo_distance)
    
    # Calculate simple mean (without RANSAC)
    simple_mean = np.mean(data)
    
    # Apply RANSAC
    ransac_distance, inliers = ransac_mean(data, num_iterations=100, sample_size=10, threshold=30)
    
    # Print results
    print(f"True distance: {true_distance} cm")
    print(f"Simple mean: {simple_mean:.2f} cm")
    print(f"RANSAC mean: {ransac_distance:.2f} cm")
    print(f"Number of inliers: {len(inliers)} out of {len(data)} samples")
    
    # Plot data distribution
    plt.figure(figsize=(12, 8))
    
    # Histogram of data
    plt.subplot(2, 1, 1)
    plt.hist(data, bins=30, alpha=0.7)
    plt.axvline(simple_mean, color='red', linestyle='--', label=f'Simple mean: {simple_mean:.2f}')
    plt.axvline(ransac_distance, color='green', linestyle='-', label=f'RANSAC mean: {ransac_distance:.2f}')
    plt.axvline(true_distance, color='black', linestyle='-', label=f'True distance: {true_distance}')
    plt.xlabel('Distance (cm)')
    plt.ylabel('Frequency')
    plt.title('Ultrasonic Distance Sensor Data')
    plt.legend()
    
    # Plot inliers vs outliers
    plt.subplot(2, 1, 2)
    plt.scatter(range(len(data)), data, c='lightgray', alpha=0.5, label='All data')
    plt.scatter(np.where(np.isin(data, inliers))[0], inliers, c='green', label='Inliers')
    plt.axhline(ransac_distance, color='green', linestyle='-', label=f'RANSAC mean: {ransac_distance:.2f}')
    plt.axhline(true_distance, color='black', linestyle='-', label=f'True distance: {true_distance}')
    plt.xlabel('Measurement index')
    plt.ylabel('Distance (cm)')
    plt.title('RANSAC Inliers')
    plt.legend()
    
    plt.tight_layout()
    plt.show()
    
    # Density plot showing bimodal distribution
    plt.figure(figsize=(10, 6))
    
    # Plot histogram with density
    plt.hist(data, bins=30, density=True, alpha=0.6, label='Data histogram')
    
    # Calculate x range for plotting distributions
    x = np.linspace(min(data), max(data), 1000)
    
    # Plot the two underlying distributions
    primary_dist = (1-0.3) * norm.pdf(x, true_distance, 2)
    echo_dist = 0.3 * norm.pdf(x, echo_distance, 4)
    combined_dist = primary_dist + echo_dist
    
    plt.plot(x, primary_dist, label='Primary reflection', color='blue')
    plt.plot(x, echo_dist, label='Echo', color='orange')
    plt.plot(x, combined_dist, label='Combined distribution', color='purple', linestyle='--')
    
    plt.axvline(simple_mean, color='red', linestyle='--', label=f'Simple mean: {simple_mean:.2f}')
    plt.axvline(ransac_distance, color='green', linestyle='-', label=f'RANSAC mean: {ransac_distance:.2f}')
    plt.axvline(true_distance, color='black', linestyle='-', label=f'True distance: {true_distance}')
    
    plt.xlabel('Distance (cm)')
    plt.ylabel('Density')
    plt.title('Bimodal Distribution of Ultrasonic Sensor Readings')
    plt.legend()
    plt.tight_layout()
    plt.show()
