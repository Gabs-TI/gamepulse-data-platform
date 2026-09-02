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