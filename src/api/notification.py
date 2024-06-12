from fastapi import WebSocket
import asyncio
from common.database_connection import get_db
from common.websocket import ConnectionManager
from common.helper import get_user_ws
from fastapi import APIRouter, Depends, Response
from controller.NotificationController import NotificationController

manager = ConnectionManager()

router = APIRouter(prefix="/ws/notifications", tags=["notifications"])

@router.websocket("")
async def websocket_endpoint(websocket: WebSocket, token: str, session = Depends(get_db)):
    await manager.connect(websocket)
    try:
        user = get_user_ws(token, session)
        while True:
            action = await websocket.receive_json()
            controller = NotificationController(user, session)
            result = controller.action(action)
            await websocket.send_json(result)
    except Exception as e:
        manager.disconnect(websocket)
