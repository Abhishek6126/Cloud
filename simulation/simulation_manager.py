# simulation/simulation_manager.py

from simulation.uav_simulation import UAVSimulation
from simulation.iot_simulation import IoTSimulation
from simulation.energy_model import EnergyModel
from simulation.communication_model import CommunicationModel
from simulation.task_offloading import TaskOffloading
from simulation.path_planning import PathPlanning
from utils.helpers import Logger
import matplotlib.pyplot as plt
import os
import matplotlib.animation as animation
import numpy as np

class SimulationManager:
    def __init__(self, config):
        self.config = config
        self.logger = Logger(config['log_file'])
        self.energy_model = EnergyModel(config)
        self.communication_model = CommunicationModel(config)
        self.path_planning = PathPlanning(config)
        self.task_offloading = TaskOffloading(config, self.energy_model, self.communication_model)
        self.uav_simulation = UAVSimulation(config, self.path_planning)
        self.iot_simulation = IoTSimulation(config)
        self.time_slots = config['simulation']['time_slots']

        # Initialize lists to store positions and energy efficiency
        self.uav_positions_over_time = []  # List of lists of UAV positions at each time slot
        self.iot_positions_over_time = []  # List of lists of IoT device positions at each time slot
        self.iot_energy_efficiency_over_time = []  # List of dicts per time slot

    def run_simulation(self):
        self.logger.log("Starting simulation.")
        for t in range(self.time_slots):
            self.logger.log(f"Time slot {t+1}/{self.time_slots}")

            # Update IoT devices and UAVs positions
            self.iot_simulation.update_positions(t)
            current_iot_positions = [device.position for device in self.iot_simulation.devices]
            current_iot_ids = [device.device_id for device in self.iot_simulation.devices]
            current_iot_energy_efficiency = self.task_offloading.task_energy_efficiency.copy()

            self.uav_simulation.update_positions(t, current_iot_positions, current_iot_energy_efficiency)

            # Record positions
            self.uav_positions_over_time.append([uav.position for uav in self.uav_simulation.uavs])
            self.iot_positions_over_time.append(current_iot_positions)

            # Generate tasks for IoT devices
            tasks = self.iot_simulation.generate_tasks(t)

            # Perform task offloading decisions
            offloading_decisions = self.task_offloading.decide_offloading(tasks, self.uav_simulation.uavs, t)

            # Record energy efficiency
            self.iot_energy_efficiency_over_time.append(self.task_offloading.task_energy_efficiency.copy())

            # Execute tasks and update energy consumption
            self.energy_model.update_energy_consumption(offloading_decisions, t)

            # Log the number of recorded positions and energy efficiencies
            self.logger.log(f"Recorded {len(self.uav_positions_over_time[-1])} UAV positions and {len(self.iot_positions_over_time[-1])} IoT positions.")
            self.logger.log(f"Recorded energy efficiencies for {len(self.iot_energy_efficiency_over_time[-1])} IoT devices.")

        self.logger.log("Simulation completed.")

    def calculate_energy_efficiency(self):
        # Energy Efficiency = System Utility / Total Energy Consumption
        total_energy = self.energy_model.get_total_energy_consumption()
        system_utility = self.calculate_system_utility()
        energy_efficiency = system_utility / total_energy if total_energy > 0 else 0
        return energy_efficiency

    def calculate_total_energy_consumption(self):
        total_energy = self.energy_model.get_total_energy_consumption()
        return total_energy

    def calculate_system_utility(self):
        # System Utility is the total processed data volume
        system_utility = sum(self.task_offloading.processed_data_volume)
        return system_utility

    def visualize_uav_flight_paths_animation(self, num_devices):
        """
        Creates an animation of UAV flight paths and IoT device locations based on energy efficiency.
        """
        # Create a subdirectory for the current simulation run
        animation_dir = f'results/plots/{num_devices}_iot_devices/animations'
        os.makedirs(animation_dir, exist_ok=True)

        fig, ax = plt.subplots(figsize=(10, 10))
        ax.set_xlim(0, self.config['simulation']['area_size'])
        ax.set_ylim(0, self.config['simulation']['area_size'])
        ax.set_xlabel('X Position (meters)')
        ax.set_ylabel('Y Position (meters)')
        ax.set_title('UAV Flight Paths and IoT Device Locations')

        # Initialize scatter plots with empty 2D arrays
        iot_scatter = ax.scatter([], [], c='blue', s=10, alpha=0.5, label='IoT Devices')
        uav_scatter = ax.scatter([], [], c='red', marker='^', s=100, label='UAVs')
        
        # Assign unique colors to each UAV
        colors = plt.cm.get_cmap('hsv', self.uav_simulation.uav_count)
        lines = []
        for idx, uav in enumerate(self.uav_simulation.uavs):
            line, = ax.plot([], [], linestyle='--', color=colors(idx), label=f'UAV {uav.uav_id} Path')
            lines.append(line)

        ax.legend(loc='upper right')
        ax.grid(True)

        def init():
            iot_scatter.set_offsets(np.empty((0, 2)))
            uav_scatter.set_offsets(np.empty((0, 2)))
            for line in lines:
                line.set_data([], [])
            return [iot_scatter, uav_scatter] + lines

        def animate(t):
            # Update IoT device positions and energy efficiency
            iot_positions = self.iot_positions_over_time[t]
            energy_efficiency = self.iot_energy_efficiency_over_time[t]
            if iot_positions:
                # Pair each IoT position with its energy efficiency
                iot_data = list(zip(iot_positions, energy_efficiency.values()))
                # Sort IoT devices by energy efficiency in descending order
                sorted_iot = sorted(iot_data, key=lambda x: x[1], reverse=True)
                # Select top N IoT devices to highlight
                top_n = 10  # Number of top IoT devices to highlight
                top_iot = sorted_iot[:top_n]
                other_iot = sorted_iot[top_n:]

                # Extract coordinates
                x_top_iot = [pos[0][0] for pos in top_iot]
                y_top_iot = [pos[0][1] for pos in top_iot]
                x_other_iot = [pos[0][0] for pos in other_iot]
                y_other_iot = [pos[0][1] for pos in other_iot]

                # Update scatter plots
                iot_scatter.set_offsets(np.column_stack((x_other_iot, y_other_iot)))
                # Remove existing top IoT scatter and add new ones
                if hasattr(self, 'top_iot_scatter'):
                    self.top_iot_scatter.remove()
                top_iot_scatter = ax.scatter(x_top_iot, y_top_iot, c='green', s=20, marker='*', label='Top Energy Efficient IoT Devices')
                self.top_iot_scatter = top_iot_scatter
            else:
                iot_scatter.set_offsets(np.empty((0, 2)))
                if hasattr(self, 'top_iot_scatter'):
                    self.top_iot_scatter.remove()

            # Update UAV positions
            uav_positions = self.uav_positions_over_time[t]
            if uav_positions:
                x_uav = [pos[0] for pos in uav_positions]
                y_uav = [pos[1] for pos in uav_positions]
                positions = np.column_stack((x_uav, y_uav))
                uav_scatter.set_offsets(positions)
            else:
                uav_scatter.set_offsets(np.empty((0, 2)))

            # Update UAV flight paths
            for idx, uav in enumerate(self.uav_simulation.uavs):
                positions = uav.position_history[:t+1]
                if positions:
                    x_path = [pos[0] for pos in positions]
                    y_path = [pos[1] for pos in positions]
                    lines[idx].set_data(x_path, y_path)
                else:
                    lines[idx].set_data([], [])

            # Update the title
            ax.set_title(f'UAV Flight Paths and IoT Device Locations at Time Slot {t+1}')
            return [iot_scatter, uav_scatter] + lines

        ani = animation.FuncAnimation(fig, animate, init_func=init,
                                      frames=self.time_slots, interval=500, blit=True)

        # Save the animation as GIF
        ani.save(f'{animation_dir}/uav_flight_paths_animation.gif', writer='pillow')
        # Alternatively, to save as MP4 (requires ffmpeg):
        # ani.save(f'{animation_dir}/uav_flight_paths_animation.mp4', writer='ffmpeg')

        plt.close()
