# SynchroQueen: Folder Synchronization Tool

A simple Python application that synchronizes files between a source and a replica folder, ensuring that any changes in the source are reflected in the replica. The tool supports interval-based synchronization and logs activities to a specified logfile.

## Features

- **File and Folder Synchronization**: Keeps the source and replica directories in sync by adding, updating, and deleting files as needed.
- **Flexible Interval Configuration**: Allows users to set a synchronization interval in seconds, minutes, hours, or days.
- **Logging**: Logs all operations to a specified file and the console for easy monitoring.
- **Fast Comparison**: Option to use metadata for quick comparisons.

## Requirements

- Python 3.9 or higher
- `hashlib` module (included in the Python standard library)
- `os` module (included in the Python standard library)
- `shutil` module (included in the Python standard library)

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/folder-synchronization-tool.git
cd folder-synchronization-tool
```

## Usage

Run the tool from the command line with the following syntax:

```bash
python main.py <source> <replica> <logfile> [-i <interval>] [-f]
```

### Arguments:

- `<source>`: Path to the source folder to be backed up.
- `<replica>`: Path to the destination folder that will hold the backup.
- `<logfile>`: Path to the log file where activities will be recorded.
- `-i`, `--interval`: (Optional) Check interval in the format `<number><unit>` where unit can be:
  - `s` for seconds
  - `m` for minutes
  - `h` for hours
  - `d` for days
- `-f`, `--fast`: (Optional) Enable fast comparison using file metadata instead of content hashing.

### Example

To synchronize the folder `~/Documents/Source` with `~/Documents/Backup` every 10 minutes and log to `sync.log`, run:

```bash
python main.py ~/Documents/Source ~/Documents/Backup sync.log -i 10m
```

## Logging

All operations are logged to the specified logfile. The log will include timestamps, the level of log messages (INFO), and a description of each operation performed.

## Error Handling

The application will raise exceptions if:

- The source or replica folders do not exist.
- The logfile path is invalid or inaccessible.
- The interval format is incorrect.

## Contributing

Contributions are welcome! If you have suggestions for improvements or features, please create an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Thanks to the Python community for their support and resources.
- Special thanks to the contributors and open-source libraries that made this project possible.

## Known bugs
- When app detects an empty folder (inside an empty folder) in replica and not in source, it removes only last empty folder, not the whole tree of empty folders. I am working on it!
