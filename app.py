from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from ml_model import predict_availability, predict_peak_hours, suggest_best_time

app = Flask(__name__)
CORS(app)

def get_db():
    return sqlite3.connect("database.db")

# ---------------- AUTH ----------------

@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    db = get_db()
    db.execute("INSERT INTO users (name,email,password) VALUES (?,?,?)",
               (data["name"], data["email"], data["password"]))
    db.commit()
    return jsonify({"message": "User registered successfully"})

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE email=? AND password=?",
                      (data["email"], data["password"])).fetchone()
    if user:
        return jsonify({"message": "Login successful", "user_id": user[0]})
    return jsonify({"message": "Invalid credentials"}), 401

# ---------------- PARKING AREAS ----------------

@app.route("/api/parking-areas", methods=["GET"])
def get_parking_areas():
    db = get_db()
    rows = db.execute("SELECT * FROM parking_areas").fetchall()
    return jsonify(rows)

@app.route("/api/parking-areas", methods=["POST"])
def add_parking_area():
    data = request.json
    db = get_db()
    db.execute("INSERT INTO parking_areas (name,total_slots) VALUES (?,?)",
               (data["name"], data["total_slots"]))
    db.commit()
    return jsonify({"message": "Parking area added"})

# ---------------- SLOTS ----------------

@app.route("/api/slots", methods=["GET"])
def get_slots():
    parking_id = request.args.get("parking_id")
    db = get_db()
    slots = db.execute("SELECT * FROM slots WHERE parking_id=?",
                       (parking_id,)).fetchall()
    return jsonify(slots)

@app.route("/api/slots/<int:slot_id>", methods=["PUT"])
def update_slot(slot_id):
    data = request.json
    db = get_db()
    db.execute("UPDATE slots SET status=? WHERE id=?",
               (data["status"], slot_id))
    db.commit()
    return jsonify({"message": "Slot updated"})

# ---------------- BOOKING ----------------

@app.route("/api/book-slot", methods=["POST"])
def book_slot():
    data = request.json
    db = get_db()
    db.execute("INSERT INTO bookings (user_id,slot_id,time) VALUES (?,?,?)",
               (data["user_id"], data["slot_id"], data["time"]))
    db.execute("UPDATE slots SET status='Booked' WHERE id=?",
               (data["slot_id"],))
    db.commit()
    return jsonify({"message": "Slot booked"})

@app.route("/api/cancel-booking/<int:booking_id>", methods=["DELETE"])
def cancel_booking(booking_id):
    db = get_db()
    slot_id = db.execute(
        "SELECT slot_id FROM bookings WHERE id=?", (booking_id,)
    ).fetchone()[0]
    db.execute("DELETE FROM bookings WHERE id=?", (booking_id,))
    db.execute("UPDATE slots SET status='Available' WHERE id=?", (slot_id,))
    db.commit()
    return jsonify({"message": "Booking cancelled"})

@app.route("/api/bookings/user/<int:user_id>")
def user_bookings(user_id):
    db = get_db()
    bookings = db.execute("SELECT * FROM bookings WHERE user_id=?",
                          (user_id,)).fetchall()
    return jsonify(bookings)

# ---------------- AI / ML ----------------

@app.route("/api/predict/availability")
def availability():
    return jsonify(predict_availability())

@app.route("/api/predict/peak-hours")
def peak_hours():
    return jsonify(predict_peak_hours())

@app.route("/api/predict/best-time")
def best_time():
    return jsonify(suggest_best_time())

# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)
