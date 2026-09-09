import json
from datetime import datetime, timezone
from pathlib import Path

def save_quarantined_snapshot(snapshot: dict, errors: list[str]) -> Path:
    detected_at = datetime.now(timezone.utc)

    output_dir = (
        Path("data")
        / "quarantine"
        / "steam"
        / "current_players"
        / f"{detected_at.year:04d}"
        / f"{detected_at.month:02d}"
        / f"{detected_at.day:02d}"
    )

    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = detected_at.strftime("%Y%m%dT%H%M%SZ")

    app_id = snapshot.get("app_id")
    app_id_label = str(app_id) if app_id is not None else "unknown"

    file_name = f"app_{app_id_label}_{timestamp}.json"
    output_path = output_dir / file_name

    quarantine_record = {
        "detected_at": detected_at.isoformat(),
        "errors": errors,
        "snapshot": snapshot,
    }

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(quarantine_record, file, ensure_ascii=False, indent=2)

    return output_path