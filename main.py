import sys

from analyzer.logic import (
    parse_logs,
    aggregate_by_user,
    print_user_stats,
    detect_signals,
    calculate_risk_scores,
    get_risk_level
)

def main():

    if len(sys.argv) < 2:
        print("Usage: python main.py <logfile>")
        sys.exit(1)
    
    filepath = sys.argv[1]

    logs = parse_logs(filepath)
    users = aggregate_by_user(logs)

    print_user_stats(users)

    alerts = detect_signals(users)

    for user, flags in alerts.items():
        print(f"User: {user}")
        for flag in flags:
            print(f"  ALERT: {flag}")
        print()

    scores = calculate_risk_scores(alerts)

    for user, score in scores.items():
        level = get_risk_level(score)

        print(f"User: {user}")
        print(f"Score: {score}")
        print(f"Risk level: {level}")
        print()
    total_users = len(users)
    total_alerts = sum(len(v) for v in alerts.values())
    high_risk_users = sum(1 for s in scores.values() if s >= 50)

    print("SUMMARY")
    print(f"Users analyzed: {total_users}")
    print(f"Alerts detected: {total_alerts}")
    print(f"High risk users: {high_risk_users}")
        
if __name__ == "__main__":
    main()