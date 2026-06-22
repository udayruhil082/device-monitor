from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def save_reading(device, battery, latency_ms, connected):
    data = {
        "device": device,
        "battery": battery,
        "latency_ms": latency_ms,
        "connected": connected
    }
    result = supabase.table("device_readings").insert(data).execute()
    return result

def get_recent_readings(device_name, limit=30):
    result = (
        supabase.table("device_readings")
        .select("battery, latency_ms, connected, timestamp")
        .eq("device", device_name)
        .order("timestamp", desc=True)
        .limit(limit)
        .execute()
    )
    return result.data