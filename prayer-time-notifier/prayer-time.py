#!/usr/bin/env python3

from datetime import datetime, timedelta
import subprocess
import os
import sys

# ========== CONFIGURATION ==========
PRAYER_TIMES = {
    "Fajr": "05:00",
    "Dhuhr": "13:45",
    "Asr": "16:30",
    "Maghrib": "18:05",
    "Isha": "19:30"
}

DEBUG = False

NOTIFY_FILE = "/tmp/prayer_time_notified"
ACTIVE_WINDOW = 1800  # 30 minutes
# ===================================


def get_prayer_icon(prayer_name):
    prayer_name = prayer_name.replace(" (tomorrow)", "")

    icons = {
        "Fajr": "🌙",
        "Dhuhr": "☀️",
        "Asr": "🌅",
        "Maghrib": "🌇",
        "Isha": "🌙",
    }

    return icons.get(prayer_name, "🕌")


def send_notification(prayer_name):
    try:
        subprocess.run([
            "notify-send",
            "-a", "Prayer Timer",
            "-i", os.path.expanduser("~/.local/share/icons/masjid.png"),
            "Prayer Time",
            f"It's time for {prayer_name}"
        ], check=False)

    except Exception:
        pass


def handle_notification(prayer_name):
    try:
        last_notified = None

        if os.path.exists(NOTIFY_FILE):
            with open(NOTIFY_FILE, "r") as f:
                last_notified = f.read().strip()

        if last_notified == prayer_name:
            return

        send_notification(prayer_name)

        with open(NOTIFY_FILE, "w") as f:
            f.write(prayer_name)

    except Exception:
        pass


def get_prayer_times(target_date):
    prayer_times = {}

    for prayer, time_str in PRAYER_TIMES.items():
        hour, minute = map(int, time_str.split(":"))

        prayer_times[prayer] = datetime(
            target_date.year,
            target_date.month,
            target_date.day,
            hour,
            minute
        )

    return prayer_times


def format_prayer_name(name):
    # Just return the clean name without icon for output
    return name.replace(" (tomorrow)", "")


def get_current_next_prayer(today_times):
    now = datetime.now()

    tomorrow = now.date() + timedelta(days=1)
    tomorrow_times = get_prayer_times(tomorrow)

    prayers = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]

    all_times = []

    for prayer in prayers:
        all_times.append((prayer, today_times[prayer]))

    all_times.append(("Fajr (tomorrow)", tomorrow_times["Fajr"]))

    all_times.sort(key=lambda x: x[1])

    current_prayer = None
    next_prayer = None

    for idx, (name, prayer_time) in enumerate(all_times):
        if now < prayer_time:
            next_prayer = (name, prayer_time)

            if idx > 0:
                current_prayer = all_times[idx - 1]

            break

    return current_prayer, next_prayer


def get_countdown(target_time):
    now = datetime.now()

    seconds = int((target_time - now).total_seconds())

    if seconds <= 0:
        return "00:00"

    total_minutes = (seconds + 59) // 60
    hours = total_minutes // 60
    minutes = total_minutes % 60

    return f"{hours:02d}:{minutes:02d}"


def main():
    try:
        now = datetime.now()

        today = now.date()
        prayer_times = get_prayer_times(today)

        # Check if any prayer is currently active
        for prayer, prayer_time in prayer_times.items():

            diff = (now - prayer_time).total_seconds()

            # Prayer active for 30 minutes after start
            if 0 <= diff < ACTIVE_WINDOW:

                # Notify only during the first minute
                if diff < 60:
                    handle_notification(prayer)

                # Output without icon
                print(f"{prayer} time")
                return

        # No active prayer -> clear old notification file
        try:
            if os.path.exists(NOTIFY_FILE):
                os.remove(NOTIFY_FILE)
        except Exception:
            pass

        # Show countdown to next prayer
        _, next_prayer = get_current_next_prayer(prayer_times)

        if not next_prayer:
            print("--:--")
            return

        prayer_name, prayer_time = next_prayer

        countdown = get_countdown(prayer_time)

        print(f"{format_prayer_name(prayer_name)}: {countdown}")

    except Exception as e:
        if DEBUG:
            print(f"Error: {e}", file=sys.stderr)

        print("--:--")


if __name__ == "__main__":
    main()
