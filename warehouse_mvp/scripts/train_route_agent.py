from __future__ import annotations

import json
from pathlib import Path

from warehouse_mvp.rl_env_factory import build_route_env

BASE = Path(__file__).resolve().parents[1]
LAYOUT_PATH = BASE / "output" / "warehouse_layout_config.demo.generated.json"
WAREHOUSE_CSV = BASE / "data" / "sample_warehouse_export.csv"
OUT_DIR = BASE / "output" / "route_rl"

LOCATION_TO_ZONE = {
    "F1-A-01": "A",
    "F1-B-02": "B",
    "F1-B-05": "B",
    "F2-A-07": "A",
    "F3-F-02": "A",
}
PROCESSING_ZONE_BY_ITEM = {
    "SKU-005": "QC",
    "SKU-002": "QC",
}


def ensure_demo_layout() -> None:
    if LAYOUT_PATH.exists():
        return
    payload = {
        "warehouse_name": "Generated Task Demo Warehouse",
        "width": 8,
        "height": 6,
        "forklift_count": 2,
        "blocked_cells": [
            {"x": 3, "y": 1},
            {"x": 3, "y": 2},
            {"x": 3, "y": 3},
        ],
        "zone_cells": [
            {"x": 1, "y": 1, "zone": "A"},
            {"x": 1, "y": 3, "zone": "B"},
            {"x": 5, "y": 2, "zone": "QC"},
            {"x": 7, "y": 5, "zone": "OUT"},
        ],
        "start_cells": [{"x": 0, "y": 0}],
        "inbound_docks": [{"x": 0, "y": 5}],
        "outbound_docks": [{"x": 7, "y": 5}],
    }
    LAYOUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    LAYOUT_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> None:
    ensure_demo_layout()
    try:
        from stable_baselines3 import PPO
    except ImportError as exc:
        raise SystemExit(
            "stable-baselines3 is not installed. Install requirements-rl.txt first."
        ) from exc

    env = build_route_env(
        layout_path=str(LAYOUT_PATH),
        warehouse_csv_path=str(WAREHOUSE_CSV),
        location_to_zone=LOCATION_TO_ZONE,
        processing_zone_by_item=PROCESSING_ZONE_BY_ITEM,
        default_dropoff_zone="OUT",
        task_index=0,
        max_steps=100,
    )

    model = PPO("MultiInputPolicy", env, verbose=1, n_steps=64, batch_size=32)
    model.learn(total_timesteps=3000)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    model_path = OUT_DIR / "ppo_route_agent"
    model.save(str(model_path))

    obs, info = env.reset()
    total_reward = 0.0
    terminated = False
    truncated = False
    history = []
    while not (terminated or truncated):
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(int(action))
        total_reward += float(reward)
        history.append(
            {
                "action": int(action),
                "reward": float(reward),
                "terminated": terminated,
                "truncated": truncated,
                "info": info,
                "render": env.render(),
            }
        )

    summary = {
        "total_reward": total_reward,
        "steps": len(history),
        "terminated": terminated,
        "truncated": truncated,
        "final_info": info,
    }
    (OUT_DIR / "route_eval_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (OUT_DIR / "route_eval_trace.json").write_text(json.dumps(history, indent=2), encoding="utf-8")

    print(f"Saved model to: {model_path}")
    print(f"Saved eval summary to: {OUT_DIR / 'route_eval_summary.json'}")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
