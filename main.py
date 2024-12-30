from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from ipaddress import ip_address
import os, uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def normalize_ip(ip: str) -> str:
    try:
        ip_obj = ip_address(ip)
        if ip_obj.version == 6 and ip_obj.ipv4_mapped:
            return str(ip_obj.ipv4_mapped)
        return str(ip_obj)
    except ValueError:
        return ip

def get_client_ip(request: Request) -> str:
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.client.host
    return normalize_ip(ip)

async def is_port_open(client_host, port):
    try:
        if ip_address(client_host).version == 6:
            output = os.popen(f"nmap -sT -6 {client_host} -p {port}").read()
        else:
            output = os.popen(f"nmap -sT {client_host} -p {port}").read()
        for line in output.splitlines():
            if f"{port}/" in line:
                return line.split()[1]
        return "State not found"
    except Exception as e:
        return f"Error: {e}"

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")

@app.get("/myip")
async def api_get_my_ip(request: Request):
    client_host = get_client_ip(request)
    return {"ip": client_host}

@app.get("/", response_class=HTMLResponse)
async def get_my_ip(request: Request):
    client_host = get_client_ip(request)
    return templates.TemplateResponse("index.html", {"request": request, "ip": client_host, "port_status": None})

@app.get("/check-port/{port}")
async def api_check_port(request: Request, port: int):
    client_host = get_client_ip(request)

    status = await is_port_open(client_host, port)
    return {"host": client_host, "port": port, "status": status}

@app.post("/", response_class=HTMLResponse)
async def check_port(request: Request, port: int = Form(...)):
    client_host = get_client_ip(request)

    status = await is_port_open(client_host, port)
    return templates.TemplateResponse("index.html", {"request": request, "ip": client_host, "port_status": {"port": port, "status": status}})

if __name__ == '__main__':
    port = os.getenv("PORT", "8000")
    reload = os.getenv("RELOAD", "False")
    uvicorn.run("main:app", host="::", port=int(port), reload=bool(reload))
