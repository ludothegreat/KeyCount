import collections
import json
import time
import subprocess
from pynput import keyboard

# Create dictionaries to store single key counts and combination key counts
key_counts = collections.defaultdict(int)
combination_key_counts = collections.defaultdict(int)

# Define a variable to track the last save time
last_save_time = time.time()

# Define a function to save the key counts to a file and push to GitHub
def save_and_push_key_counts():
    global last_save_time  # Use the global variable

    with open("key_counts.json", "w") as file:
        json.dump({"SingleKeys": dict(key_counts), "CombinationKeys": dict(combination_key_counts)}, file)

    # Commit the changes using Git
    commit_message = "Update key counts"
    subprocess.run(["git", "add", "key_counts.json"])
    subprocess.run(["git", "commit", "-m", commit_message])

    # Push the changes to GitHub
    subprocess.run(["git", "push"])

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
    print(f"Key pressed: {key_str}, Total count: {key_counts[key_str]}")

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

with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
    listener.join()
