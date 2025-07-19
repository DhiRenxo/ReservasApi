from pydantic import BaseModel

class GoogleLoginRequest(BaseModel):
    google_token: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"