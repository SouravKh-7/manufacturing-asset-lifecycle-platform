import csv
from datetime import datetime

telemetry_file = "data/processed/iot_telemetry_valid.csv"
output_file = "data/gold/asset_condition.csv"

latest_readings = {}


with open(telemetry_file, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:

        asset_id = row["asset_id"]

        timestamp = datetime.fromisoformat(
            row["event_timestamp"]
        )

        if asset_id not in latest_readings:
            latest_readings[asset_id] = row

        else:
            existing_timestamp = datetime.fromisoformat(
                latest_readings[asset_id]["event_timestamp"]
            )

            if timestamp > existing_timestamp:
                latest_readings[asset_id] = row


fieldnames = [
    "asset_id",
    "event_timestamp",
    "temperature_c",
    "vibration_mm_s",
    "rpm",
    "current_amp",
    "pressure_bar",
    "operating_state",
]


with open(
    output_file,
    "w",
    newline="",
    encoding="utf-8",
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames,
    )

    writer.writeheader()

    for row in latest_readings.values():

        writer.writerow({
            field: row[field]
            for field in fieldnames
        })


print("Assets with telemetry:", len(latest_readings))
print("Condition dataset created:", output_file)