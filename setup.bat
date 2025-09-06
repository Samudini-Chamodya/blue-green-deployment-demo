@echo off
echo 🚀 Setting up Blue-Green Deployment Demo

REM Create project structure
mkdir blue-green-demo\app\templates 2>nul
mkdir blue-green-demo\app\static 2>nul
mkdir blue-green-demo\blue_environment 2>nul
mkdir blue-green-demo\green_environment 2>nul
mkdir blue-green-demo\traffic_controller 2>nul
mkdir blue-green-demo\jenkins 2>nul
mkdir blue-green-demo\scripts 2>nul
cd blue-green-demo

REM Install Python requirements
echo 📦 Installing Python dependencies...
pip install -r requirements.txt

echo ✅ Setup completed!
echo.
echo 🎯 Next steps:
echo 1. Start Blue environment: cd blue_environment ^&^& python start.py
echo 2. Start Green environment: cd green_environment ^&^& python start.py
echo 3. Start Traffic Controller: cd traffic_controller ^&^& python controller.py
echo 4. Open admin panel: http://localhost:8000/admin
echo.
echo 🌐 Environment URLs:
echo    Blue (Port 5000): http://localhost:5000
echo    Green (Port 5001): http://localhost:5001
echo    Traffic Controller (Port 8000): http://localhost:8000