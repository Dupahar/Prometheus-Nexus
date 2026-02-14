import sys
import os

# Add root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from prometheus_robotics.simulation.environment import GridWorld
from prometheus_robotics.agent.nexus_brain import NexusBrain
import logging

logging.basicConfig(level=logging.INFO)

import json

# Mock Gemini Client for Testing Logic without API
class MockGeminiClient:
    def __init__(self, api_key=None):
        pass
    
    def assign_tasks(self, robots: dict, goals: list) -> dict:
        print(f"[MOCK] Assigning tasks for {len(robots)} robots and {len(goals)} goals.")
        # Simple Mock Logic: Assign R1 to first goal, R2 to second
        assignments = {}
        goal_list = list(goals)  # list of tuples
        
        # Hardcoded for the test scenario
        if "R1" in robots: assignments["R1"] = goal_list[1] # swap for fun
        if "R2" in robots: assignments["R2"] = goal_list[0]
        
        return assignments

    def plan_robot_action(self, robot_state: str, grid_view: list, task: str = "") -> str:
        # Simple Mock Logic: Move Right or Down
        # In a real test we'd parse the view, but here we just want to see the loop work.
        return "MOVE_RIGHT"

class MockMemoryModule:
    def __init__(self, collection_name="test"):
        pass
    def store_memory(self, text, metadata, embedding):
        pass
    def search_memory(self, query_embedding, limit=5):
        return []

def test_simulation():
    # Patch MemoryModule to avoid Qdrant connection issues
    import prometheus_robotics.agent.nexus_brain as nexus_brain_module
    nexus_brain_module.MemoryModule = MockMemoryModule
    
    print("Initializing GridWorld...")
    env = GridWorld(width=10, height=10)
    env.load_scenario("warehouse")
    
    # Add 2 Robots and 2 Goals
    env.add_robot("R1", 0, 0)
    env.add_robot("R2", 0, 1) # Start near each other
    
    env.add_goal(9, 9) # Goal 1
    env.add_goal(9, 8) # Goal 2
    
    print("Initializing NexusBrain with Mock Client...")
    brain = NexusBrain(env)
    # Inject Mock Gemini
    brain.gemini = MockGeminiClient()
    
    print("Running 3 steps...")
    for i in range(3):
        print(f"\n--- Step {i+1} ---")
        actions = brain.step()
        print(f"Actions: {actions}")
        # Print assignments if they exist
        if brain.assignments:
            print(f"Current Assignments: {brain.assignments}")
        
    print("\nTest Complete.")

if __name__ == "__main__":
    test_simulation()
