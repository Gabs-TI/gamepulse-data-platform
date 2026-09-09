import json
from datetime import datetime, timezone
from pathlib import Path
from gamepulse.quality.current_players import validate_current_players_snapshot
from gamepulse.quality.quarantine import save_quarantined_snapshot

import requests


STEAM_CURRENT_PLAYERS_URL = (
    "https://api.steampowered.com/"
    "ISteamUserStats/GetNumberOfCurrentPlayers/v1/"
)


def fetch_current_players(app_id: int) -> dict:
    response = requests.get(
        STEAM_CURRENT_PLAYERS_URL,
        params={"appid": app_id},
        timeout=10,
    )
    
    response.raise_for_status()

    return response.json()

def build_current_players_snapshot(app_id: int, payload: dict) -> dict:
    return {
        "source": "steam",
        "app_id": app_id,
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "payload": payload,
    }

def save_raw_snapshot(snapshot: dict) -> Path:
    collected_at = datetime.fromisoformat(snapshot["collected_at"])

    output_dir = (
        Path("data")
        / "raw"
        / "steam"
        / "current_players"
        / f"{collected_at.year:04d}"
        / f"{collected_at.month:02d}"
        / f"{collected_at.day:02d}"
    )

    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = collected_at.strftime("%Y%m%dT%H%M%SZ")
    file_name = f"app_{snapshot['app_id']}_{timestamp}.json"

    output_path = output_dir / file_name

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(snapshot, file, ensure_ascii=False, indent=2)

    return output_path

if __name__ == "__main__":
    app_id = 730

    payload = fetch_current_players(app_id)
    snapshot = build_current_players_snapshot(app_id, payload)
    output_path = save_raw_snapshot(snapshot)

    print(f"Raw snapshot saved to: {output_path}")

    errors = validate_current_players_snapshot(snapshot)

    if errors:
        quarantine_path = save_quarantined_snapshot(snapshot, errors)

        print(f"Data quality failed: {errors}")
        print(f"Snapshot quarantined at: {quarantine_path}")
    else:
        print("Data quality validation passed.")