from fastapi import FastAPI , WebSocket, WebSocketDisconnect 
from fastapi.responses import HTMLResponse


app = FastAPI()


# websocket functionalities 

class ConnectionManager:
    def __init__(self):
        self.active_connections:list[WebSocket] = []
    
    async def connect(self, websocket:WebSocket):
        await websocket.accept()
        
        self.active_connections.append(websocket)
        print(f"Connected ip : {self.active_connections}")

    async def disconnect(self, websocket:WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message:str, websocket:WebSocket):    
        await websocket.send_text(message)
    
    async def broadcast(self, message:str):
        print("broad cast")
        for connection in self.active_connections:
            await connection.send_text(message)
            print("send")




manager =  ConnectionManager()





@app.get("/")
async def get_value():
    print("Loading HTML file")
    with open("ui.html",'r') as html_file:
        html_content = html_file.read()
    return HTMLResponse(html_content)


@app.websocket("/ws/{client_id}")
async def websocket(client_id:int,websocket:WebSocket):
    print("Start websocket")
    await manager.connect(websocket)
    try:
        while True:
            message = await websocket.receive_text()
            await manager.send_personal_message(f"You says: {message}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {message}")

    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} has left from the chat")





if __name__ == "__main__":
    print("start")