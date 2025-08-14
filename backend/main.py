from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

class LoginData(BaseModel):
    username: str
    password: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Fake users database
fake_users = {"alice": "password123", "bob": "secret543"}

@app.post("/api/auth/login")
def login(data: LoginData, response: Response):
    username = data.username
    password = data.password

    if username in fake_users and fake_users[username] == password:
        # Set HTTP-only cookie to mimic EUA ID
        response.set_cookie(
            key="session",
            value=username,
            httponly=True,
            samesite="strict",
        )

        return {"user": username}
    return JSONResponse({"error": "Invalid credentials"}, status_code=401)

@app.get("/api/auth/status")
def status(request: Request):
    username = request.cookies.get("session")
    return {"user": username} if username else {"user": None}

@app.post("/api/auth/logout")
def logout(response: Response):
    response.delete_cookie("session")
    return { "success": True}