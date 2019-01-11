import os, sys, subprocess
from free_wifi_basekits import *
from free_wifi_config import *

stdout = open(WIFI_CONFIG["monitor"]["stdio"]["stdout"], "w", encoding="utf-8")
stderr = open(WIFI_CONFIG["monitor"]["stdio"]["stderr"], "w", encoding="utf-8")

# 重定向当前的输出
sys.stdout = stdout
sys.stderr = stderr

LogN("Boosting monitor ...", flush=True)
state = sys.argv[1]
subprocess.Popen(["python", WIFI_CONFIG["monitor"]["proc"], state], stdout=stdout, stderr=stderr)
LogN("Boosting finished and quit  ...", flush=True)