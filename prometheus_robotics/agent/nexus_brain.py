from typing import Dict, List
from prometheus_robotics.core.gemini_client import GeminiClient
from prometheus_robotics.simulation.environment import GridWorld
from prometheus_robotics.agent.memory_module import MemoryModule
import logging

logger = logging.getLogger(__name__)

class NexusBrain:
    def __init__(self, env: GridWorld):
        self.env = env
        self.gemini = GeminiClient()
        self.memory = MemoryModule() # Initialize Memory
        self.history: List[str] = []
        self.assignments: Dict[str, List[int]] = {}

    def step(self):
        """
        Executes one step of the simulation by querying Gemini for each robot.
        """
        raw_state = self.env.get_state()
        actions = {}
        
        # 0. Assign Tasks if needed
        # Simple logic: If we have robots but no assignments, or assignments are stale (optional)
        # For now, we'll try to assign if anyone is missing a goal.
        robots_without_tasks = [rid for rid in raw_state["robots"] if rid not in self.assignments]
        
        if robots_without_tasks and raw_state["goals"]:
            logger.info("Assigning tasks...")
            new_assignments = self.gemini.assign_tasks(raw_state["robots"], raw_state["goals"])
            # Merge
            self.assignments.update(new_assignments)
            self.history.append(f"Assignments: {new_assignments}")
        
        for robot_id, pos in raw_state["robots"].items():
            # 1. Get perception
            view = self.env.get_local_view(robot_id, radius=2)
            state_str = f"ID: {robot_id}, Pos: {pos}"
            
            # Determine Task
            target_pos = self.assignments.get(robot_id, "Explore")
            task_str = f"Move to Target {target_pos}" if target_pos != "Explore" else "Explore / Wait for orders"
            
            # 2. Ask Gemini (Plan)
            action = self.gemini.plan_robot_action(state_str, view, task=task_str)
            
            # 3. Clean action
            valid_actions = ["MOVE_UP", "MOVE_DOWN", "MOVE_LEFT", "MOVE_RIGHT", "WAIT"]
            clean_action = action if action in valid_actions else "WAIT"
            
            # 4. Execute
            if clean_action.startswith("MOVE_"):
                direction = clean_action.replace("MOVE_", "")
                result = self.env.move_robot(robot_id, direction)
                
                status_msg = f"{clean_action} -> {result['status']}"
                actions[robot_id] = status_msg
                self.history.append(f"{robot_id}: {status_msg}")
                
                 # Check if goal reached
                if result.get('at_goal'):
                    self.history.append(f"🏆 {robot_id} REACHED GOAL!")
                    # Clear assignment
                    if robot_id in self.assignments:
                        del self.assignments[robot_id]

                # Store interesting events in Memory
                if result['status'] == 'collision':
                    self.memory.store_memory(
                        text=f"Robot {robot_id} collided with {result['object']} at {result['position']}",
                        metadata={"robot_id": robot_id, "type": "collision", "pos": result['position']},
                        embedding=[0.0]*768 # Mock embedding for now
                    )
            else:
                actions[robot_id] = "WAIT"
        
        return actions
