# app.py
from flask import Flask, request
import socket, time, uuid

app = Flask(__name__)

@app.get("/")
def homepage():
    return {
        "message": "Welcome to Big Sale!",
        "pod": socket.gethostname(),
        "ts": time.time()
    }

@app.post("/orders")
def place_order():
    order_id = str(uuid.uuid4())[:8]
    return {
        "order_id": order_id,
        "status": "placed",
        "served_by_pod": socket.gethostname()
    }, 201

@app.get("/orders/<order_id>")
def order_status(order_id):
    return {
        "order_id": order_id,
        "status": "processing",
        "served_by_pod": socket.gethostname()
    }

@app.get("/health")
def health():
    return {"status": "healthy", "pod": socket.gethostname()}

