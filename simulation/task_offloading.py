# simulation/task_offloading.py

class TaskOffloading:
    def __init__(self, config, energy_model, communication_model):
        self.config = config
        self.energy_model = energy_model
        self.communication_model = communication_model
        self.processed_data_volume = []
        self.task_energy_efficiency = {}  # **Initialize this attribute**

    def decide_offloading(self, tasks, uavs, time_slot):
        offloading_decisions = []
        for task in tasks:
            best_uav = None
            max_energy_efficiency = -float('inf')
            for uav in uavs:
                # Check if the UAV can cover the IoT device
                distance = self.communication_model.calculate_distance(task['position'], uav.position)
                if distance <= self.config['uav']['coverage_radius']:
                    # Calculate energy efficiency
                    energy_efficiency = self.calculate_energy_efficiency(task, uav)
                    if energy_efficiency > max_energy_efficiency:
                        max_energy_efficiency = energy_efficiency
                        best_uav = uav

            if best_uav:
                # Offload to best_uav
                decision = {
                    'device_id': task['device_id'],
                    'uav_id': best_uav.uav_id,
                    'task': task,
                    'offloaded': True,
                    'energy_efficiency': max_energy_efficiency  # Store energy efficiency
                }
                self.processed_data_volume.append(task['data_size'])
                self.task_energy_efficiency[task['device_id']] = max_energy_efficiency
            else:
                # Execute locally
                energy_efficiency = self.calculate_energy_efficiency(task, None)  # Energy efficiency when not offloaded
                decision = {
                    'device_id': task['device_id'],
                    'uav_id': None,
                    'task': task,
                    'offloaded': False,
                    'energy_efficiency': energy_efficiency
                }
                self.processed_data_volume.append(task['data_size'])
                self.task_energy_efficiency[task['device_id']] = energy_efficiency
            offloading_decisions.append(decision)
        return offloading_decisions

    def calculate_energy_efficiency(self, task, uav):
        # Implement the energy efficiency calculation as per Equation (11)
        # Energy efficiency = Utility / Total Energy Consumption
        utility = task['data_size']
        if uav:
            uav_energy = self.energy_model.calculate_uav_computation_energy(task)
            iot_energy = self.energy_model.calculate_iot_transmission_energy(task)
            total_energy = uav_energy + iot_energy
        else:
            # If not offloaded, only IoT computation energy is considered
            total_energy = self.energy_model.calculate_iot_computation_energy(task)
        energy_efficiency = utility / total_energy if total_energy > 0 else 0
        return energy_efficiency
