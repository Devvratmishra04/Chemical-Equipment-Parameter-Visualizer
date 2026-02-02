# Chemical Equipment Parameter Visualizer

This project is a hybrid application involving a Django Backend, React Web Frontend, and PyQt5 Desktop Frontend.

## Prerequisites
Before running the application, ensure you have the following installed:
- **Python 3.10+** (Ensure it's added to your PATH)
- **Node.js** (LTS version recommended) & **npm**

## Setup & Running Instructions

### 1. Backend Setup (Django)
The backend serves as the core API and data processor.

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Install Python Dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    pip install -r ../requirements.txt
    ```

3.  **Run Migrations:**
    Initialize the database:
    ```bash
    python manage.py migrate
    ```

4.  **Start the Server:**
    ```bash
    python manage.py runserver
    # Server will start at http://127.0.0.1:8000/
    ```

### 2. Web Frontend Setup (React + Vite)
The web interface allows for file uploads, historical view, and visualization.

1.  **Navigate to the frontend directory:**
    Open a new terminal and run:
    ```bash
    cd frontend
    ```

2.  **Install Node Modules:**
    ```bash
    npm install
    ```

3.  **Start Development Server:**
    ```bash
    npm run dev
    # Access the web app at http://localhost:5173/ (or the port shown in terminal)
    ```

### 3. Desktop Frontend (PyQt5)
Alternatively, you can run the desktop application.

1.  **Run from the root directory:**
    Open a new terminal in the project root (`C:\FOSSEE\`) and run:
    ```bash
    python -m desktop.main
    ```

### Stopping the Application
To stop running the servers (Frontend or Backend), simply press `Ctrl + C` in the respective terminal window.

## Troubleshooting
- **ModuleNotFoundError**: Ensure you installed dependencies in the correct environment.
- **Connection Refused**: Ensure the Django backend is running on port 8000 before using the frontend.
