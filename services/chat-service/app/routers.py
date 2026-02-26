from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.db.models import ChatMessage
from app.services.graph import run_chat_workflow

router = APIRouter(prefix='/chat', tags=['chat'])

class ChatReq(BaseModel):
    session_id: int
    user_id: int
    message: str

@router.post('/message')
async def chat_message(payload: ChatReq, db: AsyncSession = Depends(get_db)):
    user_msg = ChatMessage(session_id=payload.session_id, role='user', content=payload.message)
    db.add(user_msg)
    response = await run_chat_workflow(payload.user_id, payload.session_id, payload.message)
    db.add(ChatMessage(session_id=payload.session_id, role='assistant', content=response['response']))
    await db.commit()
    return response

@router.get('/history/{session_id}')
async def chat_history(session_id: int, db: AsyncSession = Depends(get_db)):
    msgs = (await db.scalars(select(ChatMessage).where(ChatMessage.session_id == session_id))).all()
    return [{'role': m.role, 'content': m.content, 'created_at': m.created_at} for m in msgs]
