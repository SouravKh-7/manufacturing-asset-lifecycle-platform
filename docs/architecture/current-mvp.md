# Current Python MVP architecture

**State:** Implemented

```mermaid
flowchart TD
    A[Raw CSV sources]
    B[Python validation]
    C[Processed CSV files]
    D[Quarantine files]
    E[Condition and health calculations]
    F[Reliability calculations]
    G[Combined machine summary]
    H[Maintenance priority]

    A --> B
    B --> C
    B --> D
    C --> E
    C --> F
    E --> G
    F --> G
    G --> H
```

The diagram represents the current file-based implementation. It does not represent Databricks, streaming, CDC, or production orchestration.
