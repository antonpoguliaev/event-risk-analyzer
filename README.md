# Event Risk Analyzer

Event Risk Analyzer is a small Python tool that parses event logs and detects suspicious user activity using simple rule-based signals and risk scoring.

## Features

- Parse event logs from a text file
- Aggregate user activity statistics
- Detect suspicious behavior using rule-based signals
- Calculate risk scores for users
- Simple command-line interface
- Automated tests with pytest

## Example Log Input

LOGIN user101 success
BET user101 50
WITHDRAW user102 5
LOGIN user456 fail
LOGIN user456 fail
LOGIN user456 fail
BET user456 500
WITHDRAW user456 1000

## Run the Program

python main.py sample_events.txt

## Example Output

User: user456
ALERT: MANY_LOGIN_FAILS
ALERT: WITHDRAW_GT_BET

Score: 80
Risk level: HIGH

SUMMARY
Users analyzed: 5
Alerts detected: 3
High risk users: 1

## Project Structure

event-risk-analyzer
├── analyzer
│   ├── __init__.py
│   └── logic.py
├── tests
│   └── test_analyzer.py
├── main.py
├── sample_events.txt
├── events.txt
└── README.md

## Run Tests

python -m pytest

## Purpose

This project was created as a learning project to practice Python, log analysis, rule-based detection systems, and automated testing.
