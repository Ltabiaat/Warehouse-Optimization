# Sample CSV Fixtures

These files are development fixtures that mirror the expected real-world warehouse tracker exports without containing sensitive data.

## Files

- `GR FL Tracker Units Case Study D.csv`
  - device index / lookup file
  - lists the available `device_id` values used by the other CSVs

- `gr-fl-v3-0033.csv`
  - sample forklift trajectory data at 1 Hz
  - includes position, orientation quaternion, and uncertainty fields

- `gr-fl-v3-0033_STATE.csv`
  - sample device state / BLE beacon data
  - includes ready state, load beacon fields, and up to 5 driver beacon detections

## Notes

- Each sample CSV contains 15 data rows.
- The trajectory CSV intentionally includes a couple of high-uncertainty rows near the end so downstream validation can test bad-data filtering.
- These files should be safe to use for schema design, ingestion code, and tests before working with sensitive customer data.
