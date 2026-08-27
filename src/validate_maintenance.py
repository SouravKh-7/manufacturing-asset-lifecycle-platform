import csv
from datetime import datetime

asset_master_file = "data/raw/asset_master.csv"
maintenance_file = "data/raw/maintenance_work_orders.csv"

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

errors = []
seen_work_order_ids = set()


# -----------------------------
# Load Asset Master
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

    maintenance_count = 0

    for row_number, row in enumerate(reader, start=2):

        maintenance_count += 1

        work_order_id = row["work_order_id"]
        asset_id = row["asset_id"]

        # Rule 1: Work Order ID required
        if not work_order_id:
            errors.append(
                f"Row {row_number}: Missing work_order_id"
            )

        # Rule 2: Work Order ID must be unique
        if work_order_id in seen_work_order_ids:
            errors.append(
                f"Row {row_number}: Duplicate work_order_id {work_order_id}"
            )
        else:
            seen_work_order_ids.add(work_order_id)

        # Rule 3: Asset must exist
        if asset_id not in valid_asset_ids:
            errors.append(
                f"Row {row_number}: Asset ID {asset_id} does not exist in Asset Master"
            )

        # Rule 4: Maintenance type must be valid
        if row["maintenance_type"] not in valid_maintenance_types:
            errors.append(
                f"Row {row_number}: Invalid maintenance_type {row['maintenance_type']}"
            )

        # Rule 5: Status must be valid
        if row["status"] not in valid_statuses:
            errors.append(
                f"Row {row_number}: Invalid status {row['status']}"
            )

        # Rule 6: Maintenance cost must be numeric and non-negative
        try:
            maintenance_cost = float(row["maintenance_cost"])

            if maintenance_cost < 0:
                errors.append(
                    f"Row {row_number}: maintenance_cost cannot be negative"
                )

        except ValueError:
            errors.append(
                f"Row {row_number}: maintenance_cost must be numeric"
            )

        # Rule 7: Downtime must be numeric and non-negative
        try:
            downtime = int(row["downtime_minutes"])

            if downtime < 0:
                errors.append(
                    f"Row {row_number}: downtime_minutes cannot be negative"
                )

        except ValueError:
            errors.append(
                f"Row {row_number}: downtime_minutes must be an integer"
            )

        # Rule 8: Validate dates
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
                    f"Row {row_number}: completed_date cannot be before reported_date"
                )

        except ValueError:
            errors.append(
                f"Row {row_number}: Invalid date format"
            )


print("Maintenance records:", maintenance_count)
print("Known assets:", len(valid_asset_ids))


if errors:

    print("FAIL: Maintenance validation errors found.")

    for error in errors:
        print("-", error)

else:

    print("PASS: All maintenance data-quality checks passed.")