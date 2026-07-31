# Mesh Rider over the i.MX USB Port

> **Scope:** Getting a Doodle Labs Mesh Rider radio talking to an NXP
> i.MX8M Plus companion (Orqa DTK APB / Wingman APB and similar carriers)
> over the USB port. Cross-reference:
> [Mesh Radios](mesh-radios.md), [Adding a Companion Computer](companion.md),
> [Orqa Hardware Guide](../components/orqa-hardware-guide.md),
> [AI Wingman on the APB](wingman-apb.md).

---

## The one thing that trips everyone up

A Mesh Rider radio on USB is **not a serial device.** It does not show up
as `/dev/ttyUSB0`. Internally the radio is OpenWRT Linux, and its USB port
is wired to a Microchip/SMSC **LAN9500A** USB-to-Ethernet bridge. When you
plug it into the i.MX, the radio appears as a **network interface** — a new
`eth*` or `usb*` device — and you talk to it over IP.

So the mental model is: *the radio is a tiny router hanging off a USB
Ethernet dongle.* Everything below follows from that.

Two consequences people learn the hard way:

- You configure it with `ip addr` / SSH / a web browser, not with a
  serial terminal.
- The i.MX kernel needs the `smsc95xx` driver. If that driver isn't in the
  BSP, the radio enumerates on the USB bus but **no network interface ever
  appears**, and it looks like the radio is dead. It isn't.

---

## Addressing: why it's unreachable out of the box

The Mesh Rider ships with its **DHCP client disabled by default.** It will
not hand your i.MX an address, and it will not ask for one. It just sits
there on its own static IPs, waiting for you to join its subnet.

| Interface | Address | Notes |
|---|---|---|
| WAN2 (per-radio) | `10.223.x.y/16` | Unique per radio, derived from MAC, **printed on the radio label** (e.g. `10.223.164.62`). This is the normal management/data IP. |
| WAN3 (recovery) | `192.168.153.1/24` | **Same on every radio.** Fixed config/recovery address. Use this when you don't know the label IP or have locked yourself out. |

Because the radio never gives the host an address, **the i.MX must take a
static IP in one of those subnets** before anything responds to a ping.
This is the actual answer to "I plugged it in and nothing works."

---

## Bring-up on the i.MX, step by step

Run these on the i.MX (the companion is the USB *host*; the radio is the
USB *device*).

**1. Confirm the radio enumerated on the bus.**

```sh
lsusb            # look for a Microchip/SMSC LAN9500A or "Mesh Rider" device
dmesg | tail -20 # expect: smsc95xx ... registered 'smsc95xx' ... eth1: link up
```

If `lsusb` shows the device but `dmesg` shows **no `smsc95xx`** line and no
new interface, the driver is missing from the kernel — jump to
[Driver missing](#failure-driver) below.

**2. Find the interface name.**

```sh
ip -br link      # the new one is often eth1, or usb0 on some BSPs
```

**3. Give the i.MX an address in the radio's subnet and bring it up.**

```sh
ip link set eth1 up
ip addr add 10.223.1.1/16 dev eth1        # any free host in 10.223.0.0/16
# or, for the universal recovery path:
# ip addr add 192.168.153.2/24 dev eth1
```

**4. Reach the radio.**

```sh
ping 192.168.153.1                # always-on recovery IP
ping 10.223.164.62                # the IP from the radio's label
ssh root@192.168.153.1            # CLI (UCI / OpenWRT)
# or browse to https://192.168.153.1  (self-signed cert — expected)
```

If the ping answers, you're in. From here you configure the mesh (SSID,
encryption key, OGM interval, channel) exactly as in
[Mesh Radios → Network Configuration](mesh-radios.md). Nothing about that
changes because the link is USB instead of Ethernet.

---

## Make it survive a reboot

The manual `ip addr` above is gone on the next power cycle, and USB
interface names are not guaranteed to stay `eth1` (a second USB NIC, or
probe-order changes, can shuffle them). Pin both.

**Stable name via udev** — key off the LAN9500A driver / the radio's MAC
(read it once with `ip link show eth1`):

```
# /etc/udev/rules.d/70-meshrider.rules
SUBSYSTEM=="net", ACTION=="add", DRIVERS=="smsc95xx", NAME="meshrider"
```

**Static address via systemd-networkd:**

```ini
# /etc/systemd/network/20-meshrider.network
[Match]
Name=meshrider

[Network]
Address=10.223.1.1/16
# add a route to your mesh peer subnet here if it differs
```

```sh
systemctl enable --now systemd-networkd
```

On a read-only Yocto rootfs (the Orqa BSP is close to this), put these in
the BSP layer / overlay rather than expecting them to persist in `/etc`.

---

## Moving MAVLink (and video) across the link

Once the interface is up, the radio is just an IP hop. The data path is
the same one described in [Mesh Radios → MAVLink Over Mesh](mesh-radios.md):

```
FC ─(on-board bridge / UART)→ i.MX8M ─(UDP over USB-eth)→ Mesh Rider ─[mesh]→ GCS
```

On the APB the FC↔companion MAVLink bridge is already on-board (see
[wingman-apb.md](wingman-apb.md)), so the companion just forwards UDP out
to the radio's peer:

```sh
mavlink-routerd -e 10.223.255.255:14550 127.0.0.1:14540
# or
mavproxy.py --master=udp:127.0.0.1:14540 --out=udp:10.223.255.255:14550
```

The radio runs `batman-adv` (layer-2 mesh) underneath, so the host doesn't
route the mesh — it just sends IP to a peer and the radios handle delivery.

---

## Failure modes worth knowing before you're in the field

<a id="failure-driver"></a>
**Radio enumerates but no `eth*`/`usb*` appears.** The BSP kernel is missing
the USB-Ethernet driver. You need `CONFIG_USB_NET_SMSC95XX=y` (and its
parent `CONFIG_USB_USBNET`). On a stock desktop distro this is built in; on
a trimmed i.MX Yocto image it is frequently dropped. Rebuild the kernel or
ship the module in the BSP — there is no host-side workaround.

**Interface is up but nothing pings.** The host isn't in the radio's
subnet. The radio's DHCP client is off by default (see above), so a host
configured for DHCP gets *no* address and silently fails. Set a static IP
in `10.223.0.0/16` or use `192.168.153.2/24` to hit the universal recovery
address.

**Link drops, re-enumerates, or browns out under load.** The LAN9500A plus
the radio's own draw can exceed what an i.MX USB port will source —
especially the APB's compact rails. Power the radio from its **own supply**,
not the USB bus. A radio that re-enumerates every few seconds is almost
always a power problem, not a config problem. (Same lesson as
[Mesh Radios → Physical Installation](mesh-radios.md): never run a mesh
radio off the FC/host rail.)

**Throughput tops out around 90–95 Mbps no matter what the radio can do.**
The LAN9500A is a **USB 2.0, 10/100** PHY. The USB link is a 100 Mbit
bottleneck that sits *in front of* the radio's MIMO capacity. For telemetry
and one compressed video stream this is fine. If you need the radio's full
aggregate throughput (multiple HD streams, high-bandwidth payload), use the
radio's **native Gigabit Ethernet** port instead of USB. USB is a
configuration and light-data path, not a high-throughput one.

**Name churn breaks your scripts.** If a second USB NIC is present, the
radio may not stay `eth1`. Pin the name with the udev rule above before you
hardcode an interface anywhere.

---

## Quick reference

| Question | Answer |
|---|---|
| What does it show up as? | A USB-Ethernet interface (`smsc95xx`), not a serial port |
| Driver needed on i.MX | `CONFIG_USB_NET_SMSC95XX` / `smsc95xx` |
| Universal config IP | `192.168.153.1/24` (same on every radio) |
| Per-radio IP | `10.223.x.y/16`, on the label, derived from MAC |
| Host IP to set | Static in `10.223.0.0/16` (e.g. `10.223.1.1/16`) or `192.168.153.2/24` |
| Why it's dead out of the box | Radio DHCP client is off; host must take a static IP |
| Management | SSH `root@`, or `https://` (self-signed) |
| Throughput ceiling on USB | ~100 Mbit (USB 2.0 10/100 PHY) — use native Ethernet for more |
| Power | Off its own supply, never the USB bus / host rail |

---

*A Mesh Rider on USB is a router on a 100-Mbit dongle. Treat it like one:
give your host an address on its network, feed it real power, and reach for
the Ethernet port the moment you care about throughput.*
