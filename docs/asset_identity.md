# Asset Digital Identity

## Purpose

Every physical manufacturing asset in the company will have one permanent digital identity.

This identity will allow different systems such as maintenance records, IoT sensors, asset registers, and failure records to refer to the same physical machine.

---

## Asset ID Format

Every physical manufacturing asset receives a permanent enterprise-wide identifier.

Format:

AST-<SEQUENCE>

Examples:

- AST-000001
- AST-000002
- AST-000003
- AST-000004

Plant, asset type, production line, manufacturer, and location are stored as separate attributes.

They are not encoded inside the permanent Asset ID.

---

## Plant Codes

| Plant | Code |
|---|---|
| Jaipur Manufacturing Plant | JPR |
| Pune Manufacturing Plant | PUN |
| Chennai Manufacturing Plant | CHN |

---

## Asset Type Codes

| Asset Type | Code |
|---|---|
| CNC Machine | CNC |
| Grinding Machine | GRD |
| Motor | MOTOR |
| Pump | PUMP |
| Compressor | COMP |
| Furnace | FURNACE |

---

## Design Rules

1. Asset ID must be globally unique.
2. Asset ID must never change after creation.
3. Asset ID must never be reused.
4. Asset location may change without changing Asset ID.
5. Asset production line may change without changing Asset ID.
6. Asset status may change without changing Asset ID.
7. All operational datasets must reference the same Asset ID.

---

## Example

Asset:

AST-000001

Current attributes:

Plant: Jaipur Manufacturing Plant

Plant Code: JPR

Asset Type: CNC Machine

Asset Type Code: CNC

Production Line: LINE-01

If the machine later moves from Jaipur to Pune:

Asset ID remains:

AST-000001

Only the plant/location information changes.