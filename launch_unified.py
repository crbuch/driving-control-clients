"""
Single server launcher that runs the same FastAPI app on both HTTP and HTTPS ports.
This ensures shared state since it's literally the same app instance.
"""
import asyncio
import uvicorn
import ssl
from app import app

async def run_both_servers():
    """Run the same app on both HTTP and HTTPS ports"""
    
    # Create SSL context
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain('cert.pem', 'key.pem')
    
    # HTTP server config (port 8001)
    http_config = uvicorn.Config(
        app=app,
        host="0.0.0.0",
        port=8001,
        log_level="error"
    )
    
    # HTTPS server config (port 8000) 
    https_config = uvicorn.Config(
        app=app,
        host="0.0.0.0", 
        port=8000,
        ssl_certfile='cert.pem',
        ssl_keyfile='key.pem',
        log_level="error"
    )
    
    # Create servers
    http_server = uvicorn.Server(http_config)
    https_server = uvicorn.Server(https_config)
    
    print("Starting FastAPI servers...")
    print("HTTPS server: https://localhost:8000 (for mobile browsers - all endpoints)")
    print("HTTP server: http://localhost:8001 (for Roblox - all endpoints)")
    print("Both servers share the same app instance and variables!")
    print("Press Ctrl+C to stop both servers")
    
    # Run both servers concurrently
    await asyncio.gather(
        http_server.serve(),
        https_server.serve()
    )

if __name__ == '__main__':
    try:
        asyncio.run(run_both_servers())
    except KeyboardInterrupt:
        print("\nShutting down servers...")
