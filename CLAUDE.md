# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LeRobot is a PyTorch-based robotics library by Hugging Face for state-of-the-art machine learning in real-world robotics. It provides modular components for robot control, policy training, data collection, and simulation. Source code lives in `src/lerobot/`. Python >=3.10, Apache 2.0 license.

## Common Commands

### Install (development)
```bash
uv sync --extra dev --extra test          # minimal dev setup
uv sync --all-extras                      # everything including sim envs
pre-commit install                        # set up git hooks
```

### Lint & Format
```bash
pre-commit run --all-files                # ruff format + lint, typos, bandit, mypy, etc.
ruff format src/ tests/                   # format only
ruff check src/ tests/ --fix              # lint only
```

### Tests
```bash
python -m pytest tests/                   # full test suite
python -m pytest tests/test_file.py       # single test file
python -m pytest tests/test_file.py::test_name -sv  # single test, verbose
```
Tests require `git lfs pull` for artifacts in `tests/artifacts/`. Some tests require simulation extras (aloha, pusht, etc.).

### Type Checking
```bash
mypy --config-file=pyproject.toml src/lerobot/
```
mypy is enabled module-by-module (configs, envs, optim, model, cameras, transport are active; others still ignored).

### End-to-End Training/Eval Tests
```bash
make test-act-ete-train DEVICE=cpu        # train ACT policy on small dataset
make test-end-to-end DEVICE=cpu           # full E2E suite (ACT, Diffusion, TDMPC, SmolVLA)
```

### CLI Entry Points
All CLI commands are `lerobot-*` (defined in `pyproject.toml [project.scripts]`):
- `lerobot-train` / `lerobot-eval` — training and evaluation
- `lerobot-record` / `lerobot-replay` / `lerobot-teleoperate` — data collection
- `lerobot-calibrate` / `lerobot-setup-motors` / `lerobot-find-port` — hardware setup
- `lerobot-dataset-viz` / `lerobot-info` / `lerobot-edit-dataset` — dataset tools

## Architecture

### Configuration System
Uses **Draccus** (not hydra/omegaconf). Configs are Python dataclasses in `configs/`. CLI args map to nested dataclass fields with dot notation (e.g., `--policy.type=act --env.type=aloha`). `TrainPipelineConfig` in `configs/train.py` is the top-level training config. Policy configs live in each policy's `configuration_*.py` file and extend `PreTrainedConfig` from `configs/policies.py`.

### Factory Pattern
- `envs.make()` — creates gym environments from `EnvConfig`
- Policy creation goes through `PreTrainedConfig` which dynamically imports the right policy class based on `type`
- Factories use lazy imports to keep startup fast

### Key Module Responsibilities
- **policies/** — ML models (ACT, Diffusion, TDMPC, VQ-BeT, Pi0/Pi0.5, SmolVLA, GR00T, XVLA, etc.). Each has `configuration_*.py` (config dataclass) and `modeling_*.py` (nn.Module). Policies implement `select_action()` and `forward()`.
- **datasets/** — `LeRobotDataset` wraps Parquet metadata + video/image storage. Handles HuggingFace Hub push/pull.
- **robots/** — Hardware abstraction. `Robot` base class with `connect()`, `teleoperate()`, `capture_observation()`, `send_action()`.
- **cameras/** — Camera backends (OpenCV, Intel RealSense). Base class in `cameras/configs.py`.
- **motors/** — Motor bus abstraction (Dynamixel, Feetech) with `read()`/`write()` APIs.
- **teleoperators/** — Control interfaces (gamepad, keyboard, phone).
- **envs/** — Simulation wrappers for gym environments (Aloha, PushT, Libero, MetaWorld).
- **processor/** — Data transform pipelines for observations/actions.
- **scripts/** — CLI entry points. Each `lerobot_*.py` has a `main()` parsed by Draccus.
- **optim/** — Optimizer and LR scheduler configs/factories.

### Registries
`lerobot/__init__.py` maintains `available_policies`, `available_robots`, `available_cameras`, `available_motors`, and per-env mappings. Update these when adding new components.

### Adding New Components
- **New policy**: Add `configuration_*.py` + `modeling_*.py` in `policies/<name>/`, update `available_policies` in `__init__.py`, update `tests/test_available.py`
- **New robot**: Add config + class in `robots/<name>/`, update `available_robots`
- **New environment**: Update `available_tasks_per_env` and `available_datasets_per_env` in `__init__.py`

## Code Style

- **Ruff**: line length 110, Python 3.10 target. Rules: E, W, F, I, B, C4, T20, N, UP, SIM
- **isort** via ruff with `known-first-party = ["lerobot"]`
- **Google-style docstrings** (pydocstyle convention)
- Pre-commit hooks include: ruff format/lint, typos, bandit, pyupgrade (--py310-plus), gitleaks, mypy

## Optional Dependencies

Extras are grouped by hardware/feature in `pyproject.toml`. Common groups: `feetech`, `dynamixel` (motors), `aloha`, `pusht` (sim envs), `smolvla`, `groot`, `pi` (policies), `intelrealsense` (cameras), `gamepad`, `phone` (teleop). Note: `wallx` conflicts with `transformers-dep` and related extras due to pinned transformers version.
