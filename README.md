# AstroDating

## How to run the project

The startup script has been removed. Please start the frontend and backend separately.

### Backend

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```

2.  Create and activate a Python virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On macOS / Linux
    # For Windows, use: .\venv\Scripts\activate
    ```

3.  Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

4.  Start the backend server:
    ```bash
    uvicorn main:app --reload
    ```
    The server will be running on `http://127.0.0.1:8000`.

### Frontend

1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```

2.  Install the required Node.js packages:
    ```bash
    npm install
    ```

3.  Start the frontend development server:
    ```bash
    npm run dev
    ```
    The application will be accessible in your browser, usually at `http://localhost:5173`.