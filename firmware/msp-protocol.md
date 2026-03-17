# Chapter 6: MSP Protocol — The Betaflight/iNav Language

> MSP is a question-and-answer protocol. You ask the FC a question
> (send a request with a function code). It answers (sends a
> response with the data). No streaming, no subscriptions,
> no surprises.

---

## What MSP Is

MSP (MultiWii Serial Protocol) is the serial communication protocol
used by Betaflight and iNav. It's been around since the MultiWii
days and has evolved through several versions. The current version
is **MSP v2**, which supports 16-bit function codes and CRC8
checksums.

MSP is simple by design. It runs over any serial connection (UART,
USB, TCP, Bluetooth) at any baud rate. There are no connection
handshakes, no sessions, no state. Send a request, get a response.

---

## Packet Format

### MSP v2 Request (outgoing)

```
Byte:  0     1     2     3     4-5       6     7-8       9..N     N+1
       $     X     <     flag  func_id   0x00  payload   payload  crc8
       0x24  0x58  0x3C  0x00  [16-bit]  0x00  size[16]  [data]   [crc]
```

| Field | Size | Value | Description |
|-------|------|-------|-------------|
| Header | 3 bytes | `$X<` | MSP v2 request marker |
| Flag | 1 byte | 0x00 | Reserved |
| Function ID | 2 bytes | Little-endian | Which data you're requesting |
| Payload size | 2 bytes | Little-endian | 0 for most requests |
| Payload | variable | — | Data (for SET commands) |
| CRC8 | 1 byte | DVB-S2 CRC | Over flag + func_id + size + payload |

### MSP v2 Response (incoming)

```
Byte:  0     1     2     3     4-5       6-7       8..N     N+1
       $     X     >     flag  func_id   size      payload  crc8
       0x24  0x58  0x3E  0x00  [16-bit]  [16-bit]  [data]   [crc]
```

Same structure but with `>` (0x3E) instead of `<` (0x3C).

---

## The Messages That Matter

### Identity

| Function | ID | Direction | Returns |
|----------|----|-----------|---------|
| MSP_FC_VARIANT | 0x02 | Read | 4-byte ASCII: "BTFL" or "INAV" |
| MSP_FC_VERSION | 0x03 | Read | 3 bytes: major, minor, patch |
| MSP_BOARD_INFO | 0x04 | Read | Board identifier, manufacturer, board name |

These are the first messages to send on any new connection. They
tell you what firmware is running, what version, and what hardware
it's running on.

**Auto-detect pattern:** Send MSP_FC_VARIANT. If you get "BTFL",
it's Betaflight. If "INAV", it's iNav. If no response within 2
seconds, it's not an MSP firmware (try MAVLink).

### PID Tuning

| Function | ID | Direction | Payload |
|----------|----|-----------|---------|
| MSP_PID | 0x70 | Read | 9 bytes: [Roll P, Roll I, Roll D, Pitch P, Pitch I, Pitch D, Yaw P, Yaw I, Yaw D] |
| MSP_SET_PID | 0xCA | Write | Same 9 bytes |

Each value is 0-255. The FC interprets these differently by firmware
version (scaling factors change between BF 4.3 and 4.4, for example).
Always record the firmware version alongside PID values.

### Rates

| Function | ID | Direction | Payload |
|----------|----|-----------|---------|
| MSP_RC_TUNING | 0x6B | Read | Rate values (format depends on rate type) |
| MSP_SET_RC_TUNING | 0xCC | Write | Same format |

Rate payload format depends on the configured rate type (Betaflight
rates, Actual rates, KISS rates, Quick rates). Read
`rates_type` from the RC tuning response to know how to interpret
the values.

### Filters

| Function | ID | Direction | Payload |
|----------|----|-----------|---------|
| MSP_FILTER_CONFIG | 0x5E | Read | Gyro lowpass, D-term lowpass, notch filters, dynamic notch settings |
| MSP_SET_FILTER_CONFIG | 0xC9 | Write | Same format |

### Battery

| Function | ID | Direction | Payload |
|----------|----|-----------|---------|
| MSP_BATTERY_STATE | 0x82 | Read | Cell count, capacity, voltage (mV), current (cA), mAh consumed |
| MSP_ANALOG | 0x6E | Read | Voltage, power (mAh), RSSI, current |

### Blackbox

| Function | ID | Direction | Payload |
|----------|----|-----------|---------|
| MSP_BLACKBOX_CONFIG | 0x5C | Read | Device (flash/SD), rate, conditions |
| MSP_DATAFLASH_SUMMARY | 0x70 | Read | Total size, used size, ready flag |
| MSP_DATAFLASH_READ | 0x71 | Read | Address + data chunk (~4 KB) |
| MSP_DATAFLASH_ERASE | 0x72 | Write | Erases all flash (10-30 sec) |

Blackbox download is the most bandwidth-intensive MSP operation.
At 115200 baud, downloading 2 MB of flash takes ~3 minutes. At
921600 baud (via ESP32 bridge), it takes ~20 seconds.

### Motor Control

| Function | ID | Direction | Payload |
|----------|----|-----------|---------|
| MSP_MOTOR | 0x68 | Read | 8x uint16: motor values (1000-2000 or DShot) |
| MSP_SET_MOTOR | 0xD6 | Write | Same format — TEST MODE ONLY |

MSP_SET_MOTOR bypasses the PID controller and directly sets motor
outputs. **Props must be removed when using this.** This is for
motor direction testing, not flight.

### EEPROM

| Function | ID | Direction | Description |
|----------|----|-----------|-------------|
| MSP_EEPROM_WRITE | 0xF9 | Write | Saves current settings to EEPROM |

**Always send MSP_EEPROM_WRITE after SET commands.** Without it,
your changes are lost on the next reboot.

---

## Write Safety Pattern

Never write to an FC without this sequence:

1. **Read** the current value (snapshot before)
2. **Show** the diff to the operator (before vs after)
3. **Get approval** (operator confirms)
4. **Write** the new value via MSP_SET_*
5. **Read back** to verify the FC accepted it
6. **Compare** read-back to what you wrote
7. **EEPROM write** after all changes in the batch
8. **Log** every change with timestamp, old value, new value

Step 5 is critical. Some FC firmware versions silently clamp
values to valid ranges. If you write P=200 and read back P=150,
the FC clamped it. Your operator needs to know.

---

## Practical Tips

**Baud rate:** MSP works at any baud rate, but the FC UART must
be configured to match. Betaflight defaults MSP-configured UARTs
to 115200. You can change this in the Ports tab. For blackbox
download speed, 921600 is recommended.

**Timeout:** If you send a request and don't get a response within
100 ms, the FC didn't understand it (wrong function code, wrong
firmware version, or the UART isn't configured for MSP). Retry
once, then try a different approach.

**Versioning:** MSP function codes and payload formats change
between firmware versions. A message that works on BF 4.4 may
not exist on BF 4.2. Always detect the firmware version
(MSP_FC_VERSION) before sending version-specific messages.

**Multiple MSP ports:** An FC can have multiple UARTs configured
for MSP simultaneously. This is useful for connecting both a
configurator and a companion computer. Each port operates
independently.

**MSP over WiFi:** The ESP32 bridge (Tooth, SpeedyBee adapter)
wraps MSP in TCP. The byte stream is identical to serial — the
same parser works on both USB and TCP transport. The only difference
is the connection setup.

---

## Next

- **Chapter 7: MAVLink Protocol** — the other language, for ArduPilot
  and PX4.
- **Chapter 8: UART Layout** — where to put your MSP connections.

---

*MSP is simple. That's its strength. Ask a question, get an answer.
No handshakes, no state, no negotiation. The protocol stays out of
the way so you can focus on the data.*
