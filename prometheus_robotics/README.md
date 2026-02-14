# 🤖 Prometheus-Nexus
### AI-Powered Autonomous Fleet Commander
**Built for "AI Meets Robotics" Hackathon**

Prometheus-Nexus is an adaptation of the Prometheus-Siren security agent, pivoted to **Autonomous Robotics Control**. It uses **Gemini 2.0** for high-level reasoning and **Qdrant** for spatial memory.

## 🚀 Quick Start

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    pip install streamlit google-genai qdrant-client
    ```

2.  **Configure Environment**:
    Ensure `.env` has your API keys:
    ```env
    GEMINI_API_KEY=your_key
    QDRANT_URL=your_url
    QDRANT_API_KEY=your_key
    ```

3.  **Run Simulation**:
    ```bash
    streamlit run prometheus_robotics/dashboard.py
    ```

## 🧠 Architecture

| Component | Role | Technology |
| :--- | :--- | :--- |
| **Nexus Brain** | Fleet Commander | Gemini 2.0 Flash |
| **Spatial Memory** | Hazard/Path Storage | Qdrant Vector DB |
| **GridWorld** | Simulation Engine | Python (NumPy) |
| **Dashboard** | Mission Control | Streamlit |

## 📂 Structure

-   `prometheus_robotics/agent/`: Brain & Memory logic.
-   `prometheus_robotics/simulation/`: Grid world environment.
-   `prometheus_robotics/core/`: Clients for Gemini/Qdrant.
-   `prometheus_robotics/dashboard.py`: UI Entry point.
