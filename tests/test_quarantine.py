import json
from datetime import datetime

from gamepulse.quality.quarantine import save_quarantined_snapshot


def test_save_quarantined_snapshot_creates_file(tmp_path):
    snapshot = {
        "app_id": 730,
        "collected_at": "2026-09-09T15:00:00+00:00",
        "payload": {
            "response": {
                "player_count": -50,
                "result": 0,
            }
        },
    }

    errors = ["invalid player_count", "invalid result"]

    output_path = save_quarantined_snapshot(
        snapshot,
        errors,
        base_dir=tmp_path,
    )

    assert output_path.exists()

    with output_path.open("r", encoding="utf-8") as file:
        saved_data = json.load(file)

    assert saved_data["errors"] == errors
    assert saved_data["snapshot"] == snapshot

    detected_at = datetime.fromisoformat(saved_data["detected_at"])

    assert detected_at.tzinfo is not None

    expected_dir = (
        tmp_path
        / "steam"
        / "current_players"
        / f"{detected_at.year:04d}"
        / f"{detected_at.month:02d}"
        / f"{detected_at.day:02d}"
    )

    assert output_path.parent == expected_dir

    assert output_path.name.startswith("app_730_")
    assert output_path.suffix == ".json"