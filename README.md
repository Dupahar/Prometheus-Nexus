# Prometheus-Nexus: AI-Driven Swarm Robotics Command Center

**Prometheus-Nexus** is a next-generation **AI-driven fleet management system** designed for the **"AI Meets Robotics" Hackathon**. By pivoting the advanced "Prometheus-Siren" cybersecurity agent, we have created a centralized "Hive Mind" capable of orchestrating autonomous robot swarms in complex environments.

## 🚀 The Mission
In logistics, disaster relief, and hazardous exploration, controlling multiple robots individually is inefficient. **Prometheus-Nexus** solves this by allowing a single human operator to issue high-level strategic commands (e.g., *"Secure the warehouse perimeter"* or *"Locate survivors in Sector 7"*), which the system autonomously translates into specific, coordinated actions for a fleet of robots.

## 🧠 Core Technology

### 1. The Nexus Brain (Gemini 2.0 Flash)
At the heart of the system is the **Nexus Brain**, powered by **Google's Gemini 2.0 Flash**. Unlike traditional heuristic-based controllers, Nexus Brain possesses **spatial reasoning** and **semantic understanding**. It analyzes the grid-based environment, understands robot capabilities, and strictly enforces safety protocols (collision avoidance) while optimizing for mission success.

### 2. Spatial Memory (Qdrant)
Robots need to learn from their environment. We integrated **Qdrant** vector database to give Prometheus-Nexus a persistent **Spatial Memory**.
- **Collision Events**: When a robot encounters an unexpected obstacle, the event is embedded and stored.
- **Adaptive Pathing**: Future pathfinding queries retrieve these "danger zones," allowing the fleet to learn and adapt its behavior over time without manual code updates.

### 3. Simulation & Digital Twin
A lightweight **GridWorld Simulation** serves as the testing ground and Digital Twin. It simulates:
- **Heterogeneous Agents**: Multiple robots with unique IDs.
- **Dynamic Environments**: Obstacles, goals, and changing terrain.
- **Real-time Feedback**: Instant visual feedback via a Streamlit-based **Mission Control Dashboard**.

## 🛠️ Architecture
- **Agentic Core**: Python-based utilizing `google-genai` SDK.
- **Orchestration**: A centralized loop that perceives the global state, delegates tasks via Gemini, and executes moves.
- **Frontend**: A deployment-ready **Streamlit** dashboard featuring:
    -   **Orbital Command Theme**: Dark, sci-fi aesthetic for immersive control.
    -   **Live Grid Visualization**: Real-time position tracking of robots and objectives.
    -   **Neural Feed**: A transparent view into the AI's decision-making process.
- **Deployment**: Dockerized and ready for cloud deployment (Vultr) or edge computing.

## 🎯 Hackathon Fit
Prometheus-Nexus directly addresses **Track 1: Autonomous Control**. It demonstrates how Generative AI can move beyond text processing to become the decision-making engine for physical systems, bridging the gap between LLMs and robotics.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Dupahar/Prometheus-Nexus.git
   cd Prometheus-Nexus
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file with:
   ```ini
   GEMINI_API_KEY=your_gemini_key
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_qdrant_key
   ```

5. Run the dashboard:
   ```bash
   streamlit run dashboard.py
   ```
