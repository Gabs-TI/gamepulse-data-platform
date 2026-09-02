from datetime import datetime

def validate_app_id(app_id: int) -> bool:
    if type(app_id) is not int:
        return False

    if app_id <= 0:
        return False

    return True


def validate_player_count(player_count: int) -> bool:
    if type(player_count) is not int:
        return False

    if player_count < 0:
        return False

    return True


    from datetime import datetime


def validate_collected_at(collected_at: str) -> bool:
    if type(collected_at) is not str:
        return False

    try:
        datetime.fromisoformat(collected_at)
    except ValueError:
        return False

    return True


def validate_current_players_snapshot(snapshot: dict) -> list[str]:
    errors = []

    if not validate_app_id(snapshot["app_id"]):
        errors.append("invalid app_id")

#---------------------------------------------------------------
    collected_at = snapshot.get("collected_at")

    if not validate_collected_at(collected_at):
         errors.append("invalid collected_at")      

#------------------------------------------------
    payload = snapshot.get("payload")

    if not isinstance(payload, dict):
        errors.append("invalid payload")
    
        return errors    

    player_count = payload["response"]["player_count"]

    if not validate_player_count(player_count):
        errors.append("invalid player_count")    

    return errors