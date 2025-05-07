# Random Sample Consensus ([`RANSAC.py`](RANSAC.py))

## Overview

RANSAC is a robust algorithm for estimating model parameters from data that contains outliers. It's particularly useful when dealing with sensor data that may have inconsistent or erroneous readings.

## How RANSAC Works

RANSAC works by repeatedly:

1. Randomly selecting a minimal subset of data points
2. Fitting a model to this subset
3. Finding all data points that fit this model within a threshold (inliers)
4. If the number of inliers is large enough, refining the model using all inliers
5. Repeating multiple times and keeping the model with the most inliers

This approach allows RANSAC to find a good model even when a significant portion of the data consists of outliers.

## Example Implementation (Ultrasonic Sensor)

The `RANSAC.py` script demonstrates RANSAC for robust distance estimation using simulated ultrasonic sensor data. This is a common problem in robotics and automation where sensors may have multi-path reflections.

### The Problem

Ultrasonic sensors measure distance by sending sound pulses and timing how long they take to return. However, these sensors often suffer from "multi-path" issues where:

- Primary reflection: Sound travels directly to the object and back
- Echo reflection: Sound bounces off multiple surfaces before returning

This creates a bimodal distribution in readings, with the primary reflection representing the true distance and the echo producing false, typically larger readings.

### Data Generation

The `generate_ultrasonic_data()` function simulates this scenario by creating:

- Primary reflections around the true distance (with some noise)
- Echo reflections at a greater distance (with typically more noise)
- A mixture of these two distributions

### RANSAC Implementation

The `ransac_mean()` function demonstrates how RANSAC can be used to find the true distance:

1. It randomly samples small subsets of readings
2. Calculates the mean of each subset
3. Counts how many total readings are within a threshold of this mean (inliers)
4. Keeps the model with the most inliers
5. Recalculates the final mean using all inliers

### Results

When running the script, you can observe:

- A simple mean is biased toward higher values due to echo readings
- The RANSAC mean closely matches the true distance
- Visualizations show how RANSAC identifies the primary reflection distribution

## Common Applications

RANSAC is widely used in:

- Computer vision for shape detection and image matching
- Sensor fusion systems to reject outlier readings
- Mapping and localization in robotics
- Line and curve fitting in scientific data analysis
- Feature matching between images
