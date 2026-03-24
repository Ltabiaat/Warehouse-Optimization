# Order-Driven Task Generation

Purpose: define how operational data becomes forklift task sequences.

## Architecture role

This is the layer between:
- normalized sales/order/inventory signals
- the Gymnasium warehouse environment

It turns warehouse work demand into explicit forklift tasks.

## First scope

Start with outbound work.

Inputs:
- normalized warehouse movement/order rows
- item/location context
- optional processing rules
- optional dropoff defaults

Outputs:
- `OrderLineTask`
- `TaskSequence`

## First task shape

An outbound task should capture:
- order reference
- item code / name
- quantity
- pickup location or zone
- optional processing zone
- dropoff type / zone
- client id
- simple priority score

## First sequence shape

For MVP, turn each task into an ordered sequence such as:
- `pickup:A`
- `process:QC`
- `dropoff:OUT`

or, if no explicit zone exists:
- `pickup_location:LOC-A`
- `dropoff_type:outbound_dock`

## Current assumptions

- outbound quantity is the current demand signal
- `location_no` and/or `floor_code` provide pickup context
- dropoff can default to an outbound dock/zone
- some items may require an extra processing zone (e.g. QC, cold handling, packing)

## Next evolution

Later this should incorporate:
- real sales orders
- real inventory location maps
- dock selection logic
- inbound putaway tasks
- transfer tasks
- richer priority rules
