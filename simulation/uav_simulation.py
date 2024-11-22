# simulation/uav_simulation.py

from simulation.path_planning import PathPlanning
import random

class UAV:
    def __init__(self, uav_id, initial_position):
        self.uav_id = uav_id
        self.position = initial_position
        self.position_history = [initial_position]  # Record initial position

class UAVSimulation:
    def __init__(self, config, path_planning):
        self.uav_count = config['uav']['count']
        self.uavs = [
            UAV(
                uav_id=i,
                initial_position=(
                    random.uniform(0, config['simulation']['area_size']),
                    random.uniform(0, config['simulation']['area_size']),
                    config['uav']['flying_height']
                )
            )
            for i in range(self.uav_count)
        ]
        self.path_planning = path_planning

    def update_positions(self, time_slot, iot_positions, iot_energy_efficiency):
        for uav in self.uavs:
            # Update UAV positions based on the path planning algorithm
            new_position = self.path_planning.calculate_next_position(uav, time_slot, iot_positions, iot_energy_efficiency)
            uav.position = new_position
            uav.position_history.append(new_position)  # Record the new position
