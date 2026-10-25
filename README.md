# Custom Minecraft Protocol Proxy & Testing Tool

A lightweight, custom-built Minecraft packet proxy designed to act as a middle-man server between the client and target servers. Built to analyze network traffic, inspect protocol handling, and perform security testing against server infrastructure.

> **Note:** This is an experimental project written using a "Just-In-Time learning" approach to explore low-level network programming, packet manipulation, and the Minecraft protocol.

---

## ⚡ Current Features

* **Custom Proxy Routing:** Intercepts traffic and allows client connections to external/cracked servers via proxy.
* **BungeeCord Support / Exploit Analysis:** Inspects and tests vulnerabilities related to IP-forwarding and BungeeCord authentication handling.
* **Protocol Crashers:** Implements various packet-based payload stress tests to evaluate server stability.
* **Proxy Checker:** Internal utility to validate and filter usable proxies for testing.
* **Bot Framework *(In Progress)*:** Modular architecture for simulating automated client connections and stress testing.
* **Port Scanner *(In Progress)*:** Built-in network utility to scan targets for open game server ports.

---

## 🛠️ Tech Stack & Concepts

* **Language:** Python
* **Networking:** Low-level TCP sockets & custom protocol parsing
* **Concepts:** Packet serialization/deserialization, zlib compression, thread management

---

## 📋 Roadmap & Planned Improvements (TODO)

- [ ] Complete bot simulation module 
- [ ] Implement full upstream/downstream proxy support (SOCKS5/HTTP)
- [ ] Expand and optimize crash payload modules (improved stress testing)
- [ ] Major refactor codebase for better modularity and performance
- [ ] Enhance packet logging and real-time inspection UI

---

## ⚠️ Disclaimer

This tool is created strictly for educational, research, and authorized security testing purposes. Do not use this software against servers without explicit permission from the owners.
