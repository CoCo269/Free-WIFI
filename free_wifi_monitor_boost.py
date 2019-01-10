import os, sys, subprocess
from free_wifi_basekits import *
from free_wifi_config import *

LogN("Boosting monitor ...")
state = sys.argv[1]
subprocess.Popen(["python", "free_wifi_monitor.py", state])
