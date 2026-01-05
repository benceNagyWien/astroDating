# AstroDate

## Running the Application

### Backend (FastAPI)

1. **Navigate to the backend directory:**
   ```bash
   cd astroLokal/backend
   ```
2. **Install dependencies (if not already installed):**
   ```bash
   pip install fastapi "uvicorn[standard]" sqlmodel faker
   ```
3. **Run the development server:**
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at `http://localhost:8000`.

   **Note:** If port 8000 is already in use, you can specify a different port:
   ```bash
   uvicorn main:app --reload --port 8001
   ```

### Frontend (Vue.js)

1. **Navigate to the frontend directory:**
   ```bash
   cd astroLokal/frontend
   ```
2. **Install dependencies (if not already installed):**
   ```bash
   npm install
   ```
3. **Run the development server:**
   ```bash
   npm run dev
   ```
   The frontend will be available at the address specified by Vite (usually `http://localhost:5173`).