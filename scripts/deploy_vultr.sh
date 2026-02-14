#!/bin/bash

# ONE-CLICK DEPLOYMENT SCRIPT FOR PROMETHEUS-NEXUS (Vultr/Ubuntu)
# Usage: ./deploy_vultr.sh

echo "🚀 Starting Prometheus-Nexus Deployment..."

# 1. System Update
echo "📦 Updating System..."
sudo apt-get update && sudo apt-get upgrade -y

# 2. Install Git & Docker
echo "🐳 Installing Docker & Git..."
sudo apt-get install -y git curl apt-transport-https ca-certificates software-properties-common
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo groupadd docker
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 3. Clone Repository (if not already present)
if [ -d "Prometheus-Nexus" ]; then
    echo "🔄 Repository exists. Pulling latest..."
    cd Prometheus-Nexus
    git pull
else
    echo "📥 Cloning Repository..."
    git clone https://github.com/Dupahar/Prometheus-Nexus.git
    cd Prometheus-Nexus
fi

# 4. Environment Setup
if [ ! -f ".env" ]; then
    echo "⚠️ .env file missing! Creating template..."
    cat > .env <<EOF
GEMINI_API_KEY=YOUR_API_KEY_HERE
QDRANT_URL=YOUR_QDRANT_URL_HERE
QDRANT_API_KEY=YOUR_QDRANT_KEY_HERE
EOF
    echo "📝 PLEASE EDIT .env FILE WITH YOUR API KEYS!"
    echo "   Command: nano .env"
    exit 1
fi

# 5. Launch
echo "🚀 Launching Hive Mind..."
sudo docker-compose up -d --build

echo "✅ DEPLOYMENT COMPLETE!"
echo "➡️  Access Dashboard at: http://$(curl -s ifconfig.me):8501"
