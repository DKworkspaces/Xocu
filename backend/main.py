from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import database

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
