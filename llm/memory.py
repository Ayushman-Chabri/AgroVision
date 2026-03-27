import json
import os
from datetime import datetime

DB_FILE = "farm_records.json"

def save_to_json(combined_ctx: dict):
    record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "district": combined_ctx.get("district"),
        "soil": combined_ctx.get("soil_type"),
        "crop": combined_ctx.get("crop_name"),
        "investment": combined_ctx.get("investment"),
        "month": combined_ctx.get("month_of_cropping")
    }

    existing_data = []
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            try: existing_data = json.load(f)
            except: existing_data = []

    existing_data.append(record)
    with open(DB_FILE, "w") as f:
        json.dump(existing_data, f, indent=4)

def get_last_record(district: str):
    if not os.path.exists(DB_FILE): return None
    with open(DB_FILE, "r") as f:
        try:
            records = json.load(f)
            dist_records = [r for r in records if r['district'].lower() == district.lower()]
            return dist_records[-1] if dist_records else None
        except: return None