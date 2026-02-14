# 🚀 Deployment Guide: Prometheus-Nexus

This guide will help you deploy the **Prometheus-Nexus** Command Center to a fresh Vultr (Ubuntu/Debian) server.

## ⚡ Option 1: The "One-Click" Script (Recommended)

We have included a script that automates Docker installation, repository cloning, and setup.

1.  **SSH into your Vultr Server**:
    ```bash
    ssh root@<YOUR_VULTR_IP>
    ```

2.  **Run the Deployment Script**:
    ```bash
    # Download the script
    curl -o deploy_vultr.sh https://raw.githubusercontent.com/Dupahar/Prometheus-Nexus/main/scripts/deploy_vultr.sh
    
    # Make it executable
    chmod +x deploy_vultr.sh
    
    # Run it
    ./deploy_vultr.sh
    ```

3.  **Configure API Keys**:
    The script will stop and ask you to edit the `.env` file.
    ```bash
    nano .env
    # Paste your GEMINI_API_KEY and QDRANT_URL
    # Press Ctrl+X, then Y, then Enter to save
    ```

4.  **Finish**:
    Run the script again or purely:
    ```bash
    cd Prometheus-Nexus
    docker-compose up -d --build
    ```

---

## 🛠️ Option 2: Manual Setup

If you prefer to do it step-by-step:

### 1. Install Docker
```bash
sudo apt-get update
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### 2. Clone the Repository
```bash
git clone https://github.com/Dupahar/Prometheus-Nexus.git
cd Prometheus-Nexus
```

### 3. Setup Environment
```bash
nano .env
```
Paste the following:
```ini
GEMINI_API_KEY=your_api_key_here
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_key_here
```

### 4. Launches
```bash
docker-compose up -d --build
```

---

## 🌐 Accessing the Command Center

Once deployed, access the dashboard at:
**`http://<YOUR_VULTR_IP>:8501`**
