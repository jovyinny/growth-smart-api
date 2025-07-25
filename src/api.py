"""API routes."""

from typing import Annotated

from fastapi import Depends, FastAPI, status
from fastapi.responses import JSONResponse

from src.databae.config import Session, get_db_session
from src.databae.repository.auth import UserRepository
from src.schemas import UserResponseSchema, UserSchema

app = FastAPI(
    title="GrowSmart API",
    description="AI powered agriculture platform",
    version="1.0.0",
)


@app.post("/register")
async def register_user(
    user: UserSchema, db: Annotated[Session, Depends(get_db_session)]
) -> UserResponseSchema:
    """Register a new user."""
    result = UserRepository(db).create_user(user)
    if "error" in result:
        return JSONResponse(
            content={"error": result["error"], "status": result["status"]},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return result


@app.get("/prediction")
async def get_prediction() -> JSONResponse:
    """Get a prediction (placeholder)."""
    return JSONResponse(
        content={"message": "Prediction endpoint is under construction."},
        status_code=status.HTTP_200_OK,
    )
