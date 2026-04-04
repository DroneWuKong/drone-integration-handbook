# Tactical Accessories: Video Scramblers & Payload Systems

> **Forge cross-reference:** 5 entries in `video_scramblers`, 4 entries in `payload_droppers`  
> **Related handbook chapters:** Electronic Warfare, ESAD

## Video Scramblers

Video scramblers encrypt or obfuscate the analog or digital FPV video downlink to prevent adversaries from intercepting the operator's video feed. In contested environments, an unencrypted video link reveals the drone's camera view to anyone with a compatible receiver — effectively giving the enemy real-time intelligence about what the operator is seeing and targeting.

### Products Tracked

The Forge database tracks 5 video scrambler products, all from Ukrainian manufacturers developed during the ongoing conflict:

- **Carrier Electronics Chameleon** — Video encryption module from Carrier Electronics
- **Sezam Video Сезам-А** — Scrambler unit with matching decryptor (дешифратор)
- **Sezam Video Відеокрипт** — Alternative scrambler system, also with matching decryptor

These are paired devices: the scrambler flies on the drone, the decryptor sits at the ground station. Both ends must have matching keys for the operator to see the video feed.

### Integration Considerations

Video scramblers sit inline between the camera and the video transmitter (VTX). They add latency (typically 1–5 frames depending on implementation), weight (10–30g), and power draw. For FPV piloting where sub-frame latency matters, even a few milliseconds of added delay can affect flight feel.

The trade-off is operational: in a non-contested environment, video encryption adds weight and latency for no benefit. In a contested environment where the enemy is monitoring your video frequencies, unencrypted video is an operational security failure.

Digital video links (DJI, HDZero, Walksnail) have inherent scrambling from their digital protocols but are not cryptographically secure. Purpose-built scramblers provide stronger encryption guarantees.

## Payload Delivery Systems

Payload droppers are electromechanical release mechanisms that allow a drone to carry and release objects — from humanitarian supply drops to agricultural dispersal to ordnance delivery.

### Products Tracked

The Forge database tracks 4 payload dropper products from Carrier Electronics (Ukrainian manufacturer):

- **Carrier Electronics FPV v1.3 / v2.0** — Payload release mechanisms designed for FPV platforms
- **Carrier Electronics One v1.4 / Two v1.4 для Mavic 3** — Payload release mechanisms designed for DJI Mavic 3 platforms

### Integration Considerations

Payload systems require:

- **Servo or actuator channel** — Typically connected to an auxiliary PWM output on the flight controller. Betaflight, ArduPilot, and PX4 all support servo outputs on designated pads.
- **Weight and balance** — Payload shifts the CG (center of gravity). The drone must be tuned for loaded flight, and the pilot must be prepared for the CG shift at release.
- **Power** — Release mechanisms draw servo current. Budget the BEC capacity accordingly.
- **Safety** — For any payload that could cause harm if released inadvertently, an ESAD or equivalent safety system is required. See the ESAD chapter.

## Note on This Category

Both video scramblers and payload droppers in the Forge database are primarily Ukrainian-manufactured products developed for the ongoing conflict. They represent a rapidly evolving category where new products appear faster than traditional defense procurement can track. The descriptions in the database are minimal because many of these products have limited public documentation — they are field-developed tools distributed through military supply channels rather than commercial product launches.
