import json 
import collections
import threading
from datetime import datetime
import time
import git
import socket
from pynput import keyboard

# Config
CONFIG = {} 

# State
KEY_COUNTS = {}
COMBO_COUNTS = {}
LAST_SAVE = datetime.now()

LOCK = threading.Lock()
REPO = git.Repo('.')
HOSTNAME = socket.gethostname()
BRANCH = f'machine-{HOSTNAME}'

def on_press(key):
  global KEY_COUNTS, COMBO_COUNTS

  try:
    key_str = key.char
  except:
    key_str = str(key)    

  with LOCK:

    KEY_COUNTS[key_str] = KEY_COUNTS.get(key_str, 0) + 1

    if COMBO_COUNTS:
      combo = '+'.join(sorted(COMBO_COUNTS))
      COMBO_COUNTS[combo] = COMBO_COUNTS.get(combo, 0) + 1

    COMBO_COUNTS[key_str] = True

def on_release(key):
    global COMBO_COUNTS
    
    try:
        key_str = key.char
    except:
        key_str = str(key)

    with LOCK:
        COMBO_COUNTS.pop(key_str, None)
  
def save_and_push():
    # Save key counts to file
    with open(CONFIG['path'], 'w') as f:
        json.dump(KEY_COUNTS, f) 
    
    # Commit and push
    commit_msg = CONFIG['commit_template'].format(...)
    REPO.git.add(CONFIG['path'])
    REPO.git.commit(commit_msg)
    REPO.remote().push()

def main():
  global LAST_SAVE
  while True:
    if datetime.now() - LAST_SAVE > 60:
      save_and_push()
    LAST_SAVE = datetime.now() # Update every loop 
    time.sleep(1)

if __name__ == "__main__":

  main()