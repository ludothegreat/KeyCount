import json
import collections
import time
import subprocess
import os
import socket
from pynput import keyboard
from datetime import datetime

# Read configuration data from config.json
try:
    with open('config.json', 'r') as config_file:
        config_data = json.load(config_file)
except FileNotFoundError:
    print("Configuration file 'config.json' not found. Exiting.")
    exit(1)
except json.JSONDecodeError:
    print("Error decoding JSON in configuration file. Exiting.")
    exit(1)

# Get the hostname of the computer
hostname = socket.gethostname()

# Check if the hostname exists in the configuration
if hostname not in config_data["hosts"]:
    print(f"Unknown hostname {hostname}. Exiting.")
    exit(1)

# Retrieve settings based on hostname
path = config_data["hosts"][hostname]["path"]
working_dir = config_data["hosts"][hostname]["working_dir"]

# Change the working directory
os.chdir(working_dir)

# Initialize Git repository if needed
if not os.path.exists('.git'):
    print("Initializing Git repository...")
    subprocess.run(["git", "init"])

# Check if the remote is set to the GitHub repository
remote_check = subprocess.getoutput('git config --get remote.origin.url')
if remote_check != config_data["global_config"]["remote_check"]:
    print("Setting up remote to GitHub repository...")
    subprocess.run(["git", "remote", "add", "origin", config_data["global_config"]["remote_check"]])

# Create dictionaries to store single key counts and combination key counts
key_counts = collections.defaultdict(int)
combination_key_counts = collections.defaultdict(int)

# Define a variable to track the last save time
last_save_time = time.time()

# Define a function to save the key counts to a file and push to GitHub
def save_and_push_key_counts():
    global last_save_time  # Use the global variable

    # Check if the branch exists
    existing_branches = subprocess.getoutput('git branch --list')
    if hostname not in existing_branches:
        # Create and checkout new branch
        subprocess.run(["git", "checkout", "-b", hostname])
    else:
        # Checkout to the existing branch
        subprocess.run(["git", "checkout", hostname])

    # Save the current key counts to the file
    with open(path, "w") as file:
        json.dump({"SingleKeys": dict(key_counts), "CombinationKeys": dict(combination_key_counts)}, file)

    # Read commit_message template from config_data
    commit_message_template = config_data["global_config"]["commit_message"]

    # Replace placeholders with actual values
    formatted_commit_message = commit_message_template.format(
        HOSTNAME=hostname,
        TIME=datetime.now().strftime("%H:%M:%S"),
        DATE=datetime.now().strftime("%Y-%m-%d")
    )

    # Commit the changes using Git with the formatted commit message
    subprocess.run(["git", "add", path])
    subprocess.run(["git", "commit", "-m", formatted_commit_message])

    # Push the changes to GitHub
    subprocess.run(["git", "push", "origin", hostname])

    print("Key counts pushed to GitHub successfully.")

# Track currently pressed keys
pressed_keys = set()

# Create a listener for keyboard events
def on_key_press(key):
    global last_save_time, pressed_keys  # Use global variables

    try:
        key_str = key.char
    except AttributeError:
        key_str = str(key)

    # Check for combination keys
    if len(pressed_keys) > 0:
        combination = '+'.join(sorted(pressed_keys))
        combination_key_counts[combination] += 1

    key_counts[key_str] += 1
    pressed_keys.add(key_str)  # Add the pressed key to the set

    if time.time() - last_save_time >= 60:
        save_and_push_key_counts()
        last_save_time = time.time()  # Update the last save time

# Create a listener for key release events
def on_key_release(key):
    global pressed_keys  # Use the global variable

    try:
        key_str = key.char
    except AttributeError:
        key_str = str(key)

    if key_str in pressed_keys:
        pressed_keys.remove(key_str)  # Remove the released key from the set

# Start the keyboard listener
with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
    listener.join()
