# Hiring Tracker

An intelligent hiring automation system that uses AI agents to evaluate job candidates through multiple stages: triage, testing, and reporting.

## Project Scope

This project implements an AI-powered recruitment pipeline that automates candidate evaluation processes. The system consists of:

- **Dummy API**: A FastAPI-based mock recruitment API that simulates candidate applications and job postings
- **Agentic Module**: An intelligent agent system that processes candidates through multiple evaluation stages
- **Multi-Stage Evaluation**: Candidates go through triage, testing, and final reporting phases
- **AI-Powered Assessment**: Uses LLM agents to analyze candidate profiles, skills, and fit for roles
- **Extensible Architecture**: Built with abstract base classes for easy addition of new agent types

The system is designed to handle real-world recruitment scenarios while providing a testable, development-friendly environment.

## Architecture

```
┌─────────────────┐    ┌──────────────────┐
│   Dummy API     │◄──►│  Agentic Module  │
│   (FastAPI)     │    │   (AI Agents)    │
└─────────────────┘    └──────────────────┘
        │                       │
        ▼                       ▼
┌─────────────────┐    ┌──────────────────┐
│  Mock Database  │    │   LLM Client     │
│  (In-Memory)    │    │  (AI Services)   │
└─────────────────┘    └──────────────────┘
```

## Getting Started

### Prerequisites

- Python 3.11+
- Virtual environment (recommended)
- VS Code (for debug configurations)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/FabricioSouza88/hiring-tracker.git
cd hiring-tracker
```

2. Set up virtual environments for both modules:

**For Dummy API:**
```bash
cd dummy_api
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

pip install -r requirements.txt
```

**For Agentic Module:**
```bash
cd ../agentic
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

pip install -r requirements.txt
```

3. Create environment file:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Running the Application

### Option 1: Manual Terminal Commands

**Start the Dummy API:**
```bash
cd dummy_api
# Activate virtual environment first
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

The API will be available at: `http://localhost:5000`
- API Documentation: `http://localhost:5000/docs`
- Interactive API: `http://localhost:5000/redoc`

**Start the Agentic Module:**
```bash
cd agentic
# Activate virtual environment first
python src/main.py
```

### Option 2: VS Code Debug Configurations

The project includes pre-configured VS Code launch configurations:

1. **"Agents (Debug)"** - Run the agentic module in debug mode
   - Uses the debugger for step-by-step debugging
   - Automatically loads environment variables
   - Set breakpoints in agent code

2. **"API (uvicorn)"** - Run the dummy API in debug mode
   - Starts uvicorn with auto-reload
   - Debug FastAPI endpoints and models

3. **"Run Script (run.bat)"** - Start both services simultaneously (Windows)
   - Runs both API and agents in parallel
   - Good for integration testing

To use these configurations:
1. Open the project in VS Code
2. Go to Run and Debug (Ctrl+Shift+D)
3. Select your desired configuration
4. Press F5 to start

### Option 3: Batch Scripts

**Windows:**
```bash
.\run.bat
```

**Linux/Mac:**
```bash
./run.sh
```

## API Endpoints

The Dummy API provides the following endpoints:

- `GET /getNextTriage` - Get the next candidate for triage evaluation
- `POST /UpdateStatus` - Update task status
- `POST /UpdateTriageReport` - Submit triage evaluation results
- `GET /reports` - List all evaluation reports (debug endpoint)

## Configuration

Key configuration files:

- `.env` - Environment variables (API keys, URLs, etc.)
- `agentic/src/appconfig.py` - Application configuration
- `dummy_api/models.py` - Data models for API

## Development

### Adding New Agents

1. Create a new agent class inheriting from `AgentBase`
2. Implement the `evaluate()` method
3. Add agent to the orchestrator routing logic
4. Create corresponding prompt templates

### Project Structure

```
hiring-tracker/
├── dummy_api/          # Mock recruitment API
│   ├── main.py         # FastAPI application
│   ├── models.py       # Pydantic models
│   └── requirements.txt
├── agentic/            # AI agent system
│   ├── src/
│   │   ├── main.py     # Entry point
│   │   ├── agents/     # Agent implementations
│   │   ├── core/       # Core utilities
│   │   └── domain/     # Domain models
│   └── requirements.txt
├── .vscode/            # VS Code configurations
│   └── launch.json     # Debug configurations
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
