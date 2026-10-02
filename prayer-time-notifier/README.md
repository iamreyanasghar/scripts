# Prayer Time Notifier

🕌 A lightweight Python script that sends desktop notifications for the five daily prayers and displays a live countdown to the next prayer. Designed to work as a **Generic Monitor** in the XFCE panel.

---

## Features

- 🔔 Desktop notifications at prayer times (Fajr, Dhuhr, Asr, Maghrib, Isha)
- ⏳ Live countdown to the next prayer
- 🖥️ Works as an XFCE **Generic Monitor** panel item
- 🪶 No dependencies beyond Python 3 and `notify-send`
- 🔕 Notifies only once per prayer (no spam)
- 🌙 Handles tomorrow's Fajr correctly after Isha

---

## Requirements

- **Python 3.6+**
- **`notify-send`** (from `libnotify`)

Install `notify-send` if you don't have it:

```bash
# Debian / Ubuntu / Linux Mint
sudo apt install libnotify-bin

# Arch
sudo pacman -S libnotify

# Fedora
sudo dnf install libnotify
```

Optional: a custom masjid icon at `~/.local/share/icons/masjid.png` (used as the notification icon).

---

## Installation

```bash
git clone https://github.com/iamreyanasghar/scripts.git
cd scripts/prayer-time-notifier
chmod +x prayer-time.py
```

---

## Configuration

Open `prayer-time.py` and edit the `PRAYER_TIMES` dictionary at the top:

```python
PRAYER_TIMES = {
    "Fajr": "05:00",
    "Dhuhr": "13:45",
    "Asr": "16:30",
    "Maghrib": "18:05",
    "Isha": "19:30"
}
```

Set each prayer time in **24-hour `HH:MM`** format for your local area.

Other options:

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Print error messages to stderr | `False` |
| `NOTIFY_FILE` | Temp file used to avoid duplicate notifications | `/tmp/prayer_time_notified` |
| `ACTIVE_WINDOW` | Seconds after a prayer starts where it's considered "active" | `1800` (30 min) |

---

## Usage

### 1. Run manually

```bash
./prayer-time.py
```

Output:

- `Fajr time` — when a prayer is currently active (first 30 min)
- `Dhuhr: 02:15` — countdown to the next prayer (HH:MM)
- `--:--` — fallback on error

## Using as an XFCE Generic Monitor

The script is designed to run as an XFCE **Generic Monitor** panel plugin — it prints a single line each run, which XFCE displays in your panel.

### Steps

1. **Right-click your XFCE panel** → **Panel** → **Add New Items…**
2. Select **Generic Monitor** → **Add** → **Close**
3. Right-click the new item → **Properties**
4. Configure:

   | Setting | Value |
   |---------|-------|
   | **Command** | `/home/reyan/scripts/prayer-time-notifier/prayer-time.py` |
   | **Update period (s)** | `10` (or `30`, `60`) |
   | **Label** | Leave empty (script prints its own text) |

5. Go to the **Advanced** tab and make sure:
   - ✅ **Use standard input** is **unchecked**
   - ✅ **Use standard error** is **unchecked**

6. Click **Close**. Your panel will now show the countdown, e.g. `Asr: 01:42`, and automatically switch to `Asr time` when the prayer starts.

### Optional: add an icon

In the Generic Monitor properties, you can prefix the command with an icon path or use the **Icon** tab to set a masjid icon. Or leave it text-only — simpler.

---

## How It Works

- Every run, the script computes the current and next prayer times for today (and tomorrow's Fajr).
- If **now** is within `ACTIVE_WINDOW` seconds **after** a prayer start:
  - It prints `<Prayer> time`
  - On the **first minute only**, it fires a `notify-send` notification
  - A temp file (`/tmp/prayer_time_notified`) tracks the last notified prayer to prevent duplicates
- Otherwise, it prints `NextPrayer: HH:MM` — a countdown to the next prayer.
- After Isha, it correctly rolls over to **Fajr (tomorrow)**.

## Author

**Reyan Asghar** — [github.com/iamreyanasghar](https://github.com/iamreyanasghar)

