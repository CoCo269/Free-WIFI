import os, sys, subprocess
from free_wifi_basekits import *
from free_wifi_config import *

def mtLogPath(file):
	return "/".join((WIFI_CONFIG["dir"]["log"], file))

stdout = open(mtLogPath(WIFI_CONFIG["monitor"]["stdio"]["stdout"]), "w", encoding="utf-8")
stderr = open(mtLogPath(WIFI_CONFIG["monitor"]["stdio"]["stderr"]), "w", encoding="utf-8")

# 重定向当前的输出
sys.stdout = stdout
sys.stderr = stderr

LogN("Boosting monitor ...", flush=True)
state = sys.argv[1]
subprocess.Popen(["python", WIFI_CONFIG["monitor"]["script"]["proc"], state], stdout=stdout, stderr=stderr)
LogN("Boosting finished and quit  ...", flush=True)