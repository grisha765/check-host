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
            await asyncio.wait_for(asyncio.open_connection(client_host, port), timeout=5)
            return "open"
        except asyncio.TimeoutError:
            return "filtered"
        except ConnectionRefusedError:
            return "closed"
        except Exception as e:
            return f"error: {str(e)}"

    status = await is_port_open()
    return {"host": client_host, "port": port, "status": status}

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
