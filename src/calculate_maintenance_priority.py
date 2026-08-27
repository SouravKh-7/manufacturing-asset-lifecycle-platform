import csv

asset_360_file = "data/gold/asset_360.csv"
output_file = "data/gold/maintenance_priority.csv"

records = []


with open(asset_360_file, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:

        score = 0

        health_score = int(row["health_score"])
        downtime = int(row["total_downtime_minutes"])
        failures = int(row["failure_events"])
        criticality = row["criticality"]

        # Health risk
        if health_score < 50:
            score += 40
        elif health_score < 70:
            score += 30
        elif health_score < 85:
            score += 15

        # Criticality risk
        if criticality == "HIGH":
            score += 20
        elif criticality == "MEDIUM":
            score += 10

        # Failure history
        score += failures * 15

        # Downtime
        if downtime >= 300:
            score += 20
        elif downtime >= 120:
            score += 10

        if score >= 60:
            priority = "HIGH"
        elif score >= 30:
            priority = "MEDIUM"
        else:
            priority = "LOW"

        records.append({
            "asset_id": row["asset_id"],
            "asset_name": row["asset_name"],
            "health_score": health_score,
            "failure_events": failures,
            "downtime_minutes": downtime,
            "criticality": criticality,
            "priority_score": score,
            "maintenance_priority": priority,
        })


records.sort(
    key=lambda x: x["priority_score"],
    reverse=True,
)


fieldnames = [
    "asset_id",
    "asset_name",
    "health_score",
    "failure_events",
    "downtime_minutes",
    "criticality",
    "priority_score",
    "maintenance_priority",
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
    writer.writerows(records)


print("Priority records:", len(records))
print("Priority dataset created:", output_file)