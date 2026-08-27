import csv
from datetime import datetime

asset_master_file = "data/raw/asset_master.csv"
maintenance_file = "data/raw/maintenance_work_orders.csv"

valid_output_file = "data/processed/maintenance_work_orders_valid.csv"
invalid_output_file = "data/quarantine/maintenance_work_orders_invalid.csv"

valid_asset_ids = set()

valid_maintenance_types = {
    "PREVENTIVE",
    "CORRECTIVE",
    "INSPECTION",
}

valid_statuses = {
    "OPEN",
    "IN_PROGRESS",
    "COMPLETED",
}

valid_records = []
invalid_records = []

seen_work_order_ids = set()


# -----------------------------
# Load valid Asset IDs
# -----------------------------

with open(asset_master_file, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        asset_id = row["asset_id"]

        if asset_id.startswith("AST-"):
            valid_asset_ids.add(asset_id)


# -----------------------------
# Validate Maintenance Records
# -----------------------------

with open(maintenance_file, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    fieldnames = reader.fieldnames

    for row_number, row in enumerate(reader, start=2):

        errors = []

        work_order_id = row["work_order_id"]
        asset_id = row["asset_id"]

        # Rule 1: Work Order ID required
        if not work_order_id:
            errors.append("Missing work_order_id")

        # Rule 2: Work Order ID unique
        if work_order_id in seen_work_order_ids:
            errors.append("Duplicate work_order_id")
        else:
            seen_work_order_ids.add(work_order_id)

        # Rule 3: Asset must exist
        if asset_id not in valid_asset_ids:
            errors.append("Asset does not exist in Asset Master")

        # Rule 4: Maintenance type
        if row["maintenance_type"] not in valid_maintenance_types:
            errors.append("Invalid maintenance_type")

        # Rule 5: Status
        if row["status"] not in valid_statuses:
            errors.append("Invalid status")

        # Rule 6: Maintenance cost
        try:
            maintenance_cost = float(row["maintenance_cost"])

            if maintenance_cost < 0:
                errors.append("maintenance_cost cannot be negative")

        except ValueError:
            errors.append("maintenance_cost must be numeric")

        # Rule 7: Downtime
        try:
            downtime = int(row["downtime_minutes"])

            if downtime < 0:
                errors.append("downtime_minutes cannot be negative")

        except ValueError:
            errors.append("downtime_minutes must be an integer")

        # Rule 8: Dates
        try:
            reported_date = datetime.strptime(
                row["reported_date"],
                "%Y-%m-%d"
            )

            completed_date = datetime.strptime(
                row["completed_date"],
                "%Y-%m-%d"
            )

            if completed_date < reported_date:
                errors.append(
                    "completed_date cannot be before reported_date"
                )

        except ValueError:
            errors.append("Invalid date format")

        # -----------------------------
        # Separate Valid / Invalid
        # -----------------------------

        if errors:
            row["error_reason"] = "; ".join(errors)
            invalid_records.append(row)
        else:
            valid_records.append(row)


# -----------------------------
# Write Valid Records
# -----------------------------

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


# -----------------------------
# Write Invalid Records
# -----------------------------

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


# -----------------------------
# Summary
# -----------------------------

print("Total records:", len(valid_records) + len(invalid_records))
print("Valid records:", len(valid_records))
print("Invalid records:", len(invalid_records))

print("Valid file:", valid_output_file)
print("Quarantine file:", invalid_output_file)