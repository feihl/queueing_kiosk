from flask import Flask, render_template, jsonify, url_for

app = Flask(__name__)

queue_numbers = {
    "Express Bill Payment": {"prefix": "A", "number": 0, "current": 0, "serving": 0},
    "In-Hospital Pharmacy": {"prefix": "B", "number": 0, "current": 0, "serving": 0},
    "Appointment Scheduling": {"prefix": "C", "number": 0, "current": 0, "serving": 0},
    "Lab Test Sample Collection": {"prefix": "D", "number": 0, "current": 0, "serving": 0},
}

@app.route('/')
def index():
    return render_template("index.html", services=queue_numbers)

@app.route('/next/<service>')
def next_queue(service):
    if service in queue_numbers:
        queue_numbers[service]["number"] += 1
        queue_numbers[service]["current"] = queue_numbers[service]["number"]
    return jsonify(queue_numbers)

@app.route('/serve/<service>')
def serve_queue(service):
    if service in queue_numbers:
        queue_numbers[service]["serving"] = queue_numbers[service]["current"]
    return jsonify(queue_numbers)

@app.route('/back/<service>')
def back_queue(service):
    if service in queue_numbers and queue_numbers[service]["current"] > 0:
        queue_numbers[service]["current"] -= 1
    return jsonify(queue_numbers)

@app.route('/reset/<service>')
def reset_queue(service):
    if service in queue_numbers:
        queue_numbers[service]["number"] = 0
        queue_numbers[service]["current"] = 0
        queue_numbers[service]["serving"] = 0
    return jsonify(queue_numbers)

@app.route('/display')
def display():
    return render_template("display_only.html", services=queue_numbers)

@app.route('/queue_status')
def queue_status():
    """Return the current status of all queues as JSON for AJAX updates"""
    return jsonify(queue_numbers)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)