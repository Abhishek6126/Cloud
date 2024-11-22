# simulation/path_planning.py

import math
import random

class PathPlanning:
    def __init__(self, config):
        self.config = config

    def calculate_next_position(self, uav, time_slot, iot_positions, iot_energy_efficiency):
        """
        Move the UAV towards the IoT device with the highest energy efficiency.
        """
        if not iot_positions:
            # No IoT devices have tasks; stay in place or move randomly
            target_position = self.get_random_position()
        else:
            # Find the IoT device with the highest energy efficiency
            target_position = self.find_best_iot(uav.position, iot_positions, iot_energy_efficiency)

        # Move towards the target position
        new_position = self.move_towards(uav.position, target_position)
        return new_position

    def find_best_iot(self, current_position, iot_positions, iot_energy_efficiency):
        max_efficiency = -float('inf')
        best_position = current_position
        best_device_id = None
        for pos, eff in zip(iot_positions, iot_energy_efficiency.values()):
            if eff > max_efficiency:
                max_efficiency = eff
                best_position = pos
        return best_position

    def get_random_position(self):
        x = random.uniform(0, self.config['simulation']['area_size'])
        y = random.uniform(0, self.config['simulation']['area_size'])
        z = self.config['uav']['flying_height']
        return (x, y, z)

    def move_towards(self, current_position, target_position):
        x1, y1, z1 = current_position
        x2, y2, z2 = target_position
        max_step = self.config['uav']['max_speed']
        # Calculate direction vector
        dx = x2 - x1
        dy = y2 - y1
        dz = z2 - z1
        distance = self.calculate_distance(current_position, target_position)
        if distance == 0:
            return current_position
        scale = min(max_step / distance, 1)
        new_x = x1 + dx * scale
        new_y = y1 + dy * scale
        new_z = z1 + dz * scale
        return (new_x, new_y, new_z)

    def calculate_distance(self, pos1, pos2):
        """
        Calculate Euclidean distance between two 3D points.
        """
        x1, y1, z1 = pos1
        x2, y2, z2 = pos2
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)
