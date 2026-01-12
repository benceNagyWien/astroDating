# AstroDate

This document provides instructions for setting up and running both the backend and frontend components of the AstroDate application.

---

## Backend (FastAPI)

The backend is a FastAPI application that serves the API for AstroDate. It features an automated setup process for the development database.

### Backend Setup and First Run

Follow these steps to get the backend running.

**1. Navigate to the Backend Directory**

```bash
cd astrodating/backend
```

**2. Create and Activate a Python Virtual Environment**

It is crucial to use a virtual environment to isolate project dependencies.

*   **Create the environment:**
    ```bash
    python3 -m venv venv
    ```

*   **Activate the environment:**
    *   On **macOS / Linux**:
        ```bash
        source venv/bin/activate
        ```
    *   On **Windows**:
        ```bash
        .\venv\Scripts\activate
        ```
    Your terminal prompt should now be prefixed with `(venv)`.

**3. Install Dependencies**

Install all required Python packages from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

**4. Run the Development Server**

```bash
uvicorn main:app --reload
```

The API will be running at `http://127.0.0.1:8000`.

### Development Database Behavior

For a consistent development experience, the backend is configured to do the following **on every startup**:

1.  **Delete the Database**: The existing `astrodate.db` file is automatically deleted.
2.  **Recreate Database**: A new, empty `astrodate.db` file and all necessary tables are created.
3.  **Seed Data**: The database is automatically populated with:
    *   Static data (Zodiac signs and their compatibility).
    *   100 fake users for testing purposes.
    *   The default password for all fake users is `password123`.

Because of this behavior, the `astrodate.db` file is included in `.gitignore` and should not be committed to version control.

### API Documentation

Once the server is running, you can access the automatically generated API documentation in your browser:

*   **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
*   **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Frontend (Vue.js)

The frontend is a Vue.js application built with Vite.

### Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd astrodating/frontend
    ```
2.  **Install dependencies (if not already installed):**
    ```bash
    npm install
    ```
3.  **Run the development server:**
    ```bash
    npm run dev
    ```
The frontend will be available at the address specified by Vite (usually `http://localhost:5173`).
