# net-practice

[![Notion](https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=notion&logoColor=white)](https://watery-meadowlark-5e0.notion.site/netpractice-25c6e301af68800da876f484f04e2c7e)

Comprehensive networking notes and reference guide for 42's **NetPractice** project.

---

## Table of Contents

- [What is an IP Address?](#what-is-an-ip-address)
- [IP Address Classes](#ip-address-classes)
- [MAC Addresses](#mac-addresses)
- [Loopback](#loopback)
- [Broadcast Address](#broadcast-address)
- [Network Address](#network-address)
- [Multicast Addressing](#multicast-addressing)
- [Experimental Addresses](#experimental-addresses)
- [Default Network](#default-network)
- [Default Gateway](#default-gateway)
- [NAT (Network Address Translation)](#nat-network-address-translation)
- [Private Addresses (RFC 1918)](#private-addresses-rfc-1918)
- [IPv4](#ipv4)
- [IPv6](#ipv6)
- [Subnet Mask](#subnet-mask)
- [Reverse Subnet (Supernetting)](#reverse-subnet-supernetting)
- [VLSM (Variable Length Subnet Masking)](#vlsm-variable-length-subnet-masking)
- [FLSM (Fixed Length Subnet Masking)](#flsm-fixed-length-subnet-masking)
- [OSI 7-Layer Model](#osi-7-layer-model)
- [TCP/IP Protocol Suite](#tcpip-protocol-suite)

---

## What is an IP Address?

An IP (Internet Protocol) address is a unique numerical label assigned to each device connected to a computer network that uses the Internet Protocol for communication. IP addresses serve two primary functions:
1. **Identifying the host or network interface.**
2. **Providing the location of the host in the network.**

### Versions in Use:
* **IPv4 (Internet Protocol version 4):** Uses a 32-bit address scheme allowing for a total of $2^{32}$ addresses (~4.3 billion). Expressed in four octets separated by dots (e.g., `192.168.1.1`).
* **IPv6 (Internet Protocol version 6):** Uses a 128-bit address scheme, providing approximately $3.4 \times 10^{38}$ addresses ($2^{128}$). Represented as eight groups of four hexadecimal digits separated by colons (e.g., `2001:0db8:85a3:0000:0000:8a2e:0370:7334`).

### Categories:
* **Public IP addresses:** Assigned by ISPs and routable over the public internet.
* **Private IP addresses:** Used within a private local network and not directly routable on the internet.
* **Static IP addresses:** Manually assigned and constant over time.
* **Dynamic IP addresses:** Assigned temporarily via DHCP and may change over time.

---

## IP Address Classes

An IPv4 address consists of 4 octets separated by dots, where each octet is between `0` and `255` ($2^{32}$ total combinations).

Traditional classful networking divides the IPv4 space into classes:

| Class | First Octet Range | Format ($N$=Network, $H$=Host) | Default Subnet Mask | Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **Class A** | `1 - 126` | `N.H.H.H` | `255.0.0.0` (/8) | Large networks with many hosts |
| **Class B** | `128 - 191` | `N.N.H.H` | `255.255.0.0` (/16) | Medium-sized networks |
| **Class C** | `192 - 223` | `N.N.N.H` | `255.255.255.0` (/24) | Small networks |
| **Class D** | `224 - 239` | N/A | N/A | Multicast groups |
| **Class E** | `240 - 255` | N/A | N/A | Reserved for experimental use |

> **Note:** `127.x.x.x` is reserved for loopback testing and is not part of any standard class.

---

## MAC Addresses

A MAC (Media Access Control) address is a unique identifier assigned to network interface controllers (NICs) for communications on a physical network segment (Layer 2 / Data Link Layer), administered by the IEEE.

### Key Characteristics:
* **Uniqueness:** Each NIC has a globally unique hardware address assigned by the manufacturer.
* **Format:** Typically displayed as 6 pairs of hexadecimal digits separated by colons or hyphens (e.g., `00:1A:2B:3C:4D:5E`).

### Structure:
* **OUI (Organizationally Unique Identifier):** First 3 bytes (24 bits) identify the manufacturer/vendor.
* **Device Identifier:** Last 3 bytes (24 bits) represent a unique serial number assigned by the manufacturer.

### Functions:
* **Frame delivery:** Ensures Layer 2 frames reach the correct physical device on a local network segment.
* **ARP (Address Resolution Protocol):** Resolves IP addresses (Layer 3) to MAC addresses (Layer 2).
* **MAC Filtering:** Controls network access based on hardware addresses.

### Special Addresses:
* **Broadcast:** `FF:FF:FF:FF:FF:FF` (sends frames to all devices on the local segment).
* **Multicast:** First byte's least significant bit is set to `1`.
* **Locally Administered:** Second least significant bit of the first byte is set to `1`.

---

## Loopback

A loopback address routes network packets back to the same device internally without ever hitting physical network hardware.

* **IPv4:** `127.0.0.1` (entire `127.0.0.0/8` block is reserved).
* **IPv6:** `::1` (`::1/128`).
* **Hostname:** Typically mapped to `localhost`.

### Key Characteristics:
* **Self-communication:** Enables devices to send packets to themselves for testing and debugging.
* **Always Available:** Functional as long as the TCP/IP stack is operational.
* **Network Isolation:** Traffic never traverses physical network media.

---

## Broadcast Address

A broadcast address allows sending a single packet to **all** devices on a particular network segment simultaneously.

* **Format:** All host bits are set to `1` (binary).
* **Position:** The highest/last address in a subnet range.
* **Example:** In `192.168.1.0/24` (mask `255.255.255.0`), the broadcast address is `192.168.1.255`.
* **Usage:** Service discovery, network announcements, DHCP discover requests.

> **Note:** IPv6 does **not** use broadcast addresses; it uses multicast addressing instead.

---

## Network Address

The network address identifies a specific network segment/subnet rather than an individual host.

* **Format:** All host bits are set to `0` (binary).
* **Position:** The first address in a subnet range.
* **Calculation:** Bitwise `AND` between an IP address and its subnet mask.
* **Example:** IP `192.168.1.15` with mask `255.255.255.0` (`/24`) $\rightarrow$ Network address is `192.168.1.0`.
* **Usage:** Routing table lookups and packet forwarding.

---

## Multicast Addressing

Multicast delivers data from a single sender to a specific group of subscribed recipients simultaneously without duplicating packets across shared segments.

* **IPv4 Range:** Class D (`224.0.0.0` to `239.255.255.255`).
  * `224.0.0.1`: All hosts on the local network segment.
  * `224.0.0.2`: All routers on the local network segment.
  * `224.0.0.5`: All OSPF routers.
* **IPv6 Prefix:** `FF00::/8`.
* **Protocols:** IGMP (IPv4), MLD (IPv6), PIM (Protocol Independent Multicast).
* **Common Uses:** Video/audio streaming, video conferencing, financial market feeds, dynamic routing protocols.

---

## Experimental Addresses

Ranges reserved by IANA for research, testing, examples, and documentation (not routable on public internet):

* `192.0.2.0/24` (TEST-NET-1) — Documentation and examples.
* `198.51.100.0/24` (TEST-NET-2) — Documentation and examples.
* `203.0.113.0/24` (TEST-NET-3) — Documentation and examples.
* `240.0.0.0/4` (Class E) — Experimental / future use.

---

## Default Network

A default network (or default route) is a "catch-all" route used when the destination IP address does not match any specific entry in the routing table.

* **IPv4 Representation:** `0.0.0.0/0` (address `0.0.0.0`, mask `0.0.0.0`).
* **IPv6 Representation:** `::/0`.
* **Priority:** Lowest priority in routing tables (matches only after all more specific routes fail under longest prefix matching).

---

## Default Gateway

The default gateway is the IP address of the local router interface that connects a local subnet to external networks (such as other subnets or the internet).

### How it works:
1. When a host wants to send a packet, it checks whether the destination IP is on the local subnet (using its subnet mask).
2. **If Local:** Packet is sent directly to the host's MAC address via ARP.
3. **If Remote:** Packet is forwarded to the default gateway's MAC address to be routed.

---

## NAT (Network Address Translation)

NAT enables private IP subnets to communicate with external networks / internet by sharing one or a small pool of public IP addresses.

### NAT Types:
1. **Static NAT:** 1-to-1 mapping between a private IP and a public IP (used for hosting internal servers).
2. **Dynamic NAT:** Maps private IPs to a dynamic pool of public IPs on a first-come, first-served basis.
3. **PAT (Port Address Translation / NAT Overload):** Maps multiple private IP addresses to a single public IP using different source port numbers.

---

## Private Addresses (RFC 1918)

Private address ranges are reserved for internal networks and are not routed on the public internet.

### IPv4 Private Ranges:
| Range | CIDR | Total Addresses | Typical Use Case |
| :--- | :--- | :--- | :--- |
| `10.0.0.0` – `10.255.255.255` | `10.0.0.0/8` | 16,777,216 | Large enterprise networks |
| `172.16.0.0` – `172.31.255.255` | `172.16.0.0/12` | 1,048,576 | Medium to large networks |
| `192.168.0.0` – `192.168.255.255` | `192.168.0.0/16` | 65,536 | Home and small business networks |

### IPv6 Private Ranges:
* **ULA (Unique Local Addresses):** `fc00::/7` (equivalent to private IPv4).
* **Link-Local Addresses:** `fe80::/10` (valid only within the local physical segment).

---

## IPv4

* **Structure:** 32-bit address split into 4 octets (`0.0.0.0` to `255.255.255.255`).
* **Components:** Network ID + Host ID (determined by the subnet mask).
* **CIDR (Classless Inter-Domain Routing):** Replaced rigid classful networking with flexible bit prefixes (e.g., `/24`, `/27`).
* **Limitations:** Address space exhaustion (mitigated by NAT and transition to IPv6), lack of built-in security (requires IPsec).

---

## IPv6

* **Structure:** 128-bit address split into 8 groups of 4 hexadecimal digits (e.g., `2001:0db8:85a3:0000:0000:8a2e:0370:7334`).
* **Simplifications:**
  * Leading zeros can be omitted: `:0001:` $\rightarrow$ `:1:`.
  * Consecutive groups of zeros can be compressed once using `::` (e.g., `2001:db8::1`).
* **Address Types:** Unicast, Multicast, Anycast (no broadcast).
* **Key Advantages:**
  * Immense address space ($2^{128}$).
  * Simplified header and no packet fragmentation by intermediate routers.
  * Stateless Address Autoconfiguration (SLAAC).
  * Built-in IPsec support.
  * Eliminates the need for NAT.

---

## Subnet Mask

A 32-bit mask separating the Network portion (consecutive binary `1`s) from the Host portion (consecutive binary `0`s).

### Subnet Formulas:
* **Total IP Addresses:** $2^{\text{host bits}}$
* **Usable Host Addresses:** $2^{\text{host bits}} - 2$ (subtracting Network and Broadcast addresses)
* **Number of Subnets created:** $2^{\text{borrowed bits}}$

### Common Subnet Masks Reference:
| CIDR | Subnet Mask | Total IPs | Usable Hosts |
| :--- | :--- | :--- | :--- |
| `/30` | `255.255.255.252` | 4 | 2 (Point-to-point links) |
| `/29` | `255.255.255.248` | 8 | 6 |
| `/28` | `255.255.255.240` | 16 | 14 |
| `/27` | `255.255.255.224` | 32 | 30 |
| `/26` | `255.255.255.192` | 64 | 62 |
| `/25` | `255.255.255.128` | 128 | 126 |
| `/24` | `255.255.255.0` | 256 | 254 |
| `/16` | `255.255.0.0` | 65,536 | 65,534 |
| `/8` | `255.0.0.0` | 16,777,216 | 16,777,214 |

---

## Reverse Subnet (Supernetting)

Supernetting (route summarization/aggregation) combines multiple contiguous subnets into a single larger routing entry with a shorter prefix length.

* **Purpose:** Reduces routing table size, router memory overhead, and routing update frequency.
* **Example:**
  * Subnets: `192.168.16.0/24`, `192.168.17.0/24`, `192.168.18.0/24`, `192.168.19.0/24`
  * Shared Prefix: First 22 bits are identical.
  * Summary Supernet: `192.168.16.0/22` (covers `192.168.16.0` through `192.168.19.255`).

---

## VLSM (Variable Length Subnet Masking)

VLSM is a classless subnetting design method where subnets within the same address block can have **different** subnet masks based on specific host count requirements.

* **Advantages:** Maximizes address space efficiency, prevents address exhaustion, supports hierarchical routing.
* **Requirement:** Requires classless routing protocols that carry subnet mask info (e.g., OSPF, RIPv2, EIGRP, BGP).

---

## FLSM (Fixed Length Subnet Masking)

FLSM assigns the **same** subnet mask and block size to all subnets across the entire network.

* **Advantages:** Simple to design, configure, and troubleshoot.
* **Disadvantages:** Inefficient address utilization (small subnets waste addresses).

---

## OSI 7-Layer Model

| # | Layer | Primary Function | Common Protocols / Units |
| :--- | :--- | :--- | :--- |
| **7** | **Application** | Network services directly for end-user applications | HTTP, HTTPS, FTP, SMTP, DNS, SSH |
| **6** | **Presentation** | Data representation, formatting, encryption, compression | SSL/TLS, JPEG, ASCII, JSON |
| **5** | **Session** | Establishes, manages, and terminates application sessions | NetBIOS, RPC, Sockets |
| **4** | **Transport** | End-to-end communication, reliability, flow control, ports | TCP, UDP *(Segments / Datagrams)* |
| **3** | **Network** | Logical addressing, routing, path determination | IPv4, IPv6, ICMP, IPsec *(Packets)* |
| **2** | **Data Link** | Physical addressing, node-to-node framing, error detection | Ethernet, Wi-Fi, MAC, ARP, Switches *(Frames)* |
| **1** | **Physical** | Transmission of raw unstructured bitstream over physical media | Cables, Fiber, Hubs, Radio waves *(Bits)* |

---

## TCP/IP Protocol Suite

| TCP/IP Layer | Corresponding OSI Layers | Key Protocols |
| :--- | :--- | :--- |
| **4. Application** | Application, Presentation, Session (5–7) | HTTP, HTTPS, DNS, FTP, SMTP, SSH |
| **3. Transport** | Transport (4) | TCP, UDP |
| **2. Internet** | Network (3) | IP (IPv4/IPv6), ICMP, ARP, IGMP |
| **1. Network Interface** | Data Link, Physical (1–2) | Ethernet, Wi-Fi (802.11), PPP, Fiber |

---
