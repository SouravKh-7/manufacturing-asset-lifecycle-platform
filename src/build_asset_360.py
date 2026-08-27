import csv

asset_file = "data/processed/asset_master_valid.csv"
maintenance_file = "data/processed/maintenance_work_orders_valid.csv"
health_file = "data/gold/asset_health.csv"
reliability_file = "data/gold/asset_reliability.csv"
output_file = "data/gold/asset_360.csv"

assets = {}


# --------------------------------
# Load Asset Master
# --------------------------------

with open(asset_file, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:

        asset_id = row["asset_id"]

        assets[asset_id] = {
            "asset_id": asset_id,
            "asset_name": row["asset_name"],
            "asset_type": row["asset_type"],
            "plant_code": row["plant_code"],
            "criticality": row["criticality"],
            "status": row["status"],
            "maintenance_events": 0,
            "total_maintenance_cost": 0.0,
            "total_downtime_minutes": 0,
            "health_score": "",
            "health_status": "",
            "failure_events": 0,
            "mttr_minutes": 0,
            "availability_percent": 0,
        }


# --------------------------------
# Aggregate Maintenance
# --------------------------------

with open(maintenance_file, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:

        asset_id = row["asset_id"]

        if asset_id in assets:

            assets[asset_id]["maintenance_events"] += 1

            assets[asset_id]["total_maintenance_cost"] += float(
                row["maintenance_cost"]
            )

            assets[asset_id]["total_downtime_minutes"] += int(
                row["downtime_minutes"]
            )


# --------------------------------
# Add Asset Health
# --------------------------------

with open(health_file, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:

        asset_id = row["asset_id"]

        if asset_id in assets:

            assets[asset_id]["health_score"] = row[
                "health_score"
            ]

            assets[asset_id]["health_status"] = row[
                "health_status"
            ]

# --------------------------------
# Add Reliability KPIs
# --------------------------------

with open(reliability_file, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:

        asset_id = row["asset_id"]

        if asset_id in assets:

            assets[asset_id]["failure_events"] = row[
                "failure_events"
            ]

            assets[asset_id]["mttr_minutes"] = row[
                "mttr_minutes"
            ]

            assets[asset_id]["availability_percent"] = row[
                "availability_percent"
            ]
# --------------------------------
# Write Asset 360 Gold
# --------------------------------

fieldnames = [
    "asset_id",
    "asset_name",
    "asset_type",
    "plant_code",
    "criticality",
    "status",
    "maintenance_events",
    "total_maintenance_cost",
    "total_downtime_minutes",
    "health_score",
    "health_status",
    "failure_events",
    "mttr_minutes",
    "availability_percent",
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
    writer.writerows(assets.values())


print("Asset 360 records:", len(assets))
print("Gold dataset created:", output_file)