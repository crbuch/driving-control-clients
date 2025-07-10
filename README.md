# Driving Control Clients

A FastAPI-based web application that provides mobile-friendly driving controls using smartphone sensors and touch interfaces.

## Features

- **Steering Wheel Control**: Uses device orientation/gyroscope for steering input
- **Pedal Controls**: Touch-based gas and brake pedals
- **Real-time Updates**: Async endpoints for high-frequency data updates
- **Unified Architecture**: Single FastAPI app running on both HTTP and HTTPS ports

## Architecture

- **Single FastAPI App**: Same application instance runs on both ports
- **HTTPS (Port 8000)**: All endpoints for mobile browsers (requires SSL for gyroscope access)
- **HTTP (Port 8001)**: Same endpoints for external APIs (like Roblox, no SSL issues)
- **Shared Variables**: Module-level variables ensure instant synchronization

## Quick Start

**Windows:**
```batch
run.bat
```

**Manual:**
```bash
poetry install
poetry run python launch_unified.py
```

## API Endpoints

Available on both ports:
- `GET /` - Homepage with navigation
- `GET /SteeringWheel` - Steering wheel interface  
- `GET /Pedals` - Pedal controls interface
- `GET /UpdateSteering?value=X` - Update steering value (-1.0 to 1.0)
- `GET /UpdatePedals?gas=X&brake=Y` - Update pedal values (0.0 to 1.0)
- `GET /status` - Get current steering and pedal values

## Usage with Roblox

```lua
local HttpService = game:GetService("HttpService")
local res = HttpService:JSONDecode(game:HttpGet("http://localhost:8001/status"))
local steering = res.steering_value
local gas = res.gas_value  
local brake = res.brake_value
```

## Performance

- **Ultra-fast**: Direct module variable access, no IPC overhead
- **40+ requests/second**: Optimized for high-frequency polling
- **No sync issues**: Same app instance = perfect synchronization
