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

## Database Seeding

The project includes a script to populate the database with realistic test data.

### What it does
The `seed.py` script uses the `Faker` library to create **100 fake users**. Each user is assigned a random birth date, a short bio, and one of the 100 profile pictures located in `backend/userImages/`.

This is useful for development and testing of the frontend and matching logic.

### How to run
1. Make sure your virtual environment is activated.
2. From the project's **root directory**, run the following command:
    ```bash
    python -m backend.seed
    ```
This will directly execute the script and populate the database.

