from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import database

import subprocess
import os
from fastapi import BackgroundTasks


def run_shutdown():
    """Executes the Git save-and-kill routine script."""
    # Find the absolute path to our shutdown script
    script_path = os.path.join(os.path.dirname(__file__), 'shutdown.sh')
    subprocess.run(["bash", script_path])
    

app = FastAPI()

# Allow CORS requests securely from any web browser or GitHub Pages link
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enforce initialization checklist on startup
database.init_db()

class LoginRequest(BaseModel):
    username: str
    password: str
    
class CreateUserRequest(BaseModel):
    username: str
    password: str


@app.post("/login")
def handle_login(data: LoginRequest):
    """Verifies user credentials from frontend requests."""
    is_valid = database.verify_admin(data.username, data.password)
    if is_valid:
        return {"status": "authorized", "token": f"mock_session_key_{data.username}"}
    else:
        raise HTTPException(status_code=401, detail="Authentication mismatched entries.")

@app.get("/records")
def get_records():
    """Serves raw data objects to display on the database page layout."""
    try:
        return database.fetch_all_users()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/add-admin")
def create_admin(data: CreateUserRequest):
    """Processes new administrative records submitted via the frontend form."""
    if not data.username or not data.password:
        raise HTTPException(status_code=400, detail="Fields cannot be left blank.")
        
    success = database.add_new_admin(data.username, data.password)
    
    if success:
        return {"status": "success", "message": f"Account '{data.username}' registered successfully!"}
    else:
        raise HTTPException(status_code=400, detail="Username already exists in the system.")
                
@app.post("/exit-session")
def exit_session(background_tasks: BackgroundTasks):
    """Securely triggers a database commit and workflow termination."""
    # Run the shutdown in the background so the server has time to reply 'Success' to the browser first
    background_tasks.add_task(run_shutdown)
    return {"status": "terminating", "message": "Save sequence active. Cloud runner closing down safely."}
    
