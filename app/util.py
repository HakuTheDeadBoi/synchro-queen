import re

def validate_interval(interval: str) -> bool:
    return re.match("^\d+[smhd]{1}$", interval) is not None