import json
import subprocess


def ffprobe(filename: str) -> json:
    if not filename:
        raise Exception("please provide the filename first")

    cmd = ['ffprobe', '-loglevel', 'quiet', '-show_format', '-show_streams', '-of', 'json', filename]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise IOError('ffprobe', result.stderr)

    return json.loads(result.stdout)
