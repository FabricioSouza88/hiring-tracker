@echo off

rem Start DummyServer in a new command window
pushd dummy_api
start /b cmd /c ".venv\Scripts\activate && python -m uvicorn main:app --reload --port 5000"
popd

rem Start agentic in a new command window
pushd agentic
start /b cmd /c ".venv\Scripts\activate && python src/main.py"
popd

rem Keep the batch file running
echo Both processes started. Press Ctrl+C to exit.
pause > nul