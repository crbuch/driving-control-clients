"""
Simple HTTP server that only serves the /status endpoint.
Uses shared module variables (same as HTTPS server since it's the same app).
"""
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import shared_state

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

@app.get('/status')
async def status():
    """Get current steering and pedal status from shared variables"""
    return JSONResponse(shared_state.get_all())

if __name__ == '__main__':
    import uvicorn
    print("Starting HTTP server on port 8001 (status endpoint only)...")
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="error")
