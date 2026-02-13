import sqlite3

DB_NAME = "database.db"

def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # ---------------- USERS TABLE ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # ---------------- PARKING AREAS TABLE ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS parking_areas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        location TEXT,
        total_slots INTEGER NOT NULL
    )
    """)

    # ---------------- SLOTS TABLE ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS slots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        parking_id INTEGER,
        status TEXT CHECK(status IN ('Available','Booked','Occupied')),
        FOREIGN KEY (parking_id) REFERENCES parking_areas(id)
    )
    """)

    # ---------------- BOOKINGS TABLE ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        slot_id INTEGER,
        booking_time TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (slot_id) REFERENCES slots(id)
    )
    """)

    conn.commit()
    conn.close()


def insert_sample_data():
    conn = get_connection()
    cursor = conn.cursor()

    # Insert parking areas
    cursor.execute("""
    INSERT OR IGNORE INTO parking_areas (id, name, location, total_slots)
    VALUES (1, 'City Mall Parking', 'Downtown', 10)
    """)

    # Insert slots
    for i in range(1, 11):
        cursor.execute("""
        INSERT OR IGNORE INTO slots (id, parking_id, status)
        VALUES (?, 1, 'Available')
        """, (i,))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    insert_sample_data()
    print("Database initialized successfully")
