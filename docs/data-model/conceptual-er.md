# Conceptual manufacturing ER model

**State:** Current business model

Plant, production line, and asset type are attributes in the current CSV implementation. They are shown as conceptual entities to make the business relationships explicit.

```mermaid
erDiagram
    PLANT ||--o{ PRODUCTION_LINE : contains
    PLANT ||--o{ ASSET : operates
    PRODUCTION_LINE ||--o{ ASSET : contains
    ASSET_TYPE ||--o{ ASSET : classifies
    ASSET ||--o{ TELEMETRY_READING : generates
    ASSET ||--o{ MAINTENANCE_WORK_ORDER : receives

    PLANT {
        string plant_code PK
        string plant_name
    }
    PRODUCTION_LINE {
        string production_line_id PK
        string plant_code FK
    }
    ASSET_TYPE {
        string asset_type_code PK
        string asset_type_name
    }
    ASSET {
        string asset_id PK
        string plant_code FK
        string production_line_id FK
        string asset_type_code FK
        string status
    }
    TELEMETRY_READING {
        string asset_id FK
        datetime event_timestamp
        string operating_state
    }
    MAINTENANCE_WORK_ORDER {
        string work_order_id PK
        string asset_id FK
        date reported_date
        string status
    }
```

