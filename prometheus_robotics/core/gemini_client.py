import google.generativeai as genai
import os
import logging
from typing import Optional, List
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class GeminiClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not found in environment variables.")
        else:
            logger.info(f"Gemini API Key found: {self.api_key[:4]}...")
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
        
        self.model_name = "gemini-1.5-flash" 

    def generate_content(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        try:
            model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=system_instruction
            )
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini generation error: {e}")
            return f"Error: {e}"

    def assign_tasks(self, robots: dict, goals: list) -> dict:
        """
        Assigns available goals to robots based on proximity and efficiency.
        """
        system_prompt = """You are Nexus, a Fleet Commander.
        Your goal is to optimally assign distinct targets to robots.
        
        Input:
        - Robots: {ID: (x, y)}
        - Goals: [(x, y), (x, y)...]
        
        Rules:
        1. One goal per robot (if possible).
        2. Assign based on proximity (minimize total travel distance).
        3. Output strict JSON: {"robot_id": [target_x, target_y], ...}
        4. If more robots than goals, some robots can be idle ("IDLE").
        """
        
        user_prompt = f"""
        Robots: {robots}
        Goals: {goals}
        
        Assign goals now. Return ONLY the JSON.
        """
        
        response = self.generate_content(user_prompt, system_instruction=system_prompt)
        try:
            # Simple cleanup to ensure JSON parsing if the model adds markdown
            import json
            text = response.replace("```json", "").replace("```", "").strip()
            return json.loads(text)
        except Exception as e:
            logger.error(f"Failed to parse assignment: {e} | Response: {response}")
            return {}

    def plan_robot_action(self, robot_state: str, grid_view: List[str], task: str = "Explore") -> str:
        """
        Specialized method for robot planning.
        """
        system_prompt = f"""You are Nexus, an AI fleet commander for autonomous robots. 
        Your goal is to guide robots to their destinations safely and efficiently.
        
        Current Task: {task}
        
        You will receive:
        1. The Robot's internal state (Position, ID).
        2. A local grid view where:
           - 'R' is the robot.
           - '.' is empty space.
           - '#' is an obstacle.
           - 'G' is the goal.
           - 'O' is another robot.

        Output strictly ONE command from: [MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT, WAIT].
        Do not output reasoning, only the command.
        """
        
        user_prompt = f"""
        Robot State: {robot_state}
        
        Local Grid View:
        {chr(10).join(grid_view)}
        
        Next Action:
        """
        
        response = self.generate_content(user_prompt, system_instruction=system_prompt)
        return response.strip().upper()
