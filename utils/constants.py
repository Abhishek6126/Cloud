# utils/constants.py

# Simulation area size
AREA_SIZE = 1000  # meters

# UAV parameters
UAV_MAX_SPEED = 50  # meters per second
UAV_ENERGY_PARAMS = {
    'kappa': 1e-5,
    'cpu_frequency': 5e9,  # 5 GHz
}

# IoT device parameters
IOT_ENERGY_PARAMS = {
    'kappa': 1e-5,
    'cpu_frequency': 1e9,  # 1 GHz
    'transmission_power': 0.5,  # Watts
    'data_rate': 1e6,  # 1 Mbps
}

# Communication parameters
NOISE_POWER = 1e-10  # Watts
BANDWIDTH = 1e6  # 1 MHz
PATH_LOSS_EXPONENT = 2
