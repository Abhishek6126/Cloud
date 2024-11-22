# simulation/communication_model.py

import math
from utils.constants import NOISE_POWER, BANDWIDTH, PATH_LOSS_EXPONENT

class CommunicationModel:
    def __init__(self, config):
        self.bandwidth = BANDWIDTH
        self.noise_power = NOISE_POWER

    def calculate_data_rate(self, iot_device, uav):
        distance = self.calculate_distance(iot_device.position, uav.position)
        path_loss = self.calculate_path_loss(distance)
        snr = iot_device.transmission_power / (path_loss * self.noise_power)
        data_rate = self.bandwidth * math.log2(1 + snr)
        return data_rate  # in bits per second

    def calculate_distance(self, pos1, pos2):
        x1, y1, z1 = pos1
        x2, y2, z2 = pos2
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)

    def calculate_path_loss(self, distance):
        # Free-space path loss model
        path_loss = (distance ** PATH_LOSS_EXPONENT)
        return path_loss
