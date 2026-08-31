# Manufacturing Asset Lifecycle Platform

This project is a small working example of how a manufacturing company can bring asset information into one place.

Factories usually store asset details, sensor readings, and maintenance records in different systems. This makes it difficult to understand the real condition of a machine or decide which machine needs attention first. This project connects those datasets through one permanent `asset_id` and creates a simple Asset 360 view.

## The idea

Every physical machine receives a permanent digital identity, such as `AST-000001`. The ID stays the same even if the machine moves to another plant or production line.

The platform uses this identity to connect three types of information:

- Asset master data: what the machine is, where it is installed, and how critical it is.
- IoT telemetry: temperature, vibration, speed, current, pressure, and operating state.
- Maintenance history: failures, repair work, cost, and downtime.

After checking and combining the data, the platform produces useful information about each asset's condition, health, reliability, and maintenance priority.

## How it works

```text
Raw asset, telemetry, and maintenance data
                    |
                    v
        Validate and clean the records
              /             \
             v               v
      Valid records     Invalid records
      data/processed    data/quarantine
             |
             v
  Condition, health, and reliability calculations
             |
             v
          Asset 360
             |
             v
      Maintenance priority
```

Invalid records are not silently deleted. They are moved to the quarantine folder so that someone can review and correct them. The sample raw data intentionally contains a few invalid records to demonstrate this behavior.

## What the project creates

- **Asset condition:** the latest telemetry reading for each asset.
- **Health score:** a score from 0 to 100 based on temperature, vibration, current, and operating state.
- **Reliability measures:** failure count, downtime, mean time to repair, and availability.
- **Asset 360:** one combined record containing the most important information about an asset.
- **Maintenance priority:** a ranked list showing which assets should receive attention first.

The current sample contains five valid manufacturing assets. It is an early MVP designed to demonstrate the data model and processing logic before adding databases, dashboards, live IoT feeds, or machine-learning models.

## Project structure

```text
data/
  raw/          Original input data
  processed/    Valid and cleaned records
  quarantine/   Invalid records that need review
  gold/         Final business-ready datasets
docs/           Business context and asset identity rules
src/            Python validation and processing scripts
```

## Run the project

The project uses only Python's standard library, so no extra packages are required. Python 3.9 or newer is recommended.

Run these commands from the project root in the order shown:

```bash
python src/validate_asset_master.py
python src/validate_maintenance.py
python src/validate_telemetry.py
python src/process_maintenance.py
python src/process_telemetry.py
python src/build_asset_condition.py
python src/calculate_health_score.py
python src/calculate_reliability.py
python src/build_asset_360.py
python src/calculate_maintenance_priority.py
```

The final results will be available in `data/gold/`. Start with:

- `asset_360.csv` for the combined view of every asset.
- `maintenance_priority.csv` for the ranked maintenance list.

## Future direction

This MVP can grow into a larger manufacturing platform with:

- A database and automated data pipelines.
- Live IoT data ingestion.
- Dashboards and alerts.
- Maintenance planning and work-order integration.
- Failure prediction and remaining useful life estimation.

The long-term goal is simple: give maintenance and operations teams one trusted view of every asset, so they can reduce downtime, plan maintenance better, and make informed decisions.
