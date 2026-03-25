# Orqa Hardware â Flight Controllers and FPV Systems

> Orqa is a Croatian company producing flight controllers and FPV goggles
> used across both commercial FPV and defense-adjacent applications. Their
> Croatian origin is relevant for US government procurement pathways.

---

## Product Line Overview

| Product | Type | MCU | Primary Use |
|---------|------|-----|-------------|
| Orqa F405 Pro | Flight Controller | STM32F405 | FPV racing/freestyle |
| Orqa WingCore H7 | Flight Controller | STM32H743 | Fixed-wing / autonomous |
| Orqa MRM2-10 H743 | Flight Controller | STM32H743 | Multi-rotor / advanced |
| Orqa FPV.One | FPV Goggles | â | Pilot display |
| Orqa FPV.Connect | Video/RC Module | â | Digital FPV link |

---

## Orqa F405 Pro

### Specifications
- **MCU:** STM32F405RGT6
- **Gyro:** ICM-42688-P
- **OSD:** Integrated
- **VTX Control:** SmartAudio
- **UARTs:** 6x
- **Target firmware:** Betaflight 4.4+

### Betaflight Setup

The ICM-42688-P gyro requires Betaflight 4.4 or later for full support.
Earlier versions have incomplete filter support for this sensor.

**Key CLI settings:**
```
set gyro_lpf1_static_hz = 0
set gyro_lpf2_static_hz = 0
set dyn_notch_count = 4
set motor_pwm_protocol = DSHOT600
```

---

## Orqa WingCore H7

The WingCore H7 is based on the STM32H743 and targets fixed-wing and
autonomous multi-rotor applications.

### Specifications
- **MCU:** STM32H743VIT6
- **Gyros:** Dual ICM-42688-P (IMU1 + IMU2)
- **Barometer:** DPS310
- **PWM Outputs:** 14
- **UARTs:** 6x
- **Target firmware:** PX4 (MatekH743 base), iNav

### ioTag Encoding

ioTag is a compact representation used in iNav/Betaflight firmware:
```
ioTag = (port_index << 4) | pin_number
// PA4 = (0 << 4) | 4 = 0x04
// PB8 = (1 << 4) | 8 = 0x18
```

### DFU Flashing

1. Hold BOOT button while connecting USB
2. Open STM32CubeProgrammer
3. Select USB DFU connection
4. Load .bin file (not .hex for DFU mode)
5. Click Start Programming

---

## Compliance

Orqa d.o.o. is Croatian with a Delaware US subsidiary (Orqa Inc.).
- Not a covered entity under NDAA Â§848
- FOCI mitigation may be required for classified DOD programs
- SAM.gov registration required for contracting
- TReX II consortium is a potential defense pathway

---

## Related

- [Flight Controller Selection](flight-controller-selection.md)
- [The Four Firmwares](../firmware/four-firmwares.md)
- [NDAA Compliance](ndaa-compliance.md)
