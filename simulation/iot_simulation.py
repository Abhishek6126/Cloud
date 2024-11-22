# simulation/iot_simulation.py

import random
from utils.constants import AREA_SIZE

class IoTDevice:
    def __init__(self, device_id):
        self.device_id = device_id
        self.position = (random.uniform(0, AREA_SIZE), random.uniform(0, AREA_SIZE), 0)
        self.energy_consumed = 0
        self.position_history = [self.position]  # Record initial position
        # Additional IoT device attributes

class IoTSimulation:
    def __init__(self, config):
        self.device_count = config['iot']['device_count']
        self.devices = [IoTDevice(device_id=i) for i in range(self.device_count)]

    def update_positions(self, time_slot):
        for device in self.devices:
            # Update positions based on mobility model (e.g., random walk)
            device.position = self.random_walk(device.position)
            device.position_history.append(device.position)  # Record the new position

    def random_walk(self, position):
        # Simple random walk implementation
        x, y, z = position
        x += random.uniform(-5, 5)
        y += random.uniform(-5, 5)
        x = max(0, min(x, AREA_SIZE))
        y = max(0, min(y, AREA_SIZE))
        return (x, y, z)

    def generate_tasks(self, time_slot):
        tasks = []
        for device in self.devices:
            # Generate tasks based on some probability
            if random.random() < 0.5:
                task = {
                    'device_id': device.device_id,
                    'position': device.position,
                    'data_size': random.uniform(0.5, 5.2),  # in Megabits
                    'computation_intensity': random.uniform(500, 1000),  # cycles per bit
                    'deadline': time_slot + random.randint(1, 5)
                }
                tasks.append(task)
        return tasks
