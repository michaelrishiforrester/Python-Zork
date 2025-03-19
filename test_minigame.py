#!/usr/bin/env python3
from minigames import CPUPipelineMinigame

class MockGame:
    def __init__(self):
        self.player = type('obj', (object,), {'knowledge': {'cpu': 5}})

# Create a test instance
mg = CPUPipelineMinigame(MockGame())

# Test the explanation
print(mg.explain())

# Test the status display
print("\n" + mg.get_status())

# Test stepping through the simulation
print("\n" + mg.step())