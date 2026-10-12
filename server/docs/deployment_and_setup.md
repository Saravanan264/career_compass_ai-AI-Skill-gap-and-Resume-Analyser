# CAREER COMPASS AI — DEPLOYMENT & SETUP GUIDE

> **Overview**: Step-by-step instructions for local development, production build, environment configuration, security safeguards, and deployment options for Career Compass AI.

---

## 1. SYSTEM PREREQUISITES
- **Operating System**: Windows 10/11, Linux (Ubuntu 20.04+), or macOS 12+
- **Python**: Version `3.10.x` or `3.11.x`
- **Node.js**: Version `18.x` or `20.x`
- **Package Managers**: `pip` (Python) & `npm` (Node.js)

---

## 2. BACKEND SETUP (PYTHON / FASTAPI)
1. Navigate to the `server` directory:
   ```bash
   cd server
   ```
2. Create a Python virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - **Windows**:
     ```powershell
     .\venv\Scripts\activate
     ```
   - **Linux / macOS**:
     ```bash
     source venv/bin/activate
     ```
4. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 3. FRONTEND SETUP (REACT / VITE)
1. Return to the root project directory:
   ```bash
   cd ..
   ```
2. Install frontend dependencies:
   ```bash
   npm install
   ```

---

## 4. ENVIRONMENT CONFIGURATION
Create a `.env` file inside the `server/` directory (refer to `server/.env.example`):

```env
# Database Configuration
DATABASE_URL=sqlite:///./career_compass.db

# Authentication Security
JWT_SECRET=supersecretjwtkey_replace_me_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Frontend Origin for CORS
FRONTEND_URL=http://localhost:5000

# Optional LLM Enhancement Layer (Default: Disabled)
LLM_ENABLED=false
LLM_PROVIDER=openai
LLM_API_KEY=your_openai_api_key_here
LLM_MODEL=gpt-4o-mini
```

---

## 5. DATABASE INITIALIZATION
The SQLite database (`server/career_compass.db`) is automatically initialized by SQLAlchemy models on the first backend server startup. No manual migration scripts or database setup commands are required.

---

## 6. RUNNING THE APPLICATION

### Option A: Windows Automated Startup
Double-click `run_project.bat` in the root folder, or execute:
```cmd
run_project.bat
```

### Option B: Manual Execution (Two Terminals)

- **Terminal 1 (Backend API)**:
  ```bash
  cd server
  .\venv\Scripts\activate
  uvicorn main:app --reload --port 8000
  ```
  *Backend API will run at `http://localhost:8000`*

- **Terminal 2 (Frontend App)**:
  ```bash
  npm run dev
  ```
  *Frontend Application will run at `http://localhost:5000`*

---

## 7. PRODUCTION BUILD
To validate and build the production static frontend assets:
```bash
npm run build
```
Output static files will be placed in the `dist/` directory.

---

## 8. OPTIONAL LLM SETUP & SAFEGUARD
- **Enabled**: Set `LLM_ENABLED=true` and provide a valid `LLM_API_KEY`.
- **Disabled**: Leave `LLM_ENABLED=false` or `LLM_API_KEY` empty.
- **Safety Assurance**: If disabled or unavailable, the backend automatically uses 100% deterministic fallback summaries. API keys remain strictly backend-only and are never exposed to the frontend or response payloads.

---

## 9. PRODUCTION DEPLOYMENT CONSIDERATIONS
1. **Web Server**: Use Gunicorn with Uvicorn worker class (`gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app`) behind an Nginx reverse proxy.
2. **Database Scale**: For multi-container deployments, update `DATABASE_URL` to a managed PostgreSQL instance (`postgresql://user:password@host:5432/dbname`).
3. **Model Caching**: Ensure disk storage allows downloading and caching the `SentenceTransformer` (`all-MiniLM-L6-v2`) model weights (~90MB).
4. **CORS Restrictions**: Update `FRONTEND_URL` to match your production domain.
