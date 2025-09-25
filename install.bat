@echo off
echo Setting up Multi-Agent Decision System...

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo Copying environment template...
if not exist .env (
    copy .env.example .env
    echo Please edit .env file with your API keys before running the application.
) else (
    echo .env file already exists, skipping copy.
)

echo Setup complete!
echo.
echo Next steps:
echo 1. Edit .env file with your API keys
echo 2. Run: venv\Scripts\activate.bat
echo 3. Run: streamlit run multi_agent_decision_system\interfaces\streamlit_app.py
pause