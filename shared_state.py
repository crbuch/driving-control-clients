"""
Simple shared state using module-level variables.
Since we'll run a single FastAPI app on multiple ports, this will work perfectly.
"""

# Global state variables
steering_value = 0.0
gas_value = 0.0
brake_value = 0.0

def update_steering(value):
    global steering_value
    steering_value = max(-1.0, min(1.0, value))
    
def update_pedals(gas, brake):
    global gas_value, brake_value
    gas_value = max(0.0, min(1.0, gas))
    brake_value = max(0.0, min(1.0, brake))
    
def get_all():
    return {
        'steering_value': steering_value,
        'gas_value': gas_value,
        'brake_value': brake_value
    }
