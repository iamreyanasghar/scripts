# ZSH History Cleaner

A Python utility to interactively search and delete specific commands from your ZSH history file.

## Features

- **Interactive CLI** - Enter queries to find and remove matching commands
- **Case-insensitive search** - Finds commands regardless of case
- **Safe operation** - Preserves unreadable lines to prevent data loss
- **Auto-refresh** - Automatically reloads ZSH history after deletion (`fc -R`)
- **Multiple encoding support** - Handles various history file encodings (UTF-8, Latin-1, CP1252, etc.)
- **Exit commands** - Type `/exit`, `/quit`, `/q`, `exit`, or `quit` to exit (or press `Ctrl+D`)

## Requirements

- Python 3.6+
- ZSH shell

## Installation

```bash
# Clone or download the script
git clone https://github.com/iamreyanasghar/scripts/zsh-history-filter
cd zsh-history-filter

# Make executable (optional)
chmod +x zsh_history_filter.py

# Or run directly
python3 zsh_history_filter.py

# Or install globally (optional)
sudo cp zsh_history_filter.py /usr/local/bin/zsh-history-cleaner
sudo chmod +x /usr/local/bin/zsh-history-cleaner
```

## Usage

```bash
# Run the interactive cleaner
python3 zsh_history_filter.py
```

### Interactive Session

```
============================================================
🔍 ZSH History Cleaner
============================================================
Enter queries to delete matching commands from zsh history
Type '/exit' or press Ctrl+D (^D) to exit
------------------------------------------------------------

🔎 Enter query to delete: git push
✅ Successfully removed 3 command(s) containing 'git push'
🔄 History refreshed

🔎 Enter query to delete: rm -rf
✅ Successfully removed 1 command(s) containing 'rm -rf'
🔄 History refreshed

🔎 Enter query to delete: /exit

👋 Exiting...

📊 Total operations performed: 2
✨ Done!
```

## How It Works

1. **Locates history file** - Uses `$HISTFILE` environment variable or defaults to `~/.zsh_history`
2. **Reads with encoding detection** - Tries multiple encodings to handle various history file formats
3. **Parses ZSH history format** - Handles the `: timestamp:0;command` format
4. **Filters matching commands** - Removes lines where the command portion contains your query (case-insensitive)
5. **Writes back safely** - Preserves unreadable lines, writes filtered history as UTF-8
6. **Refreshes ZSH history** - Runs `fc -R` to reload history in current session


## Safety Notes

- **Backup recommended** - Consider backing up `~/.zsh_history` before first use
- **Unreadable lines preserved** - Lines that can't be parsed are kept intact
- **No regex** - Queries are simple substring matches (not regular expressions)
- **Case-insensitive** - `git` matches `Git`, `GIT`, `gIt`, etc.

## Exit Commands

| Command | Description |
|---------|-------------|
| `/exit` | Exit the program |
| `/quit` | Exit the program |
| `/q` | Exit the program |
| `exit` | Exit the program |
| `quit` | Exit the program |
| `Ctrl+D` | Exit the program (EOF) |
| `Ctrl+C` | Cancel current operation |

## Conclusion

The ZSH History Cleaner provides a simple, safe, and interactive way to maintain a clean command history. Whether you're removing sensitive commands, cleaning up typos, or just decluttering your history, this tool makes it easy without risking data loss. The automatic encoding detection and history refresh ensure a smooth experience across different ZSH configurations.