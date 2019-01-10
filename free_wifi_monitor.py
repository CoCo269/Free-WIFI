import os, re, time
from free_wifi_basekits import *
from free_wifi_config import *

WIFI_CONFIG = WIFI_CONFIG

def isRunning():
	# 当前路径下
	return bool(SearchFilesInCondition(path=".", 
		cond=(lambda obj:bool(obj.find(WIFI_CONFIG["monitor"]["prefix"]) >= 0))))

def checkAbort():
	res = "".join(os.popen("netsh wlan show hostednetwork").readlines())
	grp = re.search(r"状态 *: *(.*)", res)
	return bool(not grp or grp.group(1) == "不可用")

def startWIFI():
	os.system("netsh wlan start hostednetwork")

while isRunning():
	if checkAbort():
		startWIFI()
	time.sleep(WIFI_CONFIG["monitor"]["interval"])

LogN("Free wifi monitor stop !!!")
