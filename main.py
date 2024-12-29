from fastapi import FastAPI, Request
import asyncio, uvicorn

app = FastAPI()

@app.get("/myip")
async def get_my_ip(request: Request):
    client_host = request.client.host
    return {"ip": client_host}

@app.get("/check-port/{port}")
async def check_port(request: Request, port: int):
    client_host = request.client.host

    async def is_port_open():
        try:
            reader, writer = await asyncio.open_connection(client_host, port)
            writer.close()
            await writer.wait_closed()
            return "open"
        except ConnectionRefusedError:
            return "closed"
        except Exception:
            return "filtered"

    status = await is_port_open()
    return {"host": client_host, "port": port, "status": status}

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
