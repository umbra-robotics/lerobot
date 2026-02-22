#!/usr/bin/env python3
"""Identify leader vs follower arm by reading motor voltage.

The leader arm runs on ~5V (USB power), the follower on ~12V (external PSU).
Reads Present_Voltage (address 62) from motor 1 on each port.
"""

import scservo_sdk as scs

PORTS = ["/dev/ttyACM0", "/dev/ttyACM1"]
VOLTAGE_ADDR = 62  # Present_Voltage, 1 byte, unit = 0.1V

for port_path in PORTS:
    port = scs.PortHandler(port_path)
    if not port.openPort():
        print(f"{port_path}: CANNOT OPEN")
        continue
    port.setBaudRate(1000000)
    ph = scs.PacketHandler(0)

    data, comm, _ = ph.readTxRx(port, 1, VOLTAGE_ADDR, 1)
    port.closePort()

    if comm != 0:
        print(f"{port_path}: READ ERROR (comm={comm})")
        continue

    volts = data[0] / 10.0
    if volts > 8:
        label = "FOLLOWER (~12V)"
    else:
        label = "LEADER  (~5V)"

    print(f"{port_path}: {volts:.1f}V  -->  {label}")
