from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import logging



# Turn off Flask's default request logging
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

app = Flask(__name__)

# Configure CORS to allow requests from HTTPS
CORS(app, resources={
    r"/*": {
        "origins": ["https://localhost:8000", "https://127.0.0.1:8000", "https://192.168.0.*:8000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Store the current steering value
current_steering_value = 0.0

# Store the current pedal values
gas_value = 0.0
brake_value = 0.0

@app.route('/')
def home():
    """Serve the homepage with navigation buttons"""
    return render_template('index.html')

@app.route('/SteeringWheel')
def steering_wheel():
    """Serve the steering wheel interface"""
    return render_template('steering_wheel.html')

@app.route('/Pedals')
def pedals():
    """Serve the pedals interface"""
    return render_template('pedals.html')

@app.route('/UpdateSteering')
def update_steering():
    """Endpoint to receive steering value updates"""
    global current_steering_value
    
    try:
        value = float(request.args.get('value', 0))
        # Clamp value between -1 and 1
        value = max(-1.0, min(1.0, value))
        current_steering_value = value
        
        return jsonify({
            'status': 'success',
            'steering_value': current_steering_value,
        })
    except (ValueError, TypeError):
        return jsonify({
            'status': 'error',
            'message': 'Invalid value parameter'
        }), 400

@app.route('/UpdatePedals')
def update_pedals():
    """Endpoint to receive gas and brake pedal values"""
    global gas_value, brake_value
    try:
        gas = float(request.args.get('gas', 0))
        brake = float(request.args.get('brake', 0))
        # Clamp values between 0 and 1
        gas = max(0.0, min(1.0, gas))
        brake = max(0.0, min(1.0, brake))
        gas_value = gas
        brake_value = brake

        return jsonify({
            'status': 'success',
            'gas': gas,
            'brake': brake
        })
    except (ValueError, TypeError):
        return jsonify({
            'status': 'error',
            'message': 'Invalid gas or brake parameter'
        }), 400

@app.route('/status')
def status():
    """Get current steering and pedal status"""
    return jsonify({
        'steering_value': current_steering_value,
        'gas_value': gas_value,
        'brake_value': brake_value
    })


if __name__ == '__main__':
    import threading
    
    def run_https():
        app.run(host='0.0.0.0', port=8000, debug=False, ssl_context=('cert.pem', 'key.pem'))
    
    def run_http():
        app.run(host='0.0.0.0', port=8001, debug=False)
    
    print("Starting Flask servers...")
    print("HTTPS server: https://localhost:8000 (for mobile browsers)")
    print("HTTP server: http://localhost:8001 (for Roblox HttpService)")
    print("Note: You'll need to accept the self-signed certificate warning for HTTPS")
    
    # Start HTTPS server in a separate thread
    https_thread = threading.Thread(target=run_https)
    https_thread.daemon = True
    https_thread.start()
    
    # Start HTTP server in main thread
    run_http()




