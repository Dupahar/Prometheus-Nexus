import numpy as np
from typing import List, Tuple, Dict, Any

class GridWorld:
    def __init__(self, width: int = 20, height: int = 20):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=int)  # 0: Empty, 1: Obstacle, 2: Goal, 3: Robot
        self.robots: Dict[str, Tuple[int, int]] = {}
        self.goals: List[Tuple[int, int]] = []
        self.obstacles: List[Tuple[int, int]] = []

    def load_scenario(self, layout_type: str = "warehouse"):
        """Initializes the grid with a predefined layout."""
        self.grid.fill(0)
        self.obstacles = []
        self.goals = []
        
        if layout_type == "warehouse":
            # Create aisles
            for y in range(2, self.height - 2, 4):
                for x in range(2, self.width - 2):
                    self.add_obstacle(x, y)
        elif layout_type == "random":
            num_obstacles = (self.width * self.height) // 5
            for _ in range(num_obstacles):
                x = np.random.randint(0, self.width)
                y = np.random.randint(0, self.height)
                self.add_obstacle(x, y)
        
        # Ensure boundaries are open or closed as needed (simple box here)
        # (Optional: Add boundary walls)

    def add_obstacle(self, x: int, y: int):
        if 0 <= x < self.width and 0 <= y < self.height:
            if self.grid[y, x] == 0:
                self.grid[y, x] = 1
                self.obstacles.append((x, y))

    def add_robot(self, robot_id: str, x: int, y: int):
        if 0 <= x < self.width and 0 <= y < self.height:
            if self.grid[y, x] == 0:
                self.grid[y, x] = 3
                self.robots[robot_id] = (x, y)
                return True
        return False

    def add_goal(self, x: int, y: int):
        if 0 <= x < self.width and 0 <= y < self.height:
            if self.grid[y, x] != 1:
               self.grid[y, x] = 2
               self.goals.append((x, y))

    def move_robot(self, robot_id: str, direction: str) -> Dict[str, Any]:
        """
        Moves a robot in a given direction (UP, DOWN, LEFT, RIGHT).
        Returns status: success, collision, or out_of_bounds.
        """
        if robot_id not in self.robots:
            return {"status": "error", "message": "Robot not found"}

        cx, cy = self.robots[robot_id]
        nx, ny = cx, cy

        if direction == "UP":
            ny -= 1
        elif direction == "DOWN":
            ny += 1
        elif direction == "LEFT":
            nx -= 1
        elif direction == "RIGHT":
            nx += 1

        # Check bounds
        if not (0 <= nx < self.width and 0 <= ny < self.height):
            return {"status": "out_of_bounds", "position": (cx, cy)}

        # Check collisions (Obstacle=1, Other Robot=3)
        cell_val = self.grid[ny, nx]
        if cell_val == 1:
            return {"status": "collision", "object": "obstacle", "position": (cx, cy)}
        elif cell_val == 3:
            return {"status": "collision", "object": "robot", "position": (cx, cy)}
        
        # Move
        self.grid[cy, cx] = 0  # Clear old pos
        self.grid[ny, nx] = 3  # Set new pos
        self.robots[robot_id] = (nx, ny)
        
        # Check Goal
        at_goal = False
        if (nx, ny) in self.goals:
             at_goal = True
             # Keep goal visible? Or consume it? For now, robot sits on it.
             # If we want to visualize goal under robot, we need better state.
             # We'll assume goal remains. 

        return {"status": "success", "position": (nx, ny), "at_goal": at_goal}

    def get_state(self):
        """Returns the grid state for visualization."""
        return {
            "grid": self.grid.tolist(),
            "robots": self.robots,
            "goals": self.goals,
            "obstacles": self.obstacles,
            "dims": (self.width, self.height)
        }

    def get_local_view(self, robot_id: str, radius: int = 2) -> List[str]:
        """Returns a textual representation of the robot's surroundings for the LLM."""
        if robot_id not in self.robots:
            return []
        
        cx, cy = self.robots[robot_id]
        view = []
        
        for y in range(cy - radius, cy + radius + 1):
            row_str = ""
            for x in range(cx - radius, cx + radius + 1):
                if 0 <= x < self.width and 0 <= y < self.height:
                    val = self.grid[y, x]
                    if (x, y) == (cx, cy):
                        row_str += "R" # Robot (Self)
                    elif val == 1:
                        row_str += "#" # Obstacle
                    elif val == 2:
                        row_str += "G" # Goal
                    elif val == 3:
                        row_str += "O" # Other Robot
                    else:
                        row_str += "." # Empty
                else:
                    row_str += "X" # Out of bounds
            view.append(row_str)
            
        return view
