# Event Risk Analyzer

A Python tool for parsing event logs and detecting suspicious user activity using rule-based risk scoring.

## Features

- Log parsing
- User activity aggregation
- Suspicious activity detection
- Risk score calculation
- Automated tests using pytest

## Example input

LOGIN user101 success
BET user101 50
WITHDRAW user102 5

## Run

python main.py sample_events.txt

## Output

User: user456
ALERT: MANY_LOGIN_FAILS
ALERT: WITHDRAW_GT_BET

Score: 80
Risk level: HIGH
