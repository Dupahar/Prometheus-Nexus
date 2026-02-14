
import streamlit as st
import pandas as pd
import time
import sys
import os
from datetime import datetime

# Enable importing local modules
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from prometheus_robotics.simulation.environment import GridWorld
from prometheus_robotics.agent.nexus_brain import NexusBrain

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="PROMETHEUS NEXUS",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS STYLING (The "Storytelling" UI) ---
st.markdown("""
<style>
    /* ORBITAL COMMAND THEME */
    .stApp { background-color: #050510; color: #00f0ff; font-family: 'Segoe UI', monospace; }
    
    /* Headers */
    h1, h2, h3 { color: #fff !important; text-shadow: 0 0 10px #00f0ff; letter-spacing: 2px; }
    
    /* Metrics */
    div[data-testid="stMetric"] {
        background-color: #0a0a1a;
        border: 1px solid #00f0ff;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.1);
        border-radius: 0px;
    }
    div[data-testid="stMetricLabel"] { color: #00f0ff; }
    div[data-testid="stMetricValue"] { color: #fff; font-size: 1.8rem !important; }

    /* The Grid */
    .grid-container {
        display: grid;
        gap: 2px;
        background-color: #111;
        padding: 10px;
        border: 2px solid #333;
        width: fit-content;
        margin: auto;
    }
    .grid-cell {
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        background-color: #0f0f1f;
        border: 1px solid #222;
        color: #444;
    }
    .cell-robot { background-color: #00f0ff; color: #000; box-shadow: 0 0 10px #00f0ff; animation: pulse 2s infinite; }
    .cell-goal { background-color: #00ff41; color: #000; box-shadow: 0 0 10px #00ff41; }
    .cell-obstacle { background-color: #ff4b4b; opacity: 0.5; }
    .cell-trail { background-color: #1a1a2e; }

    /* Neural Feed */
    .neural-log {
        font-family: 'Courier New', monospace;
        background: #000;
        border-left: 3px solid #00f0ff;
        padding: 10px;
        margin-bottom: 5px;
        font-size: 0.9em;
    }
    .log-timestamp { color: #666; font-size: 0.8em; margin-right: 10px; }
    .log-content { color: #eee; }
    
    @keyframes pulse {
        0% { opacity: 0.8; }
        50% { opacity: 1; box-shadow: 0 0 20px #00f0ff; }
        100% { opacity: 0.8; }
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'env' not in st.session_state:
    st.session_state.env = GridWorld(width=15, height=15)
    st.session_state.env.load_scenario("warehouse")
    # Default scenario
    st.session_state.env.add_robot("Unit-01", 1, 1)
    st.session_state.env.add_robot("Unit-02", 1, 13)
    st.session_state.env.add_goal(13, 13)
    st.session_state.env.add_goal(13, 1)

if 'brain' not in st.session_state:
    st.session_state.brain = NexusBrain(st.session_state.env)

if 'step_count' not in st.session_state:
    st.session_state.step_count = 0

# --- SIDEBAR: MISSION CONFIG ---
with st.sidebar:
    st.title("🛰️ MISSION CONFIG")
    st.markdown("---")
    
    # Reset Buttons
    if st.button("RESET SIMULATION", type="primary"):
        st.session_state.env = GridWorld(width=15, height=15)
        st.session_state.env.load_scenario("warehouse")
        st.session_state.env.add_robot("Unit-01", 1, 1)
        st.session_state.env.add_robot("Unit-02", 1, 13)
        st.session_state.env.add_goal(13, 13)
        st.session_state.env.add_goal(13, 1)
        st.session_state.brain = NexusBrain(st.session_state.env)
        st.session_state.step_count = 0
        st.rerun()

    st.markdown("### FLEET STATUS")
    state = st.session_state.env.get_state()
    for rid, pos in state['robots'].items():
        st.markdown(f"**{rid}**: `{pos}`")
        if rid in st.session_state.brain.assignments:
            st.caption(f"🎯 Target: {st.session_state.brain.assignments[rid]}")
        else:
            st.caption("💤 Idle")

# --- MAIN LAYOUT ---
col1, col2 = st.columns([2, 1])

with col1:
    st.title("PROMETHEUS NEXUS")
    st.subheader(f"ORBITAL SURVEILLANCE [T+{st.session_state.step_count}]")
    
    # RENDER GRID
    # We build an HTML grid
    grid_state = st.session_state.env.grid
    width = st.session_state.env.width
    height = st.session_state.env.height
    
    html = f'<div class="grid-container" style="grid-template-columns: repeat({width}, 30px);">'
    
    for y in range(height):
        for x in range(width):
            cell_class = "grid-cell"
            content = "·"
            
            # Check for objects
            # Priority: Robot > Goal > Obstacle
            is_robot = False
            for rid, pos in state['robots'].items():
                if pos == (x, y):
                    cell_class += " cell-robot"
                    content = "🤖"
                    is_robot = True
                    break
            
            if not is_robot:
                if (x, y) in state['goals']:
                    cell_class += " cell-goal"
                    content = "🚩"
                elif (x, y) in state['obstacles']:
                    cell_class += " cell-obstacle"
                    content = ""
            
            html += f'<div class="{cell_class}">{content}</div>'
    
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)
    
    # Controls
    st.markdown("###")
    c1, c2, c3 = st.columns(3)
    if c1.button("▶️ STEP SIMULATION", use_container_width=True):
        actions = st.session_state.brain.step()
        st.session_state.step_count += 1
        st.rerun()
        
    if c2.button("🎲 RANDOMIZE GOALS", use_container_width=True):
        import random
        st.session_state.env.goals = []
        st.session_state.env.add_goal(random.randint(0, width-1), random.randint(0, height-1))
        st.session_state.env.add_goal(random.randint(0, width-1), random.randint(0, height-1))
        st.session_state.brain.assignments = {} # Force re-assign
        st.rerun()

with col2:
    st.subheader("🧠 NEURAL FEED")
    
    # Display History from Brain
    history = st.session_state.brain.history
    
    # Container for logs
    log_container = st.container(height=500)
    with log_container:
        if not history:
            st.markdown("*Awaiting Neural Link...*")
        
        for entry in reversed(history[-15:]): # Show last 15
            timestamp = datetime.now().strftime("%H:%M:%S")
            st.markdown(f"""
            <div class="neural-log">
                <span class="log-timestamp">[{timestamp}]</span>
                <span class="log-content">{entry}</span>
            </div>
            """, unsafe_allow_html=True)

    # Metrics
    m1, m2 = st.columns(2)
    m1.metric("Active Drones", len(state['robots']))
    m2.metric("Pending Goals", len(state['goals']))
