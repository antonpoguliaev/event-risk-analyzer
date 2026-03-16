VALID_EVENT_TYPE = {'LOGIN', 'BET', 'WITHDRAW'}

SIGNAL_SCORES = {
    "HIGH_BET_NO_WITHDRAW": 40,
    "MANY_LOGIN_FAILS": 30,
    "WITHDRAW_GT_BET": 50
}

def parse_logs(filepath):
    """Parse raw event logs into structured dictionaries."""
    with open(filepath) as f:
        lines = f.readlines()
    logs = []
# === PARSE LOGS ===
    for line in lines:
        line = line.strip()
        parts = line.split()
        if len(parts) < 2:
            continue
        log = {}
        event_type = parts[0]
        if event_type not in VALID_EVENT_TYPE:
            continue
        if event_type =='LOGIN' and len(parts)>=3:
            status = parts[2]
            value=None
        elif event_type in {'BET','WITHDRAW'} and len(parts)>=3 :
            try:
                value = float(parts[2])
            except ValueError:
                continue
            status=None
        else:
            continue
        user_id=parts[1]
        log['type'] = event_type
        log['user'] = user_id
        log['value'] = value
        log['status'] = status
        logs.append(log)
    return logs

# === ANALYTICS ===
def aggregate_by_user(logs):
    """Aggregate user statistics: bets, withdrawals, login success/fail."""
    users = {}
    for log in logs:
        user=log['user']
        if user not in users:
            users[user] = {
                'events': 0,
                'total_bet': 0.0,
                'total_withdraw': 0.0,
                'login_success': 0,
                'login_fail': 0
            }
        users[user]['events'] += 1
        if log['type'] == 'BET':
            users[user]['total_bet'] += log['value']
        elif log['type'] == 'WITHDRAW':
            users[user]['total_withdraw'] += log['value']
        if log['type'] == 'LOGIN':    
            if log['status'] == 'fail':
                users[user]['login_fail'] += 1
            elif log['status'] =='success':
                users[user]['login_success'] += 1
    return users

def print_user_stats(users):
    """Print aggregated user statistics."""
    for user, data in users.items():
        net=data['total_bet'] - data['total_withdraw']
        total_logins=data['login_success'] + data['login_fail']
        if total_logins > 0:
            success_rate=data['login_success'] / total_logins
        else:
            success_rate=0
        print(f"User: {user}")
        print(f"  Events: {data['events']}")
        print(f"  Total bet: {data['total_bet']}")
        print(f"  Total withdraw: {data['total_withdraw']}")
        print(f"  Net: {net}")
        print(f"  Login success rate: {success_rate:.2%}")
        print()



def detect_signals(users):
    """Detect suspicious patterns based on predefined rules."""
    alerts = {}

    for user, data in users.items():
        user_alerts = []

        # SIGNAL 1
        if data['total_bet'] >= 100 and data['total_withdraw'] == 0:
            user_alerts.append('HIGH_BET_NO_WITHDRAW')

        # SIGNAL 2
        if data['login_fail'] >= 3:
            user_alerts.append('MANY_LOGIN_FAILS')

        # SIGNAL 3
        if data['total_bet'] > 0 and data['total_withdraw'] > data['total_bet'] * 1.2:
            user_alerts.append('WITHDRAW_GT_BET')

        if user_alerts:
            alerts[user] = user_alerts
    return alerts

def calculate_risk_scores(alerts):
    """Calculate total risk score for each user based on triggered signals.""" 
    scores = {}
    for user, flags in alerts.items():
        score = 0
        for flag in flags:
            score += SIGNAL_SCORES.get(flag, 0)
        scores[user] = score
    return scores
def get_risk_level(score):
    """Convert numeric score into LOW / MEDIUM / HIGH risk level."""
    if score >= 50:
        return "HIGH"

    elif score >= 20:
        return "MEDIUM"

    else:
        return "LOW"