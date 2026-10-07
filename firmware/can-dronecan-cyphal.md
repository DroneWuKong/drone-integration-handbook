# CAN, DroneCAN and Cyphal

CAN describes a transport/physical interface. DroneCAN and Cyphal define higher-level communication contracts. A CAN connector does not establish application-protocol compatibility.

## Integration matrix

| Layer | Record |
|---|---|
| Physical | Connector pinout, transceiver/voltage, bus power, grounding and termination |
| Transport | Classical CAN versus CAN FD, bit rates and interface support |
| Protocol | DroneCAN or exact Cyphal version/transport; do not infer from old “UAVCAN” branding |
| Data types | DSDL definitions/version, node identity and message/service identifiers |
| Firmware | Autopilot and peripheral releases, supported drivers and discovery method |

DroneCAN maintains its own specification and data types. Cyphal was known as UAVCAN before its renaming; name history does not make the two application protocols wire-compatible. [DroneCAN specification](https://dronecan.github.io/Specification/1._Introduction/) and [OpenCyphal guide/specification](https://opencyphal.org/), checked 2026-10-07.

## Observe before configuring

In software, replay a known capture with the matching decoder/data-type definitions. Record node-status messages, identity changes, missing transfers and decoder errors. Test duplicate node identity and absent data types explicitly. SocketCAN `vcan` can exercise software frame handling, but does not model electrical noise, power, termination or a particular peripheral's protocol behavior.

For a physical installation, use the exact manufacturer's wiring and termination documentation. Do not apply generic pinouts or terminate every node. A powered-bus test is separate from a decoder test. [DroneCAN hardware guidance](https://dronecan.github.io/Specification/8._Hardware_design_recommendations/) and [Linux SocketCAN](https://www.kernel.org/doc/html/latest/networking/can.html), checked 2026-10-07.

Retain the capture, decoder version and physical test boundary in the [evidence record](../field/evidence-record.md).
