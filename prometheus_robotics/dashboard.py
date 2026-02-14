import streamlit as st
import pandas as pd
import numpy as np
import time
import sys
import os

# Add root to path so imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from prometheus_robotics.simulation.environment import GridWorld
from prometheus_robotics.agent.nexus_brain import NexusBrain

st.set_page_config(page_title="Prometheus-Nexus | Robotics Commander", layout="wide")

st.title("🤖 Prometheus-Nexus: Autonomous Fleet Commander")
st.markdown("### AI Meets Robotics Hackathon - Track 1: Autonomous Control")

# Initialize Session State
if "env" not in st.session_state:
    env = GridWorld(width=10, height=10)
    env.load_scenario("warehouse")  # or random
    env.add_robot("R1", 0, 0)
    env.add_goal(9, 9)
    st.session_state.env = env
    st.session_state.brain = NexusBrain(env)
    st.session_state.logs = []

env = st.session_state.env
brain = st.session_state.brain

# Sidebar Controls
st.sidebar.header("Mission Control")
if st.sidebar.button("Reset Simulation"):
    env.load_scenario("warehouse")
    env.add_robot("R1", 0, 0)
    env.add_goal(9, 9)
    st.session_state.logs = ["Simulation Reset."]

step_btn = st.sidebar.button("Step Simulation (AI Move)")

# Main Display
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Live Grid View")
    
    # Render Grid
    # We can use a heatmap or a custom HTML/Canvas component.
    # For now, a colorful dataframe or simple text grid.
    
    grid_data = env.grid.copy()
    
    # Map integers to emojis for better viz
    # 0: Empty, 1: Obstacle, 2: Goal, 3: Robot
    emoji_map = {0: "⬜", 1: "🧱", 2: "🏁", 3: "🤖"}
    
    # Create visual grid
    visual_grid = []
    for row in grid_data:
        visual_row = [emoji_map.get(cell, "?") for cell in row]
        visual_grid.append(visual_row)
        
    df = pd.DataFrame(visual_grid)
    st.table(df)

with col2:
    st.subheader("Nexus Brain Logs (Gemini 2.0)")
    log_container = st.container(height=400)
    
    if step_btn:
        with st.spinner("Nexus is thinking..."):
            decision = brain.step() # Returns dict of actions
            for r_id, action in decision.items():
                st.session_state.logs.insert(0, f"**{r_id}**: {action}")
    
    with log_container:
        for log in st.session_state.logs:
            st.markdown(log)

    st.subheader("Memory Implants (Qdrant)")
    if st.button("Query Spatial Memory"):
        # Mock query for now
        st.info("Querying Qdrant for 'hazardous locations'...")
        # In real impl: results = brain.memory.search_memory(...)
        st.write("Memory retrieval implementation pending visualization.")

# Metrics
st.markdown("---")
st.metric("Grid Size", f"{env.width}x{env.height}")
st.metric("Active Robots", len(env.robots))
