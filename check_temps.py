#!/usr/bin/env python3
"""Check motor temperatures on both arms."""

import scservo_sdk as scs

MOTORS = ["shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_roll", "gripper"]
ARMS = [("Leader", "/dev/ttyACM0"), ("Follower", "/dev/ttyACM1")]

for name, port_path in ARMS:
    port = scs.PortHandler(port_path)
    port.openPort()
    port.setBaudRate(1000000)
    ph = scs.PacketHandler(0)

    print(f"{name} ({port_path}):")
    for motor_id, motor in enumerate(MOTORS, 1):
        temp, comm, _ = ph.readTxRx(port, motor_id, 63, 1)
        if comm == 0:
            warn = " ⚠️" if temp[0] >= 55 else ""
            print(f"  {motor:15s} {temp[0]}°C{warn}")
        else:
            print(f"  {motor:15s} READ ERROR")
    print()
    port.closePort()
