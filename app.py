from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import shared_state
import logging



# Turn off default request logging
log = logging.getLogger('hypercorn')
log.setLevel(logging.ERROR)

app = FastAPI()

# Configure CORS to allow requests from HTTPS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:8000", "https://127.0.0.1:8000", "https://192.168.0.*:8000"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

# Templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the homepage with navigation buttons"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/SteeringWheel", response_class=HTMLResponse)
async def steering_wheel(request: Request):
    """Serve the steering wheel interface"""
    return templates.TemplateResponse("steering_wheel.html", {"request": request})

@app.get("/Pedals", response_class=HTMLResponse)
async def pedals(request: Request):
    """Serve the pedals interface"""
    return templates.TemplateResponse("pedals.html", {"request": request})

@app.get('/UpdateSteering')
async def update_steering(value: float = 0):
    """Endpoint to receive steering value updates"""
    try:
        shared_state.update_steering(value)
        return JSONResponse({
            'status': 'success',
            'steering_value': shared_state.steering_value,
        })
    except (ValueError, TypeError):
        raise HTTPException(status_code=400, detail="Invalid value parameter")

@app.get('/UpdatePedals')
async def update_pedals(gas: float = 0, brake: float = 0):
    """Endpoint to receive gas and brake pedal values"""
    try:
        shared_state.update_pedals(gas, brake)
        return JSONResponse({
            'status': 'success',
            'gas': shared_state.gas_value,
            'brake': shared_state.brake_value
        })
    except (ValueError, TypeError):
        raise HTTPException(status_code=400, detail="Invalid gas or brake parameter")

@app.get('/status')
async def status():
    """Get current steering and pedal status"""
    return JSONResponse(shared_state.get_all())


if __name__ == '__main__':
    print("To run the servers, use:")
    print("HTTPS server: python -m hypercorn app:app --bind 0.0.0.0:8000 --certfile cert.pem --keyfile key.pem")
    print("HTTP server:  python -m hypercorn app:app --bind 0.0.0.0:8001")
    print("Or use the launcher scripts")




