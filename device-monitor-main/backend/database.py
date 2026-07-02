"""
database.py

Handles all SQLite database operations.
"""

import sqlite3
from config import DATABASE_NAME


class Database:

    def __init__(self):
        self.db = DATABASE_NAME
        self.initialize()

    # ==========================================================
    # Create Tables
    # ==========================================================

    def initialize(self):

        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()

        # ---------------- Devices ----------------

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS devices(

            device_id TEXT PRIMARY KEY,

            device_type TEXT,

            device_name TEXT,

            manufacturer TEXT,

            model TEXT,

            firmware TEXT,

            serial_number TEXT,

            hardware_id TEXT,

            ip_address TEXT,

            mac_address TEXT,

            onvif_version TEXT

        )
        """)

        # ---------------- Live Metrics ----------------

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS live_metrics(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            device_id TEXT,

            connection_status TEXT,

            latency INTEGER,

            packet_loss REAL,

            stream_status TEXT,

            resolution TEXT,

            fps TEXT,

            bitrate TEXT,

            codec TEXT,

            timestamp TEXT

        )
        """)

        # ---------------- Alerts ----------------

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            device_id TEXT,

            level TEXT,

            title TEXT,

            message TEXT,

            timestamp TEXT,

            resolved INTEGER

        )
        """)

        # ---------------- Analytics ----------------

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS analytics(

            device_id TEXT PRIMARY KEY,

            average_latency REAL,

            maximum_latency REAL,

            minimum_latency REAL,

            connection_stability REAL,

            downtime REAL,

            health_score REAL,

            prediction TEXT,

            recommendation TEXT

        )
        """)

        conn.commit()
        conn.close()

    # ==========================================================
    # Save Device Information
    # ==========================================================

    def save_device(self, device):

        conn = sqlite3.connect(self.db)

        cursor = conn.cursor()

        cursor.execute("""

        INSERT OR REPLACE INTO devices(

        device_id,

        device_type,

        device_name,

        manufacturer,

        model,

        firmware,

        serial_number,

        hardware_id,

        ip_address,

        mac_address,

        onvif_version

        )

        VALUES(?,?,?,?,?,?,?,?,?,?,?)

        """,

        (

        device["device_id"],

        device["device_type"],

        device["device_name"],

        device["manufacturer"],

        device["model"],

        device["firmware"],

        device["serial_number"],

        device["hardware_id"],

        device["ip_address"],

        device["mac_address"],

        device["onvif_version"]

        )

        )

        conn.commit()
        conn.close()

    # ==========================================================
    # Save Live Metrics
    # ==========================================================

    def save_metrics(self, metrics):

        conn = sqlite3.connect(self.db)

        cursor = conn.cursor()

        cursor.execute("""

        INSERT INTO live_metrics(

        device_id,

        connection_status,

        latency,

        packet_loss,

        stream_status,

        resolution,

        fps,

        bitrate,

        codec,

        timestamp

        )

        VALUES(?,?,?,?,?,?,?,?,?,?)

        """,

        (

        metrics["device_id"],

        metrics["connection_status"],

        metrics["latency"],

        metrics["packet_loss"],

        metrics["stream_status"],

        metrics["resolution"],

        str(metrics["fps"]),

        str(metrics["bitrate"]),

        metrics["codec"],

        metrics["timestamp"]

        )

        )

        conn.commit()
        conn.close()

    # ==========================================================
    # Latest Reading
    # ==========================================================

    def latest_metrics(self):

        conn = sqlite3.connect(self.db)

        conn.row_factory = sqlite3.Row

        row = conn.execute("""

        SELECT *

        FROM live_metrics

        ORDER BY id DESC

        LIMIT 1

        """).fetchone()

        conn.close()

        if row:

            return dict(row)

        return None

    # ==========================================================
    # Metrics History
    # ==========================================================

    def history(self, limit=50):

        conn = sqlite3.connect(self.db)

        conn.row_factory = sqlite3.Row

        rows = conn.execute("""

        SELECT *

        FROM live_metrics

        ORDER BY id DESC

        LIMIT ?

        """,(limit,)).fetchall()

        conn.close()

        return [dict(r) for r in rows]

    # ==========================================================
    # Device Information
    # ==========================================================

    def get_device(self, device_id):

        conn = sqlite3.connect(self.db)

        conn.row_factory = sqlite3.Row

        row = conn.execute("""

        SELECT *

        FROM devices

        WHERE device_id=?

        """,(device_id,)).fetchone()

        conn.close()

        if row:

            return dict(row)

        return None

    # ==========================================================
    # All Devices
    # ==========================================================

    def get_devices(self):

        conn = sqlite3.connect(self.db)

        conn.row_factory = sqlite3.Row

        rows = conn.execute("""

        SELECT *

        FROM devices

        """).fetchall()

        conn.close()

        return [dict(r) for r in rows]


db = Database()