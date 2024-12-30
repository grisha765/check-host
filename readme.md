# check-host

A Python application using FastAPI to check your public IP address and verify if a specified port is open. This app provides a web interface and an API for checking the IP address and port status.

### Initial Setup

1. **Clone the repository**: Clone this repository using `git clone`.
2. **Create Virtual Env**: Create a Python Virtual Env `venv` to download the required dependencies and libraries.
3. **Download Dependencies**: Download the required dependencies into the Virtual Env `venv` using `pip`.

```shell
git clone https://github.com/grisha765/check-host.git
cd check-host
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt 
```

### Deploy

- Run:
    ```bash
    PORT="8000" RELOAD="True" .venv/bin/python main.py
    ```

#### Container

- Pull container:
    ```bash
    podman pull ghcr.io/grisha765/check-host:latest
    ```

- Deploy in container
    ```bash
    podman run -d \
    --name check-host \
    --privileged \
    --network host \
    -e PORT="8000" \
    ghcr.io/grisha765/check-host:latest
    ```

### Features

- Display the client's public IP address.
- Check the status of a specific port (open, closed, or filtered).
- Simple and user-friendly web interface.
- API endpoints for programmatic access.

