"""
Flask backend for the Warehouse Layout Editor.

Run:
    cd warehouse_mvp/layout_editor && python app.py
    # or from repo root:
    python -m warehouse_mvp.layout_editor.app

Opens at http://localhost:5050
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from flask import Flask, jsonify, render_template, request

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR.parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Optional: server-side validation via layout_loader
# ---------------------------------------------------------------------------
try:
    sys.path.insert(0, str(BASE_DIR.parent / "src"))
    from warehouse_mvp.layout_loader import (
        LayoutValidationError,
        warehouse_config_from_dict,
    )
    HAS_VALIDATOR = True
except ImportError:
    HAS_VALIDATOR = False

# ---------------------------------------------------------------------------
# Flask app
# ---------------------------------------------------------------------------
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("editor.html")


@app.route("/api/layouts", methods=["GET"])
def list_layouts():
    """Return list of layout JSON files in output/."""
    layouts = []
    for f in sorted(OUTPUT_DIR.glob("*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            layouts.append({
                "filename": f.name,
                "name": data.get("warehouse_name", f.stem),
                "width": data.get("width", 0),
                "height": data.get("height", 0),
            })
        except (json.JSONDecodeError, KeyError):
            continue
    return jsonify(layouts)


@app.route("/api/layouts/<filename>", methods=["GET"])
def get_layout(filename: str):
    """Return a specific layout JSON."""
    path = OUTPUT_DIR / filename
    if not path.exists() or not path.suffix == ".json":
        return jsonify({"error": "Not found"}), 404
    data = json.loads(path.read_text(encoding="utf-8"))
    return jsonify(data)


@app.route("/api/layouts", methods=["POST"])
def save_layout():
    """Save a layout JSON. Body: {filename: str, data: {...}}."""
    body = request.get_json(force=True)
    filename = body.get("filename", "warehouse_layout_config.json")
    data = body.get("data", {})

    if not filename.endswith(".json"):
        filename += ".json"

    # Server-side validation
    if HAS_VALIDATOR:
        try:
            warehouse_config_from_dict(data)
        except LayoutValidationError as exc:
            return jsonify({"error": str(exc)}), 400
        except Exception as exc:
            return jsonify({"error": f"Validation error: {exc}"}), 400

    path = OUTPUT_DIR / filename
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return jsonify({"ok": True, "path": str(path)})


if __name__ == "__main__":
    import webbrowser, threading
    url = "http://localhost:5050"
    threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    print(f"\n  Warehouse Layout Editor → {url}\n")
    app.run(debug=False, port=5050, host="127.0.0.1")
