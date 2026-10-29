
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
import re

# Playlist file
playlist = Path("try.m3u")

if not playlist.exists():
    raise FileNotFoundError("try.m3u not found!")

# Read playlist
content = playlist.read_text(encoding="utf-8")

# Ensure M3U header exists
if not content.startswith("#EXTM3U"):
    raise ValueError("Invalid M3U playlist: #EXTM3U header missing")

# Set Bangladesh time
bd_time = datetime.now(
    ZoneInfo("Asia/Dhaka")
).strftime("%I:%M:%S %p (BD Time)")

# Count channels using EXTINF entries
channel_count = len(
    re.findall(r"(?m)^#EXTINF:", content)
)

# Update or add Playlist name
if re.search(r"(?m)^# Playlist name\s*:.*$", content):
    content = re.sub(
        r"(?m)^# Playlist name\s*:.*$",
        "# Playlist name : EITV",
        content,
        count=1
    )
else:
    content = content.replace(
        "#EXTM3U",
        "#EXTM3U\n# Playlist name : EITV",
        1
    )

# Update or add Last Updated time
if re.search(r"(?m)^# Last Updated\s*:.*$", content):
    content = re.sub(
        r"(?m)^# Last Updated\s*:.*$",
        f"# Last Updated: {bd_time}",
        content,
        count=1
    )
else:
    content = content.replace(
        "#EXTM3U",
        f"#EXTM3U\n# Last Updated: {bd_time}",
        1
    )

# Update or add channel count
if re.search(r"(?m)^# All channel\s*:.*$", content):
    content = re.sub(
        r"(?m)^# All channel\s*:.*$",
        f"# All channel : {channel_count}",
        content,
        count=1
    )
else:
    content = content.replace(
        "#EXTM3U",
        f"#EXTM3U\n# All channel : {channel_count}",
        1
    )

# Save updated playlist
playlist.write_text(content, encoding="utf-8")

print("Playlist name: EITV")
print(f"Last Updated: {bd_time}")
print(f"Total Channels: {channel_count}")
print("Playlist saved successfully!")
