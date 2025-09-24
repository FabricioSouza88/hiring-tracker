#!/bin/bash

# Start solver background process
cd dummy_api && source .venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8000 &

cd ../agentic && source .venv/bin/activate && python3 src/main.py &

# Keep the main script running so the container doesn't exit
wait