# p1-dsmr-common

Shared compatibility helpers for Home Assistant P1/DSMR integrations.

This package does **not** implement a DSMR parser. Standard telegram parsing remains the responsibility of upstream [dsmr-parser](https://github.com/ndokter/dsmr_parser), as used by Home Assistant.

The purpose of this project is to keep compatibility behaviour shared between integrations such as `homey-p1-ha` and `ecoflow-p1-ha`:

- shared semantic mappings for upstream `dsmr-parser` values;
- local-mapping override support for backwards-compatible integration keys;
- temporary OBIS/spec extensions that are not yet available upstream;
- capability discovery, including measurements that appear after startup;
- common M-Bus normalization/classification helpers;
- compatibility helpers only where upstream `dsmr-parser` does not already model the data;
- shared fixtures and regression tests.

## Boundary

The shared package describes **what the meter reports**. Individual integrations remain responsible for:

- device transport (WebSocket, HTTP, etc.);
- Home Assistant entity descriptions and registration;
- translations and user-facing names;
- unique IDs and entity migrations;
- device-specific diagnostics.

Mapping resolution is local-first:

```python
resolved = resolve_mapping(upstream_name, local_mapping)
```

A local integration mapping wins when present; otherwise the shared global mapping is used.

## Status

Initial shared compatibility layer. The first consumers are expected to be:

- `chill-uk/homey-p1-ha`
- `chill-uk/ecoflow-p1-ha`
