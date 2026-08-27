import csv
from datetime import datetime

asset_master_file = "data/raw/asset_master.csv"
telemetry_file = "data/raw/iot_telemetry.csv"

valid_asset_ids = set()

valid_operating_states = {
    "RUNNING",
    "IDLE",
    "STOPPED",
}

errors = []

# Load known assets
with open(asset_master_file, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        if row["asset_id"].startswith("AST-"):
            valid_asset_ids.add(row["asset_id"])


# Validate telemetry
with open(telemetry_file, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    telemetry_count = 0

    for row_number, row in enumerate(reader, start=2):
        telemetry_count += 1

        # Rule 1: Asset must exist
        if row["asset_id"] not in valid_asset_ids:
            errors.append(
                f"Row {row_number}: Unknown asset_id {row['asset_id']}"
            )

        # Rule 2: Timestamp format
        try:
            datetime.fromisoformat(row["event_timestamp"])
        except ValueError:
            errors.append(
                f"Row {row_number}: Invalid event_timestamp"
            )

        # Rule 3: Operating state
        if row["operating_state"] not in valid_operating_states:
            errors.append(
                f"Row {row_number}: Invalid operating_state {row['operating_state']}"
            )

        # Rule 4: Temperature
        try:
            temperature = float(row["temperature_c"])

            if temperature < -20 or temperature > 200:
                errors.append(
                    f"Row {row_number}: temperature_c outside valid range"
                )

        except ValueError:
            errors.append(
                f"Row {row_number}: temperature_c must be numeric"
            )

        # Rule 5: Vibration
        try:
            vibration = float(row["vibration_mm_s"])

            if vibration < 0 or vibration > 50:
                errors.append(
                    f"Row {row_number}: vibration_mm_s outside valid range"
                )

        except ValueError:
            errors.append(
                f"Row {row_number}: vibration_mm_s must be numeric"
            )

        # Rule 6: RPM
        try:
            rpm = int(row["rpm"])

            if rpm < 0:
                errors.append(
                    f"Row {row_number}: rpm cannot be negative"
                )

        except ValueError:
            errors.append(
                f"Row {row_number}: rpm must be an integer"
            )

        # Rule 7: Current
        try:
            current = float(row["current_amp"])

            if current < 0:
                errors.append(
                    f"Row {row_number}: current_amp cannot be negative"
                )

        except ValueError:
            errors.append(
                f"Row {row_number}: current_amp must be numeric"
            )

        # Rule 8: Pressure
        try:
            pressure = float(row["pressure_bar"])

            if pressure < 0:
                errors.append(
                    f"Row {row_number}: pressure_bar cannot be negative"
                )

        except ValueError:
            errors.append(
                f"Row {row_number}: pressure_bar must be numeric"
            )


print("Telemetry records:", telemetry_count)
print("Known assets:", len(valid_asset_ids))

if errors:
    print("FAIL: Telemetry validation errors found.")

    for error in errors:
        print("-", error)
else:
    print("PASS: All telemetry data-quality checks passed.")
# Rule 8: Pressure
try:
    pressure = float(row["pressure_bar"])

    if pressure < 0:
        errors.append(
            f"Row {row_number}: pressure_bar cannot be negative"
        )

except ValueError:
    errors.append(
        f"Row {row_number}: pressure_bar must be numeric"
    )