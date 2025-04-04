# ipo_schedule.py

from datetime import datetime, timedelta

def get_upcoming_ipos():
    return [
        {
            "symbol": "NMAX",
            "datetime": datetime.now() + timedelta(seconds=15),  # replace with real IPO datetime
        },
        {
            "symbol": "KARM",
            "datetime": datetime.now() + timedelta(minutes=2),
        },
        # Add more as needed
    ]
