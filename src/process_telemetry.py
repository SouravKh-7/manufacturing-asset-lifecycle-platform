import csv
from datetime import datetime

asset_master_file = "data/raw/asset_master.csv"
telemetry_file = "data/raw/iot_telemetry.csv"

valid_output_file = "data/processed/iot_telemetry_valid.csv"
invalid_output_file = "data/quarantine/iot_telemetry_invalid.csv"

valid_asset_ids = set()

valid_operating_states = {
    "RUNNING",
    "IDLE",
    "STOPPED",
}

valid_records = []
invalid_records = []


# --------------------------------
# Load valid Asset IDs
# --------------------------------

with open(asset_master_file, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        if row["asset_id"].startswith("AST-"):
            valid_asset_ids.add(row["asset_id"])


# --------------------------------
# Validate Telemetry
# --------------------------------

with open(telemetry_file, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    fieldnames = reader.fieldnames

    for row_number, row in enumerate(reader, start=2):

        errors = []

        # Asset ID
        if row["asset_id"] not in valid_asset_ids:
            errors.append("Unknown asset_id")

        # Timestamp
        try:
            datetime.fromisoformat(row["event_timestamp"])
        except ValueError:
            errors.append("Invalid event_timestamp")

        # Operating state
        if row["operating_state"] not in valid_operating_states:
            errors.append("Invalid operating_state")

        # Temperature
        try:
            temperature = float(row["temperature_c"])

            if temperature < -20 or temperature > 200:
                errors.append("temperature_c outside valid range")

        except ValueError:
            errors.append("temperature_c must be numeric")

        # Vibration
        try:
            vibration = float(row["vibration_mm_s"])

            if vibration < 0 or vibration > 50:
                errors.append("vibration_mm_s outside valid range")

        except ValueError:
            errors.append("vibration_mm_s must be numeric")

        # RPM
        try:
            rpm = int(row["rpm"])

            if rpm < 0:
                errors.append("rpm cannot be negative")

        except ValueError:
            errors.append("rpm must be an integer")

        # Current
        try:
            current = float(row["current_amp"])

            if current < 0:
                errors.append("current_amp cannot be negative")

        except ValueError:
            errors.append("current_amp must be numeric")

        # Pressure
        try:
            pressure = float(row["pressure_bar"])

            if pressure < 0:
                errors.append("pressure_bar cannot be negative")

        except ValueError:
            errors.append("pressure_bar must be numeric")

        # Separate valid and invalid
        if errors:
            row["error_reason"] = "; ".join(errors)
            invalid_records.append(row)
        else:
            valid_records.append(row)


# --------------------------------
# Write valid telemetry
# --------------------------------

with open(
    valid_output_file,
    "w",
    newline="",
    encoding="utf-8",
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames,
    )

    writer.writeheader()
    writer.writerows(valid_records)


# --------------------------------
# Write quarantined telemetry
# --------------------------------

invalid_fieldnames = fieldnames + ["error_reason"]

with open(
    invalid_output_file,
    "w",
    newline="",
    encoding="utf-8",
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=invalid_fieldnames,
    )

    writer.writeheader()
    writer.writerows(invalid_records)


print("Total records:", len(valid_records) + len(invalid_records))
print("Valid records:", len(valid_records))
print("Invalid records:", len(invalid_records))
print("Valid file:", valid_output_file)
print("Quarantine file:", invalid_output_file)