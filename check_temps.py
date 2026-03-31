#!/usr/bin/env python3
"""Check motor temperatures on both arms (auto-detects ports)."""

import glob
import scservo_sdk as scs

MOTORS = ["shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_roll", "gripper"]
VOLTAGE_ADDR = 62  # Present_Voltage, 1 byte, unit = 0.1V
TEMP_ADDR = 63     # Present_Temperature, 1 byte, unit = °C


def find_arms():
    """Scan serial ports and identify leader (~5V) vs follower (~12V) by motor voltage."""
    ports = sorted(glob.glob("/dev/ttyACM*") + glob.glob("/dev/ttyUSB*"))
    leader = None
    follower = None

    for port_path in ports:
        port = scs.PortHandler(port_path)
        if not port.openPort():
            continue
        port.setBaudRate(1000000)
        ph = scs.PacketHandler(0)

        data, comm, _ = ph.readTxRx(port, 1, VOLTAGE_ADDR, 1)
        port.closePort()

        if comm != 0:
            continue

        volts = data[0] / 10.0
        if volts > 8:
            follower = port_path
        else:
            leader = port_path

    return leader, follower


def check_temps(arms):
    for name, port_path in arms:
        port = scs.PortHandler(port_path)
        port.openPort()
        port.setBaudRate(1000000)
        ph = scs.PacketHandler(0)

        print(f"{name} ({port_path}):")
        for motor_id, motor in enumerate(MOTORS, 1):
            temp, comm, _ = ph.readTxRx(port, motor_id, TEMP_ADDR, 1)
            if comm == 0:
                warn = " ⚠️" if temp[0] >= 55 else ""
                print(f"  {motor:15s} {temp[0]}°C{warn}")
            else:
                print(f"  {motor:15s} READ ERROR")
        print()
        port.closePort()


if __name__ == "__main__":
    leader_port, follower_port = find_arms()

    if not leader_port or not follower_port:
        print("ERROR: Could not find both arms! Are they plugged in?")
        exit(1)

    print(f"Leader:   {leader_port}")
    print(f"Follower: {follower_port}\n")

    check_temps([("Leader", leader_port), ("Follower", follower_port)])
