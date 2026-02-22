# My SO-100 Teleop Commands

## Hardware Setup
- **Leader arm**: serial `5AE6085519`
- **Follower arm**: serial `5AE6057851`
- **Camera (Innomaker 1080p)**: `/dev/video2`
- **Laptop webcam**: `/dev/video0`

### Stable port paths (never swap between reboots!)
- **Leader**: `/dev/serial/by-id/usb-1a86_USB_Single_Serial_5AE6085519-if00`
- **Follower**: `/dev/serial/by-id/usb-1a86_USB_Single_Serial_5AE6057851-if00`

## 1. Find USB Ports
```bash
lerobot-find-port
```

## 2. Setup Motors (only needed once per arm)
```bash
lerobot-setup-motors --robot.type=so100_follower --robot.port=/dev/serial/by-id/usb-1a86_USB_Single_Serial_5AE6057851-if00
```
```bash
lerobot-setup-motors --teleop.type=so100_leader --teleop.port=/dev/serial/by-id/usb-1a86_USB_Single_Serial_5AE6085519-if00
```

## 3. Calibrate

**Leader arm:**
```bash
lerobot-calibrate --teleop.type=so100_leader --teleop.port=/dev/serial/by-id/usb-1a86_USB_Single_Serial_5AE6085519-if00 --teleop.id=my_leader
```

**Follower arm:**
```bash
lerobot-calibrate --robot.type=so100_follower --robot.port=/dev/serial/by-id/usb-1a86_USB_Single_Serial_5AE6057851-if00 --robot.id=my_follower
```

## 4. Teleoperate

**Basic (no camera):**
```bash
lerobot-teleoperate --robot.type=so100_follower --robot.port=/dev/serial/by-id/usb-1a86_USB_Single_Serial_5AE6057851-if00 --robot.id=my_follower --teleop.type=so100_leader --teleop.port=/dev/serial/by-id/usb-1a86_USB_Single_Serial_5AE6085519-if00 --teleop.id=my_leader
```

**With Innomaker camera (640x480):**
```bash
lerobot-teleoperate --robot.type=so100_follower --robot.port=/dev/serial/by-id/usb-1a86_USB_Single_Serial_5AE6057851-if00 --robot.id=my_follower --teleop.type=so100_leader --teleop.port=/dev/serial/by-id/usb-1a86_USB_Single_Serial_5AE6085519-if00 --teleop.id=my_leader --robot.cameras='{ front: {type: opencv, index_or_path: 2, width: 640, height: 480, fps: 30} }' --display_data=true
```

**With Innomaker camera (1080p):**
```bash
lerobot-teleoperate --robot.type=so100_follower --robot.port=/dev/serial/by-id/usb-1a86_USB_Single_Serial_5AE6057851-if00 --robot.id=my_follower --teleop.type=so100_leader --teleop.port=/dev/serial/by-id/usb-1a86_USB_Single_Serial_5AE6085519-if00 --teleop.id=my_leader --robot.cameras='{ front: {type: opencv, index_or_path: 2, width: 1920, height: 1080, fps: 30} }' --display_data=true
```

**With two cameras (front + top):**
```bash
lerobot-teleoperate --robot.type=so100_follower --robot.port=/dev/serial/by-id/usb-1a86_USB_Single_Serial_5AE6057851-if00 --robot.id=my_follower --teleop.type=so100_leader --teleop.port=/dev/serial/by-id/usb-1a86_USB_Single_Serial_5AE6085519-if00 --teleop.id=my_leader --robot.cameras='{ front: {type: opencv, index_or_path: 2, width: 640, height: 480, fps: 30}, top: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30} }' --display_data=true
```

## 5. Record Dataset

**Single camera:**
```bash
lerobot-record --robot.type=so100_follower --robot.port=/dev/serial/by-id/usb-1a86_USB_Single_Serial_5AE6057851-if00 --robot.id=my_follower --teleop.type=so100_leader --teleop.port=/dev/serial/by-id/usb-1a86_USB_Single_Serial_5AE6085519-if00 --teleop.id=my_leader --robot.cameras='{ front: {type: opencv, index_or_path: 2, width: 640, height: 480, fps: 30} }' --dataset.repo_id=YOUR_HF_USER/YOUR_DATASET_NAME --dataset.num_episodes=50
```

**Two cameras:**
```bash
lerobot-record --robot.type=so100_follower --robot.port=/dev/serial/by-id/usb-1a86_USB_Single_Serial_5AE6057851-if00 --robot.id=my_follower --teleop.type=so100_leader --teleop.port=/dev/serial/by-id/usb-1a86_USB_Single_Serial_5AE6085519-if00 --teleop.id=my_leader --robot.cameras='{ front: {type: opencv, index_or_path: 2, width: 640, height: 480, fps: 30}, top: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30} }' --dataset.repo_id=YOUR_HF_USER/YOUR_DATASET_NAME --dataset.num_episodes=50
```

## Notes
- Calibration files are stored in `~/.cache/huggingface/lerobot/calibration/`
- STS3215 firmware v3.10 requires Goal_Velocity to be non-zero (patched in local code)
- If teleop crashes with "no status packet", the retry fix is already applied locally
- **Ports can swap between reboots!** Always use `/dev/serial/by-id/` paths or the Jupyter notebook `teleop.ipynb` to auto-detect ports
