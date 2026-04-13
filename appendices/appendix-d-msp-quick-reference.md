# Appendix D — MSP Function Code Quick Reference

The 15 MSP codes you actually use for Betaflight/iNav FC integration.

MSP v1 frame: `$M< [size] [cmd] [payload] [crc]`
MSP v2 frame: `$X< [flags] [cmd_lo] [cmd_hi] [size_lo] [size_hi] [payload] [crc]`

Direction: `<` = to FC, `>` = from FC, `!` = error response.

---

## Identification

| Code | Name | Direction | Description |
|------|------|-----------|-------------|
| 1 | MSP_API_VERSION | Request | Protocol version. Payload: `[protocol_ver, api_major, api_minor]` |
| 2 | MSP_FC_VARIANT | Request | Firmware name. Returns 4-byte string: `BTFL`, `INAV`, `ARDU`, `CLFL` |
| 3 | MSP_FC_VERSION | Request | Firmware version. `[major, minor, patch]` |
| 4 | MSP_BOARD_INFO | Request | Board name string (8 bytes) + hardware rev |
| 100 | MSP_IDENT | Request | Legacy. Protocol version, type, capability flags |

---

## Status & Arming

| Code | Name | Direction | Description |
|------|------|-----------|-------------|
| 101 | MSP_STATUS | Request | Cycle time, I2C errors, sensor flags, flight mode, arming flags |
| 150 | MSP_STATUS_EX | Request | Extended status including arming disable flags |

**Arming check from MSP_STATUS:**
```
payload[9..10] = flags word
flags & 0x01 = armed
```

**Common arming disable flags (MSP_STATUS_EX payload[13..14]):**
- bit 0: No RC
- bit 2: Roll/Pitch not centered
- bit 3: Throttle not low
- bit 7: Calibrating

---

## PID & Rates

| Code | Name | Direction | Description |
|------|------|-----------|-------------|
| 111 | MSP_RC_TUNING | Request | Rates, expo, throttle curve. 14 bytes. |
| 112 | MSP_PID | Request | PID values. 30 bytes: 10 axes × [P, I, D]. |
| 202 | MSP_SET_PID | Send | Write PID values. Same 30-byte format as MSP_PID. |
| 204 | MSP_SET_RC_TUNING | Send | Write rate/expo settings. |

**MSP_PID payload layout:**
```
Byte 0,1,2   = ROLL  P, I, D
Byte 3,4,5   = PITCH P, I, D
Byte 6,7,8   = YAW   P, I, D
Byte 9..29   = ALT, POS, POSR, NAVR, LEVEL, MAG, VEL
```

---

## Filters

| Code | Name | Direction | Description |
|------|------|-----------|-------------|
| 92 | MSP_FILTER_CONFIG | Request | Gyro LPF, D-term LPF, notch filters |
| 223 | MSP_SET_FILTER_CONFIG | Send | Write filter settings |

---

## RC & Channels

| Code | Name | Direction | Description |
|------|------|-----------|-------------|
| 105 | MSP_RC | Request | Raw RC channel values (1000–2000). 32 channels max. |
| 200 | MSP_SET_RAW_RC | Send | Override RC channels. Use with caution — bypasses failsafe. |

---

## Sensors

| Code | Name | Direction | Description |
|------|------|-----------|-------------|
| 102 | MSP_RAW_IMU | Request | Raw accelerometer (±512), gyro (±16384), magnetometer (±1024) |
| 108 | MSP_ALTITUDE | Request | Altitude (cm), vario (cm/s) |
| 109 | MSP_ANALOG | Request | Voltage (0.1V units), mAh used, RSSI, amperage |

---

## Persistence

| Code | Name | Direction | Description |
|------|------|-----------|-------------|
| 250 | MSP_EEPROM_WRITE | Send | **Persist all pending changes to flash.** No payload. FC may briefly pause. Call after any SET command or changes are lost on reboot. |

---

## Write Sequence

Always follow this order for parameter write-back:

```
1. Check MSP_STATUS — confirm not armed (flags & 0x01 == 0)
2. MSP_FC_VARIANT   — confirm expected firmware
3. MSP_PID          — snapshot before state
4. MSP_SET_PID      — write new values
5. MSP_PID          — verify-read (confirm FC accepted)
6. MSP_SET_RC_TUNING (if rates changed)
7. MSP_RC_TUNING    — verify-read
8. MSP_SET_FILTER_CONFIG (if filters changed)
9. MSP_EEPROM_WRITE — persist everything
10. Wait 300ms      — FC writes flash, briefly pauses
```

---

## CRC Calculation (MSP v1)

```python
def msp_crc(size, cmd, payload):
    crc = size ^ cmd
    for b in payload:
        crc ^= b
    return crc & 0xFF
```

---

## Common Gotchas

**EEPROM_WRITE is mandatory.** SET commands update RAM only. Power cycle without EEPROM_WRITE = all changes lost.

**Don't write while armed.** FC will ignore or return error. Check status first.

**Verify-read is not optional.** FC may silently reject values outside valid range. Always read back and compare.

**MSP_SET_RAW_RC overrides failsafe.** If your code crashes while RC override is active, the drone will fly away. Use MSP_SET_RAW_RC only for testing, never in production without a watchdog.

---

## Related

- [MSP Protocol Deep Dive](../firmware/msp-protocol.md)
- [MAVLink Quick Reference](appendix-c-mavlink-quick-reference.md)
- [Hangar FC Write-Back](../../../Ai-Project/hangar/src/main/kotlin/ai/wingman/hangar/fc/MspClient.kt)
