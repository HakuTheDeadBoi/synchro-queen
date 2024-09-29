from datetime import datetime, timedelta
import logging
from time import sleep

from app.argparsing import get_args, validate_args, interval_arg_into_seconds
from app.compare import compare_folders
from app.filehandling import push_changes
from app.log import configure_logging

def main():
    args = get_args()
    are_args_valid, message = validate_args(args)

    if not are_args_valid:
        raise Exception(message)

    interval_in_seconds = interval_arg_into_seconds(args.interval)
    
    # logging setting
    configure_logging(args.logfile)
    
    # initial time snap
    delta = timedelta(seconds=interval_in_seconds)
    last_saved_time = datetime.now()

    # initial run
    logging.info("Initial synchronization started.")
    changes = compare_folders(args.source, args.replica, fast_comparison=args.fast)
    if not changes:
        logging.info("No changes found.")
    push_changes(changes, args.source, args.replica)

    while True:
        if (current_time := datetime.now()) > last_saved_time + delta:
            logging.info("Regular synchronization started.")
            last_saved_time = last_saved_time + delta
            changes = compare_folders(args.source, args.replica, fast_comparison=args.fast)
            if not changes:
                logging.info("No changes found.")
            push_changes(changes, args.source, args.replica)
        sleep(1)

if __name__ == '__main__':
    main()