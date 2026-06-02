from typing import Annotated

from fastapi import APIRouter, Depends
from .auth import get_current_user

import models
from schema import UserResponse

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/")
def dashboard(current_user: Annotated[models.User, Depends(get_current_user)]):
    return {"message": "hello, world!"}
