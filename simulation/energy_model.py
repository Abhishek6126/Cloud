# simulation/energy_model.py

from utils.constants import UAV_ENERGY_PARAMS, IOT_ENERGY_PARAMS

class EnergyModel:
    def __init__(self, config):
        self.uav_energy_consumption = {}
        self.iot_energy_consumption = {}
        self.config = config

    def update_energy_consumption(self, offloading_decisions, time_slot):
        # Calculate energy consumption based on offloading decisions
        for decision in offloading_decisions:
            device_id = decision['device_id']
            uav_id = decision['uav_id']
            task = decision['task']
            offloaded = decision['offloaded']

            if offloaded:
                # Energy consumed by UAV for computation
                uav_energy = self.calculate_uav_computation_energy(task)
                # Energy consumed by UAV for propulsion is calculated in path_planning
                # Update UAV energy consumption
                if uav_id not in self.uav_energy_consumption:
                    self.uav_energy_consumption[uav_id] = 0
                self.uav_energy_consumption[uav_id] += uav_energy

                # Energy consumed by IoT device for transmission
                iot_energy = self.calculate_iot_transmission_energy(task)
            else:
                # Energy consumed by IoT device for local computation
                iot_energy = self.calculate_iot_computation_energy(task)

            # Update IoT device energy consumption
            if device_id not in self.iot_energy_consumption:
                self.iot_energy_consumption[device_id] = 0
            self.iot_energy_consumption[device_id] += iot_energy

    def calculate_uav_computation_energy(self, task):
        # Implement Equation (8) from the paper
        # U_j^{comp} = \kappa_j (f_j^{(k)})^2 D_k C_k
        kappa = UAV_ENERGY_PARAMS['kappa']
        f = UAV_ENERGY_PARAMS['cpu_frequency']
        D_k = task['data_size']
        C_k = task['computation_intensity']
        energy = kappa * (f ** 2) * D_k * C_k
        return energy

    def calculate_iot_transmission_energy(self, task):
        # Implement energy consumption for transmission
        power = IOT_ENERGY_PARAMS['transmission_power']
        duration = task['data_size'] / IOT_ENERGY_PARAMS['data_rate']
        energy = power * duration
        return energy

    def calculate_iot_computation_energy(self, task):
        # Implement Equation (9) from the paper
        # U_i = e_i (f_i)^2 D_k C_k
        e_i = IOT_ENERGY_PARAMS['kappa']
        f_i = IOT_ENERGY_PARAMS['cpu_frequency']
        D_k = task['data_size']
        C_k = task['computation_intensity']
        energy = e_i * (f_i ** 2) * D_k * C_k
        return energy

    def get_total_energy_consumption(self):
        total_uav_energy = sum(self.uav_energy_consumption.values())
        total_iot_energy = sum(self.iot_energy_consumption.values())
        total_energy = total_uav_energy + total_iot_energy
        return total_energy
