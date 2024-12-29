from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ipaddress import ip_address
import asyncio, uvicorn

app = FastAPI()

templates = Jinja2Templates(directory="templates")

def normalize_ip(ip: str) -> str:
    try:
        ip_obj = ip_address(ip)
        if ip_obj.version == 6 and ip_obj.ipv4_mapped:
            return str(ip_obj.ipv4_mapped)
        return str(ip_obj)
    except ValueError:
        return ip

async def is_port_open(client_host, port):
    try:
        await asyncio.wait_for(asyncio.open_connection(client_host, port), timeout=5)
        return "open"
    except asyncio.TimeoutError:
        return "filtered"
    except ConnectionRefusedError:
        return "closed"
    except Exception as e:
        return f"error: {str(e)}"

@app.get("/myip")
async def api_get_my_ip(request: Request):
    client_host = normalize_ip(request.client.host)
    return {"ip": client_host}

@app.get("/", response_class=HTMLResponse)
async def get_my_ip(request: Request):
    client_host = normalize_ip(request.client.host)
    return templates.TemplateResponse("index.html", {"request": request, "ip": client_host, "port_status": None})

@app.get("/check-port/{port}")
async def api_check_port(request: Request, port: int):
    client_host = normalize_ip(request.client.host)

    status = await is_port_open(client_host, port)
    return {"host": client_host, "port": port, "status": status}

@app.post("/", response_class=HTMLResponse)
async def check_port(request: Request, port: int = Form(...)):
    client_host = normalize_ip(request.client.host)

    status = await is_port_open(client_host, port)
    return templates.TemplateResponse("index.html", {"request": request, "ip": client_host, "port_status": {"port": port, "status": status}})

if __name__ == '__main__':
    uvicorn.run("main:app", host="::", port=8000, reload=True)
