from typing import Any, Optional, List
from pydantic import BaseModel


class SuccessResponse(BaseModel):
    success: bool = True
    message: str = "Operación exitosa."
    data: Optional[Any] = None


class ErrorResponse(BaseModel):
    success: bool = False
    message: str = "Ocurrió un error."
    errors: Optional[List[Any]] = None


class ValidationError(BaseModel):
    field: str
    message: str


class PaginatedResponse(BaseModel):
    success: bool = True
    message: str = "Consulta exitosa."
    data: List[Any]
    total: int
    page: int
    page_size: int
