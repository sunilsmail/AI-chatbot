from fastapi import APIRouter, WebSocket
router = APIRouter()

@router.websocket('/ws/chat/{session_id}')
async def ws_chat(websocket: WebSocket, session_id: int):
    await websocket.accept()
    while True:
        text = await websocket.receive_text()
        await websocket.send_json({'session_id': session_id, 'echo': text})
