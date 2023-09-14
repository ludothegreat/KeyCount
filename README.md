# KeyCount Project

## Description

This Python script listens to keystrokes and saves the counts to a JSON file, which is then pushed to a GitHub repository.

## Installation

1. Clone this repository: `git clone https://github.com/username/KeyCount.git`
2. Navigate to the cloned directory: `cd KeyCount`
3. Install required packages: `pip install -r requirements.txt`

## Configuration

Create a `config.json` file in the root directory with the following structure:

```json
{
    "global_config": {
        "remote_check": "https://github.com/username/KeyCount.git",
        "commit_message": "auto_update-{HOSTNAME}-{TIME}-{DATE}"
    },
    "hosts": {
        "HostName1": {
            "path": "/path/to/hostname1/key_counts.json",
            "working_dir": "/path/to/hostname1/working_directory"
        },
        "HostName2": {
            "path": "/path/to/hostname2/key_counts.json",
            "working_dir": "/path/to/hostname2/working_directory"
        }
    }
}
```

Replace the values with the corresponding information for each host machine.

## Usage

Run the `keycount.py` script to start listening to keystrokes.

```bash
python keycount.py
```

The script will create or update a JSON file with the counts of single and combination keystrokes, and push the changes to GitHub.

## License

MIT License
