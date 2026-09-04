import pytest

from gamepulse.quality.current_players import (
    validate_app_id, 
    validate_player_count,
    validate_collected_at,
    validate_current_players_snapshot,
    validate_result,
)

def test_validate_app_id_accepts_positive_integer():
    assert validate_app_id(730) is True


@pytest.mark.parametrize(
    "invalid_app_id",
    [-10, 0, "730", True],
)
def test_validate_app_id_rejects_invalid_values(invalid_app_id):
    assert validate_app_id(invalid_app_id) is False  


@pytest.mark.parametrize(
    "valid_player_count",
    [751087, 0],
)
def test_validate_player_count_accepts_valid_values(valid_player_count):
    assert validate_player_count(valid_player_count) is True


@pytest.mark.parametrize(
    "invalid_player_count",
    [-1, "100", True],
)
def test_validate_player_count_rejects_invalid_values(invalid_player_count):
    assert validate_player_count(invalid_player_count) is False    



@pytest.mark.parametrize(
    "valid_collected_at",
    ["2026-09-02T15:07:56.478639+00:00", "2026-09-02T15:07:56+00:00"],
)
def test_validate_collected_at_accepts_valid_values(valid_collected_at):
    assert validate_collected_at(valid_collected_at) is True


@pytest.mark.parametrize(
    "invalid_collected_at",
    ["banana", "2026-99-99", 123],
)
def test_validate_collected_at_rejects_invalid_values(invalid_collected_at):
    assert validate_collected_at(invalid_collected_at) is False  






def test_validate_current_players_snapshot_rejects_missing_response():
    snapshot = {
        "app_id": 730,
        "collected_at": "2026-09-04T18:00:00+00:00",
        "payload": {},
    }

    assert validate_current_players_snapshot(snapshot) == ["invalid response"]   



@pytest.mark.parametrize(
    "valid_result",
    [1],
)
def test_validate_result_accepts_valid_values(valid_result):
    assert validate_result(valid_result) is True

@pytest.mark.parametrize(
    "invalidate_result",
    [-1, "1", True, 2, 0],
)
def test_validate_result_rejects_invalid_values(invalidate_result):
    assert validate_result(invalidate_result) is False   



def test_validate_current_players_snapshot_accepts_valid_snapshot():
    snapshot = {
        "app_id": 730,
        "collected_at": "2026-09-04T18:00:00+00:00",
        "payload": {
            "response": {
                "player_count": 500000,
                "result": 1,
            }
        },
    }

    assert validate_current_players_snapshot(snapshot) == []
    

@pytest.mark.parametrize(
    "invalid_result",
    [0, 2, "1", True, None],
)
def test_validate_current_players_snapshot_rejects_invalid_result(invalid_result):
    snapshot = {
        "app_id": 730,
        "collected_at": "2026-09-04T18:00:00+00:00",
        "payload": {
            "response": {
                "player_count": 500000,
                "result": invalid_result,
            }
        },
    }

    assert validate_current_players_snapshot(snapshot) == ["invalid result"]

