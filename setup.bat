@echo off
echo Setting up Unified Study Calculator Backend...

echo.
echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Creating database tables...
python -c "from app import create_app; app = create_app(); app.app_context().push(); from app import db; db.create_all(); print('Database tables created successfully!')"

echo.
echo Setup complete! You can now run the backend with:
echo python run.py

pause