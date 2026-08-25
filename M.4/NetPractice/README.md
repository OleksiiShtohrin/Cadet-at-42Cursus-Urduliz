*This project has been created as part of the 42 curriculum by oshtohri.*

# NetPractice

## Description

NetPractice is a practical networking exercise from the 42 curriculum.

The goal is to learn the basics of computer networking by configuring small simulated networks. The exercises focus on IPv4 addressing, subnet masks, default gateways, routers, switches, routing tables, and communication between hosts and networks.

There are 10 training levels. Each level contains a non-functioning network diagram with some fields locked and others editable. The objective is to modify the editable fields until all required communication paths work correctly.

The networks used by NetPractice are simulated and are not real networks.

## What I Practiced

- IPv4 addressing
- Network and broadcast addresses
- Usable host ranges
- CIDR notation and subnet masks
- Subnet block sizes
- Default gateways
- Point-to-point `/30` networks
- Routers and routing tables
- Switches
- Static routes
- Default routes (`0.0.0.0/0`)
- Return paths
- Internet connectivity
- Route aggregation
- Reading network logs to diagnose configuration errors

## Instructions

### Start the training interface

Run:

```bash
./run.sh
```

If `run.sh` does not work, the project documentation also allows the interface to be started manually:

```bash
python3 -m http.server 49242
```

Then open:

```text
http://localhost:49242
```

The port can be changed if necessary.

### Enter the login

Enter your 42 login in the training interface so that the personal configuration is generated.

The evaluation tab can also generate random configurations suitable for evaluation.

### Complete the levels

For each level:

1. Read the objectives at the top of the page.
2. Identify the editable IP, mask, route, and gateway fields.
3. Calculate the required networks and addresses.
4. Configure the editable fields.
5. Click **Check again**.
6. Use the logs when the configuration is incorrect.
7. When the level is completed, export the configuration with **Get my config**.

### Export the configurations

The assignment requires 10 exported configuration files, one per level, at the repository root:

```text
level1.json
level2.json
level3.json
level4.json
level5.json
level6.json
level7.json
level8.json
level9.json
level10.json
```

## Networking Concepts

### IPv4 addressing

An IPv4 address identifies an interface on a network.

Example:

```text
192.168.50.34
```

### Subnet masks

A subnet mask determines which part of an IP address identifies the network and which part identifies the host.

Common examples:

```text
255.255.255.0   = /24
255.255.255.128 = /25
255.255.255.192 = /26
255.255.255.224 = /27
255.255.255.240 = /28
255.255.255.248 = /29
255.255.255.252 = /30
```

### Network and broadcast addresses

For a normal subnet, the first address is the network address and the last address is the broadcast address. Addresses between them are usable host/interface addresses.

Example:

```text
192.168.50.32/29

Network   = 192.168.50.32
Usable    = 192.168.50.33 - 192.168.50.38
Broadcast = 192.168.50.39
```

### `/30` point-to-point networks

A `/30` network contains four addresses:

```text
Network
Host
Host
Broadcast
```

Example:

```text
192.168.10.0/30

Network   = 192.168.10.0
Host      = 192.168.10.1
Host      = 192.168.10.2
Broadcast = 192.168.10.3
```

This is useful for a direct connection between two router interfaces.

### Default gateway

When a destination is outside the local network, a host sends the packet to its default gateway.

### Routers and routing tables

A router uses its routing table to decide where to forward a packet.

A default route is:

```text
0.0.0.0/0
```

It is used when no more specific route matches the destination.

### Switches

A switch connects devices on the same local network and allows connected hosts and router interfaces to communicate on that network.

### Return paths

Communication must work in both directions. A packet reaching its destination is not enough; the destination also needs a valid route back to the source.

## Troubleshooting

The NetPractice logs help identify configuration problems.

Useful messages include:

- destination does not match any interface
- route match
- no forward way
- no reverse way
- invalid gateway
- loop detected
- destination IP reached

Following the packet hop by hop makes it possible to identify where routing fails.

## Resources

### Official project documentation

- NetPractice subject / project PDF provided by the 42 curriculum.
- NetPractice training interface.

### Networking references

- TCP/IP addressing
- IPv4 addressing
- CIDR notation
- Subnet masks and subnetting
- Default gateways
- Routing tables
- Routers and switches
- OSI model and network layers
- RFC 791 — Internet Protocol
- RFC 1918 — Address Allocation for Private Internets


YouTube — What is Subnetting? — Practical Networking
https://www.youtube.com/watch?v=BWZ-MHIhqjM

YouTube — IPv4 Subnet Masks
https://www.youtube.com/watch?v=L3dsWxn5RBU

Cisco — IP Networking Basics
https://www.cisco.com/en/US/docs/security/vpn5000/manager/reference/guide/appA.html

Cisco — Configure IP Addresses and Unique Subnets
https://www.cisco.com/c/en/us/support/docs/ip/routing-information-protocol-rip/13788-3.html

Cloudflare — What is a subnet?
https://www.cloudflare.com/learning/network-layer/what-is-a-subnet/

Cloudflare — What is a router?
https://www.cloudflare.com/learning/network-layer/what-is-a-router/

Cloudflare — What is a network switch?
https://www.cloudflare.com/learning/network-layer/what-is-a-network-switch/

### AI usage

AI was used as a learning and reasoning assistant during the project.

It was used to:

- explain IPv4 addressing and subnet masks;
- explain CIDR notation and subnet calculations;
- practice calculating network, broadcast, and usable host addresses;
- explain `/28`, `/29`, `/30` and other prefixes;
- reason about gateways and routing tables;
- understand why particular network configurations worked or failed;
- help structure and document the project.


## Submission

The repository must contain:

- `README.md`;
- 10 exported configuration files, one for each level;
- all 10 configuration files at the repository root.

Before submission, verify that:

- the login was entered in the training interface;
- all 10 levels were successfully completed;
- all 10 configurations were exported;
- the exported files have the correct names;
- the files are present at the repository root.
