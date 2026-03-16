import sys
import os

from analyzer.logic import (
    get_risk_level,
    calculate_risk_scores,
    parse_logs,
    detect_signals,
    aggregate_by_user
)


def test_parse_logs():
    logs = parse_logs("sample_events.txt")

    assert len(logs) > 0
    assert any(log["type"] == "LOGIN" for log in logs)
    assert any(log["user"] == "user101" for log in logs)

def test_detect_high_bet_no_withdraw():
    users = {
        "u1": {
            "events": 2,
            "total_bet": 200,
            "total_withdraw": 0,
            "login_success": 1,
            "login_fail": 0
        }
    }

    alerts = detect_signals(users)

    assert "HIGH_BET_NO_WITHDRAW" in alerts["u1"]

def test_calculate_risk_scores():
    alerts = {
        "u1": ["MANY_LOGIN_FAILS", "WITHDRAW_GT_BET"]
    }

    scores = calculate_risk_scores(alerts)

    assert scores["u1"] == 80

def test_risk_level():
    assert get_risk_level(80) == "HIGH"
    assert get_risk_level(30) == "MEDIUM"
    assert get_risk_level(10) == "LOW"

def test_parse_invalid_line():
    logs = parse_logs("sample_events.txt")

    for log in logs:
        assert log["type"] in {"LOGIN", "BET", "WITHDRAW"}

def test_multiple_signals():
    users = {
        "u1": {
            "events": 5,
            "total_bet": 500,
            "total_withdraw": 1000,
            "login_success": 0,
            "login_fail": 3
        }
    }

    alerts = detect_signals(users)

    assert "MANY_LOGIN_FAILS" in alerts["u1"]
    assert "WITHDRAW_GT_BET" in alerts["u1"]

def test_full_pipeline():
    logs = parse_logs("sample_events.txt")
    users = aggregate_by_user(logs)
    alerts = detect_signals(users)
    scores = calculate_risk_scores(alerts)

    assert isinstance(scores, dict)

def test_empty_logs():

    users = aggregate_by_user([])

    assert users == {}

def test_invalid_log_line():
    logs = [
        {"type": "INVALID", "user": "u1", "value": None, "status": None}
    ]
    users = aggregate_by_user(logs)

    assert "u1" in users

def test_max_risk_score():

    alerts = {
        "u1": [
            "HIGH_BET_NO_WITHDRAW",
            "MANY_LOGIN_FAILS",
            "WITHDRAW_GT_BET"
        ]
    }
    scores = calculate_risk_scores(alerts)

    assert scores["u1"] == 120

def test_no_risk():
        
    alerts = {}
    scores = calculate_risk_scores(alerts)

    assert scores == {}