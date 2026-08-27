import csv
import re

input_file = "data/raw/asset_master.csv"

valid_output_file = "data/processed/asset_master_valid.csv"
invalid_output_file = "data/quarantine/asset_master_invalid.csv"

valid_plants = {"JPR", "PUN", "CHN"}

valid_asset_types = {
    "CNC Machine",
    "Grinding Machine",
    "Motor",
    "Pump",
    "Compressor",
    "Furnace",
}

valid_criticality = {"LOW", "MEDIUM", "HIGH"}

valid_status = {
    "ACTIVE",
    "MAINTENANCE",
    "INACTIVE",
    "RETIRED",
}

valid_records = []
invalid_records = []

seen_asset_ids = set()


with open(input_file, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    fieldnames = reader.fieldnames

    for row_number, row in enumerate(reader, start=2):

        errors = []

        asset_id = row["asset_id"]

        # Rule 1: Asset ID format
        if not re.fullmatch(r"AST-\d{6}", asset_id):
            errors.append("Invalid asset_id")

        # Rule 2: Plant code
        if row["plant_code"] not in valid_plants:
            errors.append("Invalid plant_code")

        # Rule 3: Asset type
        if row["asset_type"] not in valid_asset_types:
            errors.append("Invalid asset_type")

        # Rule 4: Criticality
        if row["criticality"] not in valid_criticality:
            errors.append("Invalid criticality")

        # Rule 5: Status
        if row["status"] not in valid_status:
            errors.append("Invalid status")

        # Rule 6: Required fields
        required_fields = [
            "asset_id",
            "asset_name",
            "asset_type",
            "plant_code",
            "manufacturer",
            "model",
            "serial_number",
            "installation_date",
            "criticality",
            "status",
        ]

        for field in required_fields:
            if not row[field].strip():
                errors.append(f"Missing {field}")

        # Rule 7: Duplicate Asset ID
        if asset_id in seen_asset_ids:
            errors.append("Duplicate asset_id")
        else:
            seen_asset_ids.add(asset_id)

        # Separate good and bad records
        if errors:
            row["error_reason"] = "; ".join(errors)
            invalid_records.append(row)
        else:
            valid_records.append(row)


# Write valid records
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


# Write invalid records
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