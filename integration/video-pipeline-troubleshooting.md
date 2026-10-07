# Video Pipeline Troubleshooting

Trace capture → encode → transport → jitter buffer → decode → display. Each stage has independent timestamps, counters and failure states. A functioning telemetry overlay does not prove the camera image is current.

## Failure isolation

| Symptom | Next observation |
|---|---|
| No session | Address, authentication/TLS, RTSP negotiation and selected transport |
| Session but no frames | Codec/caps, payload mapping, parameter sets and keyframes |
| Frames arrive but decode fails | Decoder support, damaged access units and packet-loss counters |
| Delay grows | Queue/jitter depth, retransmission, decode throughput and display pacing |
| Frozen image, moving OSD | Last decoded/displayed frame time versus last telemetry sample |
| Reconnect fails | Teardown, stale peer/session identity and bounded retry state |

RTSP session setup and RTP media transport are distinct. UDP loss and TCP retransmission can create different symptoms; neither has a universal latency guarantee. H.264/H.265 compatibility depends on profile, level, bit depth, decoder and configuration. WebRTC adds negotiation and media/security behavior of its own.

[GStreamer rtspsrc documentation](https://gstreamer.freedesktop.org/documentation/rtsp/rtspsrc.html), [RTP jitter buffer](https://gstreamer.freedesktop.org/documentation/rtpmanager/rtpjitterbuffer.html) and [WebRTC element](https://gstreamer.freedesktop.org/documentation/webrtc/), checked 2026-10-07.

## Measure the boundary

For glass-to-glass latency, measure a real optical event through the complete camera-to-display path and report resolution, frame rate, codec, exposure, encoder, radio mode, jitter settings, decoder/display and sample distribution. Packet interval, encode time, network RTT and frame age are different measurements. RTCP sender reports and RTP header extensions must be inspected rather than assumed present.

Use local media/replay first, then a controlled transport fixture; keep simulated results separate from on-air evidence. See [OpenHD](../components/openhd-implementation-guide.md) and [time provenance](time-and-coordinate-provenance.md).
