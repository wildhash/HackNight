#!/bin/bash
# Quick start script for AI Knowledge Sprint demo

echo "🚀 AI Knowledge Sprint - Quick Start"
echo "======================================"
echo ""

# Check if Docker is available
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    echo "✓ Docker and Docker Compose found"
    echo ""
    echo "Starting services with Docker Compose..."
    echo "This will start both Weaviate and the API server."
    echo ""
    
    # Create .env if it doesn't exist
    if [ ! -f .env ]; then
        echo "Creating .env file from .env.example..."
        cp .env.example .env
    fi
    
    docker-compose up --build
else
    echo "⚠ Docker not found. Starting API server only (without Weaviate)."
    echo ""
    echo "Note: Some features will use mock mode without Weaviate."
    echo ""
    
    # Check if Python is available
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3 not found. Please install Python 3.11+"
        exit 1
    fi
    
    # Check if dependencies are installed
    if ! python3 -c "import fastapi" &> /dev/null; then
        echo "Installing dependencies..."
        pip install -r requirements.txt
    fi
    
    # Create .env if it doesn't exist
    if [ ! -f .env ]; then
        echo "Creating .env file from .env.example..."
        cp .env.example .env
    fi
    
    echo "Starting API server..."
    echo ""
    echo "API will be available at: http://localhost:8000"
    echo "Open demo.html in your browser to test the API"
    echo ""
    
    python3 main.py
fi
