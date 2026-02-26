from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
from jose import jwt
from app.db.session import get_db
from app.db.models import User
from app.core.settings import settings

router = APIRouter(prefix="/auth", tags=["auth"])
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

class RegisterReq(BaseModel):
    email: EmailStr
    password: str

class LoginReq(RegisterReq):
    pass

@router.post('/register')
async def register(payload: RegisterReq, db: AsyncSession = Depends(get_db)):
    existing = await db.scalar(select(User).where(User.email==payload.email))
    if existing: raise HTTPException(400, 'Email exists')
    user = User(email=payload.email, password_hash=pwd.hash(payload.password))
    db.add(user); await db.commit(); await db.refresh(user)
    return {'id': user.id, 'email': user.email}

@router.post('/login')
async def login(payload: LoginReq, db: AsyncSession = Depends(get_db)):
    user = await db.scalar(select(User).where(User.email==payload.email))
    if not user or not pwd.verify(payload.password, user.password_hash):
        raise HTTPException(401, 'Invalid credentials')
    token = jwt.encode({'sub': str(user.id), 'role': user.role}, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return {'access_token': token, 'token_type': 'bearer'}
