#!/bin/bash
# Validation script to check if the demo environment is ready

echo "🔍 AI Knowledge Sprint - Setup Checker"
echo "======================================"
echo ""

ERRORS=0
WARNINGS=0

# Check Python
echo "Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ $PYTHON_VERSION found"
else
    echo "✗ Python 3 not found"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# Check Docker
echo "Checking Docker..."
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    echo "✓ $DOCKER_VERSION found"
    
    # Check if Docker daemon is running
    if docker info &> /dev/null; then
        echo "✓ Docker daemon is running"
    else
        echo "⚠ Docker is installed but daemon is not running"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo "⚠ Docker not found (optional but recommended)"
    WARNINGS=$((WARNINGS + 1))
fi
echo ""

# Check Docker Compose
echo "Checking Docker Compose..."
if docker compose version &> /dev/null || command -v docker-compose &> /dev/null; then
    if docker compose version &> /dev/null; then
        COMPOSE_VERSION=$(docker compose version)
    else
        COMPOSE_VERSION=$(docker-compose --version)
    fi
    echo "✓ $COMPOSE_VERSION found"
else
    echo "⚠ Docker Compose not found (optional but recommended)"
    WARNINGS=$((WARNINGS + 1))
fi
echo ""

# Check Python dependencies
echo "Checking Python dependencies..."
if [ -f "requirements.txt" ]; then
    echo "✓ requirements.txt found"
    
    # Check if key dependencies are installed
    MISSING_DEPS=0
    for package in fastapi uvicorn sentence-transformers weaviate-client; do
        if python3 -c "import ${package//-/_}" &> /dev/null; then
            echo "  ✓ $package installed"
        else
            echo "  ✗ $package not installed"
            MISSING_DEPS=$((MISSING_DEPS + 1))
        fi
    done
    
    if [ $MISSING_DEPS -gt 0 ]; then
        echo ""
        echo "⚠ Some dependencies are missing. Run:"
        echo "  pip install -r requirements.txt"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo "✗ requirements.txt not found"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# Check required files
echo "Checking required files..."
FILES_OK=true
for file in main.py demo.html docker-compose.yml Dockerfile; do
    if [ -f "$file" ]; then
        echo "✓ $file exists"
    else
        echo "✗ $file missing"
        FILES_OK=false
        ERRORS=$((ERRORS + 1))
    fi
done
echo ""

# Check if .env exists
echo "Checking configuration..."
if [ -f ".env" ]; then
    echo "✓ .env file exists"
else
    if [ -f ".env.example" ]; then
        echo "⚠ .env file not found (will use defaults)"
        echo "  You can create it with: cp .env.example .env"
        WARNINGS=$((WARNINGS + 1))
    else
        echo "⚠ No .env or .env.example found"
        WARNINGS=$((WARNINGS + 1))
    fi
fi
echo ""

# Summary
echo "======================================"
echo "Summary:"
echo "======================================"

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo "✓ Everything looks good! You're ready to go!"
    echo ""
    echo "Start the demo with:"
    echo "  docker-compose up --build"
    echo ""
    echo "Or run:"
    echo "  ./start-demo.sh"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo "⚠ Setup is functional but has $WARNINGS warning(s)"
    echo ""
    echo "You can still run the demo with:"
    echo "  docker-compose up --build"
    echo ""
    echo "Or fix warnings and get the full experience!"
    exit 0
else
    echo "✗ Found $ERRORS error(s) and $WARNINGS warning(s)"
    echo ""
    echo "Please fix the errors above before running the demo."
    exit 1
fi
