from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

import models
from database import get_db
from schema import UserSignup, UserResponse, UserLogin, Token
from security import create_access_token, hash_password, verify_password


router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"],
)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user_data: UserSignup, db: Annotated[Session, Depends(get_db)]):
    # Check if user already exists
    existing_user = (
        db.query(models.User).filter(models.User.email == user_data.email).first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )

    new_user = models.User(
        email=user_data.email,
        username=user_data.username,
        password_hash=hash_password(user_data.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Annotated[Session, Depends(get_db)]):
    user = (
        db.query(models.User).filter(models.User.username == user_data.username).first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    is_valid = verify_password(user_data.password, user.password_hash)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    token_payload = {"sub": user.email}

    access_token = create_access_token(data=token_payload)

    return {"access_token": access_token, "token_type": "bearer"}
