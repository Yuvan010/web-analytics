from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)

# In-memory storage for demo purposes
vehicles = [
    {
        'id': 1,
        'plate': 'ABC-123',
        'model': 'Toyota Camry',
        'status': 'Active',
        'location': 'Downtown',
        'last_update': '10:30 AM'
    },
    {
        'id': 2,
        'plate': 'XYZ-789',
        'model': 'Honda Civic',
        'status': 'Maintenance',
        'location': 'Service Center',
        'last_update': '09:15 AM'
    }
]

alerts = [
    {'id': 1, 'type': 'Speed Alert', 'vehicle': 'ABC-123', 'time': '10:45 AM'},
    {'id': 2, 'type': 'Low Fuel', 'vehicle': 'XYZ-789', 'time': '09:30 AM'}
]

@app.route('/')
def home():
    return render_template('home.html', vehicles=vehicles[:3])

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', vehicles=vehicles, alerts=alerts)

@app.route('/fleet')
def fleet():
    return render_template('fleet.html', vehicles=vehicles)

@app.route('/alerts')
def alerts_page():
    return render_template('alerts.html', alerts=alerts)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/api/vehicle_status')
def vehicle_status():
    return jsonify({
        'total': len(vehicles),
        'active': len([v for v in vehicles if v['status'] == 'Active']),
        'maintenance': len([v for v in vehicles if v['status'] == 'Maintenance'])
    })

@app.route('/api/add_vehicle', methods=['POST'])
def add_vehicle():
    data = request.json
    new_vehicle = {
        'id': len(vehicles) + 1,
        'plate': data.get('plate'),
        'model': data.get('model'),
        'status': 'Active',
        'location': data.get('location', 'Unknown'),
        'last_update': datetime.now().strftime('%I:%M %p')
    }
    vehicles.append(new_vehicle)
    return jsonify({'success': True, 'vehicle': new_vehicle})

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    # In a real app, you would save this to a database
    return redirect(url_for('contact') + '?success=1')

if __name__ == '__main__':
    app.run(debug=True)