#!/bin/bash

# DataSentinel Streamlit App Launcher
# This script starts the Streamlit web interface for DataSentinel

echo "🛡️  Starting DataSentinel Streamlit App..."
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run:"
    echo "   python -m venv .venv"
    echo "   source .venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. Make sure to configure your environment variables."
    echo ""
fi

# Activate virtual environment
source .venv/bin/activate

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit not found. Installing..."
    pip install streamlit==1.39.0
fi

# Run the Streamlit app
echo "🚀 Launching DataSentinel Web Interface..."
echo "📱 The app will open in your browser at http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run streamlit_app.py
