# Architectural and Design Decisions

This document records significant architectural and design decisions made during the development of this integration.

## Format

Each decision is documented with:

- **Date:** When the decision was made
- **Context:** Why this decision was necessary
- **Decision:** What was decided
- **Rationale:** Why this approach was chosen
- **Consequences:** Expected impacts and trade-offs

> [!NOTE]
> Guidance on _when_ a decision is worth recording here, and a copy-ready entry template, lives in the
> [`ha-planning`](../../.agents/skills/ha-planning/SKILL.md) agent skill.

---

## Decision Log

### Use DataUpdateCoordinator for All Data Fetching

**Date:** 2025-11-29 (Template initialization)

**Context:** The integration needs to fetch data from an external API and share it with multiple entities. Home Assistant provides several patterns for this.

**Decision:** Use `DataUpdateCoordinator` from `homeassistant.helpers.update_coordinator` as the central data management component.

**Rationale:**

- Provides built-in support for update intervals and error handling
- Automatic retry with exponential backoff
- Shared data access prevents duplicate API calls
- Standard pattern recommended by Home Assistant
- Entities automatically become unavailable when coordinator fails

**Consequences:**

- All entities must inherit from `CoordinatorEntity`
- Single update interval applies to all entities
- Data is fetched even if no entities are enabled
- Coordinator manages entity lifecycle and availability

---

### Separate API Client from Coordinator

**Date:** 2025-11-29 (Template initialization)

**Context:** The coordinator needs to fetch data, but business logic should be separated from data transport.

**Decision:** Implement API communication in separate `api/client.py` module, coordinator only orchestrates updates.

**Rationale:**

- Separation of concerns: transport vs. orchestration
- Easier to test API client in isolation
- Simpler to swap API implementation if needed
- Clearer error handling boundaries

**Consequences:**

- Additional abstraction layer
- Coordinator depends on API client
- API client raises custom exceptions for error translation

---

### Platform-Specific Directories

**Date:** 2025-11-29 (Template initialization)

**Context:** Integration supports multiple platforms (sensor, binary_sensor, switch, etc.).

**Decision:** Each platform gets its own directory with individual entity files.

**Rationale:**

- Clear organization as integration grows
- Easier to find specific entity implementations
- Supports multiple entities per platform cleanly
- Follows Home Assistant Core pattern

**Consequences:**

- More files/directories than single-file approach
- Platform `__init__.py` must import and register entities
- Slightly more initial setup overhead

---

### EntityDescription for Static Metadata

**Date:** 2025-11-29 (Template initialization)

**Context:** Entities have static metadata (name, icon, device class) that doesn't change.

**Decision:** Use `EntityDescription` dataclasses to define static entity metadata.

**Rationale:**

- Declarative and easy to read
- Type-safe with dataclasses
- Recommended Home Assistant pattern
- Separates static configuration from dynamic behavior

**Consequences:**

- Each entity type needs an EntityDescription
- Dynamic entities need custom handling
- Static and dynamic properties clearly separated

---

### Own aiohttp Client Instead of a PyPI Library

**Date:** 2026-08-19

**Context:** The integration talks to a single VKF hail-warning endpoint: an unauthenticated
`GET /devices/{id}/poll?hwtypeId={id}` returning `{"currentState": <int>}`. No PyPI package wraps this vendor API.

**Decision:** Implement `api/client.py` as a small `aiohttp`-based client using Home Assistant's shared client
session, rather than searching for or publishing a wrapping library.

**Rationale:**

- Per `AGENTS.md` § Custom Integration Flexibility, a maintained library is preferred only when it already fits; one
  unauthenticated GET endpoint with a two-field JSON response does not justify a dependency.
- No OAuth2, no complex protocol, no standard like MQTT that would argue for a library.

**Consequences:**

- If the vendor's API grows (authentication, more endpoints), this decision should be revisited.

---

### No Authentication Error Class, No Reauth Flow

**Date:** 2026-08-19

**Context:** `blueprint.coordinator.instructions.md` lists a three-exception hierarchy (`...Error`,
`...CommunicationError`, `...AuthenticationError`) as required for an API client, mirroring the blueprint's
username/password example. The VKF poll endpoint takes no credentials at all.

**Decision:** `api/__init__.py` defines only `HagelschutzVkfApiClientError` and
`HagelschutzVkfApiClientCommunicationError`. The config flow has no reauth step, and the coordinator never raises
`ConfigEntryAuthFailed`.

**Rationale:** There is nothing to authenticate and nothing that could be rejected as invalid credentials, so an
`AuthenticationError` class and a reauth flow would be dead code with no way to ever trigger.

**Consequences:**

- If the vendor later adds authentication (an API key, a token), this decision needs to be revisited alongside the
  API client and config flow.

---

## Future Considerations

### State Restoration

**Status:** Not yet implemented

Consider implementing state restoration for switches and configurable settings to maintain state across Home Assistant restarts when the external device is unavailable.

### Multi-Device Support

**Status:** Not yet implemented

Current architecture assumes single device per config entry. If multi-device support is needed, coordinator data structure will need redesign to map device ID → data.

### Polling vs. Push

**Status:** Uses polling

Currently implements polling-based updates. If the API supports webhooks or WebSocket, consider implementing push-based updates for real-time responsiveness.

---

## Decision Review

These decisions should be reviewed periodically (suggested: quarterly or when major features are added) to ensure they still serve the integration's needs.
