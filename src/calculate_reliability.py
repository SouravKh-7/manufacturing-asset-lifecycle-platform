import csv

maintenance_file = "data/processed/maintenance_work_orders_valid.csv"
output_file = "data/gold/asset_reliability.csv"

metrics = {}


with open(maintenance_file, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:

        asset_id = row["asset_id"]

        if asset_id not in metrics:
            metrics[asset_id] = {
                "asset_id": asset_id,
                "maintenance_events": 0,
                "failure_events": 0,
                "total_downtime_minutes": 0,
            }

        metrics[asset_id]["maintenance_events"] += 1

        downtime = int(row["downtime_minutes"])

        metrics[asset_id]["total_downtime_minutes"] += downtime

        if row["failure_code"] != "NONE":
            metrics[asset_id]["failure_events"] += 1


# Assume a 30-day observation window for MVP
observation_minutes = 30 * 24 * 60


for asset in metrics.values():

    failures = asset["failure_events"]
    downtime = asset["total_downtime_minutes"]

    if failures > 0:
        asset["mttr_minutes"] = round(
            downtime / failures,
            2
        )
    else:
        asset["mttr_minutes"] = 0

    uptime_minutes = observation_minutes - downtime

    availability = (
        uptime_minutes / observation_minutes
    ) * 100

    asset["availability_percent"] = round(
        availability,
        2
    )


fieldnames = [
    "asset_id",
    "maintenance_events",
    "failure_events",
    "total_downtime_minutes",
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
    writer.writerows(metrics.values())


print("Reliability records:", len(metrics))
print("Reliability dataset created:", output_file)