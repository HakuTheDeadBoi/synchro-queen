import argparse
import os
import re

def get_args() -> argparse.Namespace:
    argparser = argparse.ArgumentParser()
    argparser.add_argument("source", type=str, help="Source folder you want to backup.")
    argparser.add_argument("replica",type=str, help="Destination folder you want to hold 'source' backup.")
    argparser.add_argument("logfile", type=str, help="Path to log file - created a new one if not exists.")
    argparser.add_argument("-i", "--interval", type=str, dest="interval", help="Check interval in format <number><unit> where unit is (s)econd|(m)inute|(h)our|(d)ay")
    argparser.add_argument("-f", "--fast", action="store_true", help="Fast comparison, using metadata.")

    return argparser.parse_args()

def validate_interval(interval: str) -> bool:
    return re.match(r"^\d+[smhd]{1}$", interval) is not None

def validate_folder(path: str) -> tuple[bool, str]:
    if not os.path.exists(path):
        return False, f"Folder {path} doesn't exist."
    if not os.path.isdir(path):
        return False, f"Folder {path} isn't a proper folder."
    if not os.access(path, os.R_OK | os.W_OK):
        return False, f"Can't access {path} folder."
    return True, ""

def validate_file(path: str) -> tuple[bool, str]:
    if not os.path.exists(path):
        return False, f"File {path} doesn't exist."
    if not os.path.isfile(path):
        return False, f"File {path} isn't a proper file."
    if not os.access(path, os.R_OK | os.W_OK):
        return False, f"Can't access {path} file."
    return True, ""

def validate_args(args: argparse.Namespace) -> tuple[bool, str]:
    is_everything_valid = True
    final_message = ""

    # invalid source is fatal
    is_source_valid, msg = validate_folder(args.source)
    is_everything_valid = is_everything_valid and is_source_valid
    final_message += msg

    # if replica is invalid, we can try to create one
    is_replica_valid, msg = validate_folder(args.replica)
    if not is_replica_valid:
        try:
            os.makedirs(args.replica)
            is_replica_valid, msg = validate_folder(args.replica)
        except IOError:
            pass
    is_everything_valid = is_everything_valid and is_replica_valid
    final_message += msg

    # logfile is the same case as replica
    is_logfile_valid, msg = validate_file(args.logfile)
    if not is_logfile_valid:
        try:
            open(args.logfile, "w").close()
            is_logfile_valid, msg = validate_file(args.logfile)
        except IOError:
            pass
    is_everything_valid = is_everything_valid and is_logfile_valid
    final_message += msg

    is_interval_valid = validate_interval(args.interval)
    is_everything_valid = is_everything_valid and is_interval_valid
    final_message += "" if is_interval_valid else "Interval has not a valid format."

    return is_everything_valid, final_message

def interval_arg_into_seconds(interval: str) -> int:
    time_unit_table = {
        "s": 1,
        "m": 60,
        "h": 60**2,
        "d": (60**2)*24
    }

    return int(interval[:-1]) * time_unit_table[interval[-1]]
