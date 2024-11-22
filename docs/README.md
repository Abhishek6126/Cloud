# Energy-Efficient Computation Offloading in Multi-UAV Edge Computing 🚁

Welcome to the repository for **Energy-Efficient Computation Offloading in Edge Computing for Multi-UAV Networks**, a cutting-edge simulation of how UAVs (Unmanned Aerial Vehicles) can enhance IoT networks through efficient computational offloading and adaptive path planning. 🌐

---

## 📜 Project Overview

This project focuses on integrating **IoT networks**, **edge computing**, and **UAVs** to optimize **computational performance** and **energy efficiency** in resource-constrained environments. It features:

- **Energy-efficient task offloading**: Balancing energy usage between IoT devices and UAVs.
- **Dynamic path planning**: UAVs adapt to changing IoT locations for optimal coverage.
- **Scalable and real-time solutions**: Designed for large-scale IoT networks in dynamic conditions.

---

## 🛠 Features

- **Custom Algorithm:** Implements the **ECOP (Energy-Efficient Computation Offloading and Path Planning)** algorithm.
- **Real-Time Simulation:** Models dynamic IoT and UAV movement within a simulated environment.
- **Comprehensive Visualizations:** Includes graphs and visual outputs for energy efficiency, task processing, and UAV trajectories.
- **Energy Calculations:** Tracks energy usage for offloading, computation, and UAV flight.

---
## 📊 Outputs

The simulation provides insightful metrics and visualizations, including:

### 1. **Energy Efficiency Graph**
   - **Description**: A line plot that shows how energy efficiency evolves during the simulation, reflecting the optimization achieved by the ECOP algorithm.
   - **Purpose**: Demonstrates the overall system performance improvement over time.

### 2. **Task Processing Distribution**
   - **Description**: A scatter plot of tasks categorized as **locally processed** vs. **offloaded** to UAVs, with corresponding energy efficiencies.
   - **Purpose**: Highlights the effectiveness of the task offloading strategy in achieving energy savings.

### 3. **UAV Trajectories**
   - **Description**: A 2D visualization of UAV paths over the simulation area, including IoT device positions. Coverage zones of UAVs are also displayed.
   - **Purpose**: Shows the adaptability of UAV movements to maintain optimal coverage.

### 4. **Summary Metrics**
   - **Description**: The script outputs total energy consumed, the number of offloaded vs. locally executed tasks, and the system's average energy efficiency after each simulation run.
   - **Purpose**: Provides numerical insights into the system's performance.

## 🚀 Getting Started

### Prerequisites

1. **Python 3.7+**
2. Install **LeafSim** using:
   ```bash
   pip install leafsim
### Steps to Run the Simulation

1. Clone the repository:
   ```bash
   git clone https://github.com/Abhishek6126/Cloud.git
   cd Cloud
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Run the main script:
   ```bash
   python main.py

👥 Contributors
Kalp Patel (242CS028)
Abhishek Pandey (242CS004)
