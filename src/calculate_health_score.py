import csv

condition_file = "data/gold/asset_condition.csv"
output_file = "data/gold/asset_health.csv"

health_records = []


with open(condition_file, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:

        health_score = 100

        temperature = float(row["temperature_c"])
        vibration = float(row["vibration_mm_s"])
        current = float(row["current_amp"])
        operating_state = row["operating_state"]


        # Temperature penalties
        if temperature >= 80:
            health_score -= 25
        elif temperature >= 70:
            health_score -= 15
        elif temperature >= 60:
            health_score -= 5


        # Vibration penalties
        if vibration >= 7:
            health_score -= 30
        elif vibration >= 5:
            health_score -= 20
        elif vibration >= 3:
            health_score -= 10


        # Current penalty
        if current >= 30:
            health_score -= 10


        # Operating-state penalty
        if operating_state == "STOPPED":
            health_score -= 10


        # Prevent score below zero
        health_score = max(health_score, 0)


        # Health classification
        if health_score >= 85:
            health_status = "HEALTHY"

        elif health_score >= 70:
            health_status = "MONITOR"

        elif health_score >= 50:
            health_status = "MAINTENANCE_RECOMMENDED"

        else:
            health_status = "CRITICAL"


        health_records.append({
            "asset_id": row["asset_id"],
            "health_score": health_score,
            "health_status": health_status,
            "temperature_c": temperature,
            "vibration_mm_s": vibration,
            "current_amp": current,
            "operating_state": operating_state,
        })


fieldnames = [
    "asset_id",
    "health_score",
    "health_status",
    "temperature_c",
    "vibration_mm_s",
    "current_amp",
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
    writer.writerows(health_records)


print("Health records:", len(health_records))
print("Health dataset created:", output_file)