from fastapi import FastAPI, Request
from ipaddress import ip_address
import asyncio, uvicorn

app = FastAPI()

def normalize_ip(ip: str) -> str:
    try:
        ip_obj = ip_address(ip)
        if ip_obj.version == 6 and ip_obj.ipv4_mapped:
            return str(ip_obj.ipv4_mapped)
        return str(ip_obj)
    except ValueError:
        return ip

@app.get("/myip")
async def get_my_ip(request: Request):
    client_host = normalize_ip(request.client.host)
    return {"ip": client_host}

@app.get("/check-port/{port}")
async def check_port(request: Request, port: int):
    client_host = normalize_ip(request.client.host)

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
    uvicorn.run("main:app", host="::", port=8000, reload=True)
