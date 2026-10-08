from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    usuario: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: str
    nombre: str
    rol: str


class UserInfo(BaseModel):
    id: int
    usuario: str
    nombre: str
    rol: str
    activo: bool

    class Config:
        from_attributes = True
