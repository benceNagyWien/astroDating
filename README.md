# AstroDate API Backend

This is the backend for the AstroDate project, built with FastAPI.

## Requirements

The following Python packages are required to run the server. They can be installed via `pip`.

- `fastapi`
- `uvicorn[standard]`
- `sqlmodel`
- `faker`

You can install them all by running the following command inside the activated virtual environment:
```bash
pip install fastapi "uvicorn[standard]" sqlmodel faker
```

## Running the Development Server

1.  **Activate the virtual environment:**
    Make sure you are in the project's root directory.
    ```bash
    source backend/venv/bin/activate
    ```
    *(On Windows, use: `backend\venv\Scripts\activate`)*

2.  **Start the server:**
    From the project's root directory, run:
    ```bash
    uvicorn backend.main:app --reload
    ```
    - The `--reload` flag will automatically restart the server when you make changes to the code.
    - The API will be available at `http://localhost:8000`.
    - The interactive API documentation (Swagger UI) will be available at `http://localhost:8000/docs`.
