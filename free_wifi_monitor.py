import os, sys, re, time
from free_wifi_basekits import *
from free_wifi_config import *

WIFI_CONFIG = WIFI_CONFIG

def isRunning(state):
	# 当前路径下
	return bool(SearchFilesInCondition(path=".", 
		cond=(lambda obj:bool(obj.find(state) >= 0))))

def checkAbort():
	res = "".join(os.popen("netsh wlan show hostednetwork").readlines())
	grp = re.search(r"状态 *: *(.*)", res)
	return bool(not grp or grp.group(1) == "不可用")

def startWIFI():
	os.system("netsh wlan start hostednetwork")

if __name__ == '__main__':

	state = sys.argv[1]
	while isRunning(state):
		if checkAbort():
			LogN("Wifi monitor for {state} is retrying ...".format(state=state))
			startWIFI()
		time.sleep(WIFI_CONFIG["monitor"]["interval"])

	LogN("Wifi monitor for {state} stop !!!".format(state=state))
