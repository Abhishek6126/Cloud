# main.py

from simulation.simulation_manager import SimulationManager
import json
import matplotlib.pyplot as plt

def main():
    # Load configuration settings
    with open('config.json', 'r') as config_file:
        base_config = json.load(config_file)

    # Lists to store results
    num_iot_devices_list = range(300, 1001, 100)  # From 300 to 1000 with 100 units gap
    energy_efficiency_list = []
    energy_consumption_list = []
    system_utility_list = []

    for num_devices in num_iot_devices_list:
        print(f"Running simulation with {num_devices} IoT devices...")

        # Update the number of IoT devices in the config
        config = base_config.copy()
        config['iot']['device_count'] = num_devices

        # Initialize the simulation manager with the updated configuration
        sim_manager = SimulationManager(config)

        # Run the simulation
        sim_manager.run_simulation()

        # Visualize UAV flight paths as an animation
        sim_manager.visualize_uav_flight_paths_animation(num_devices)

        # Collect metrics
        energy_efficiency = sim_manager.calculate_energy_efficiency()
        energy_consumption = sim_manager.calculate_total_energy_consumption()
        system_utility = sim_manager.calculate_system_utility()

        # Store metrics
        energy_efficiency_list.append(energy_efficiency)
        energy_consumption_list.append(energy_consumption)
        system_utility_list.append(system_utility)

    # Plot the results
    plot_results(num_iot_devices_list, energy_efficiency_list, energy_consumption_list, system_utility_list)

def plot_results(num_iot_devices_list, energy_efficiency_list, energy_consumption_list, system_utility_list):
    # Plot Energy Efficiency vs Number of IoT Devices
    plt.figure(figsize=(10, 6))
    plt.plot(num_iot_devices_list, energy_efficiency_list, marker='o', label='Energy Efficiency')
    plt.title('Energy Efficiency vs Number of IoT Devices')
    plt.xlabel('Number of IoT Devices')
    plt.ylabel('Energy Efficiency (Megabits/Joule)')
    plt.grid(True)
    plt.legend()
    plt.savefig('results/plots/energy_efficiency.png')
    plt.show()

    # Plot Energy Consumption vs Number of IoT Devices
    plt.figure(figsize=(10, 6))
    plt.plot(num_iot_devices_list, energy_consumption_list, marker='o', color='r', label='Energy Consumption')
    plt.title('Energy Consumption vs Number of IoT Devices')
    plt.xlabel('Number of IoT Devices')
    plt.ylabel('Total Energy Consumption (Joules)')
    plt.grid(True)
    plt.legend()
    plt.savefig('results/plots/energy_consumption.png')
    plt.show()

    # Plot System Utility vs Number of IoT Devices
    plt.figure(figsize=(10, 6))
    plt.plot(num_iot_devices_list, system_utility_list, marker='o', color='g', label='System Utility')
    plt.title('System Utility vs Number of IoT Devices')
    plt.xlabel('Number of IoT Devices')
    plt.ylabel('System Utility (Megabits Processed)')
    plt.grid(True)
    plt.legend()
    plt.savefig('results/plots/system_utility.png')
    plt.show()

if __name__ == "__main__":
    main()
