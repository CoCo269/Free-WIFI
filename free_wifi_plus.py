import os, sys
import re
from free_wifi_basekits import *

WIFI_CONFIG = {
	"file"    : "free-wifi-data.csv", 
	"guard"   : "#",
	"format"  : {
		"ssid" : (lambda ssid : bool(re.match(r"[a-zA-Z0-9_]+", ssid))),
		"key"  : (lambda key  : bool(re.match(r"[a-zA-Z0-9!@#$%^&*_]{8,}", key))),
	},
	"monitor" : {
		"name"     : "free-wifi-monitor",
		"interval" : 5000,
	}
}

WIFI_CMD = {
	"check"   : "netsh wlan show drivers",
	"setmode" : "netsh wlan set hostednetwork mode=allow",
	"setnet"  : "netsh wlan set hostednetwork ssid={ssid} key={key}",
	"start"   : "netsh wlan start hostednetwork",
	"stop"    : "netsh wlan stop hostednetwork",
	"status"  : "netsh wlan show hostednetwork",
}

WIFI_ACCOUNTS_INFO = {
	"account_list"  : {
		# "xKey" : "xPassw",
	},  
	"account_order" : [
		# "xPassw",
	],
	"selected" 	    : None, # "xKey"
}

########################## WIFI 控制模块 ##################################
def wfCheck():
	res = "".join(os.popen(WIFI_CMD["check"]).readlines())
	grp = re.search(r"支持的承载网络  : (.*)[\r\n ]*", res)
	return bool(grp and grp.group(1) == "是")

# wifi startup
def wfStart(ssid, key):
	os.system(WIFI_CMD["setmode"])
	os.system(WIFI_CMD["setnet"].format(ssid=ssid,key=key))
	os.system(WIFI_CMD["start"])

# wifi stop
def wfStop():
	os.system(WIFI_CMD["stop"])

# wifi status
def wfStatus():
	return "".join(os.popen(WIFI_CMD["status"]).readlines())

########################## ACCOUNT 管控模块 ##################################
def acInit():
	file = WIFI_CONFIG["file"]
	with open(file, 'a'):
		pass

def acLoad():
	account_list     = {}
	account_selected = None
	with open(WIFI_CONFIG["file"], "r") as fr:
		for account in fr.readlines():
			account = account.strip()
			if not account:
				continue
			account  = account.split(',')
			ssid 	 = account[0] 
			key      = account[1]
			selected = bool(len(account) > 2 and account[2] == WIFI_CONFIG["guard"])
			account_list[ssid] = key
			account_selected   = (ssid if selected else account_selected)
	WIFI_ACCOUNTS_INFO["account_list"] = account_list
	WIFI_ACCOUNTS_INFO["selected"]     = account_selected

def acDump():
	with open(WIFI_CONFIG["file"], "w") as fw:
		account_list = WIFI_ACCOUNTS_INFO["account_list"]
		for ssid in account_list:
			key = account_list[ssid]
			fw.write("{}\n".format(",".join((ssid,key,WIFI_CONFIG["guard"]) 
				if ssid == WIFI_ACCOUNTS_INFO["selected"] else (ssid,key))))

def acRefresh():
	# sorted list for accounts' ssid
	WIFI_ACCOUNTS_INFO["account_order"] = sorted(WIFI_ACCOUNTS_INFO["account_list"].keys())
	# check selected ssid, if not choose a default one
	if WIFI_ACCOUNTS_INFO["selected"] not in WIFI_ACCOUNTS_INFO["account_order"]:
		WIFI_ACCOUNTS_INFO["selected"] = (WIFI_ACCOUNTS_INFO["account_order"][0] if WIFI_ACCOUNTS_INFO["account_order"] else None)
	# DEBUG
	LogP(WIFI_ACCOUNTS_INFO)

def acFilter(ssid, key):
	return bool(WIFI_CONFIG["format"]["ssid"](ssid) and WIFI_CONFIG["format"]["key"](key))

## 以下账户管理函数为基本操作的实现 ##
def acListAll():
	infos         = []
	account_order = WIFI_ACCOUNTS_INFO["account_order"]
	for idx, ssid in enumerate(account_order):
		info = [idx, ssid, WIFI_ACCOUNTS_INFO["account_list"][ssid], ""]
		if WIFI_ACCOUNTS_INFO["selected"] == ssid:
			info[3] = WIFI_CONFIG["guard"]
		infos.append(info)
	return infos

def acUpdate(ssid, key):
	if not acFilter(ssid, key):
		raise IncorrectFormatError
	WIFI_ACCOUNTS_INFO["account_list"][ssid] = key
	acRefresh()
	acDump()

def acDelete(idx):
	if idx < 0 or idx >= len(WIFI_ACCOUNTS_INFO["account_order"]):
		raise AccountNotFoundError
	ssid = WIFI_ACCOUNTS_INFO["account_order"][idx]
	del WIFI_ACCOUNTS_INFO["account_list"][ssid]
	acRefresh()
	acDump()

def acSelect(idx):
	if idx < 0 or idx >= len(WIFI_ACCOUNTS_INFO["account_order"]):
		raise AccountNotFoundError
	WIFI_ACCOUNTS_INFO["selected"] = WIFI_ACCOUNTS_INFO["account_order"][idx]
	acDump()

########################## CMD 模块 ##################################
class CommandLines:
	def __init__(self, cmds):
		if not isinstance(cmds, dict):
			raise TypeError("cmd map must be a dictionary")
		self.cmds = cmds or {}
	def run(self):
		while 1:
			try:
				comd = input("\n>>")
				comd = comd.strip().split(' ')
				if comd[0] in self.cmds:
					self.cmds[comd[0]](*(comd[1:] if len(comd) > 1 else []))
				else:
					LogW("Unknown Command ...")
			except Exception as err:
				LogE("Unknown Error in Command: ", err)

########################## 指令逻辑流程 ##################################
def InitWifi():
	checkDrivers()
	acInit()
	acLoad()
	acRefresh()

def checkDrivers():
	LogN("Drivers checking ...")
	if not wfCheck():
		LogW("Sorry, your drivers not support wifi hotspot, any press to exit ...")
		input()
		quit()

def StartWifi(*args, **kwargs):
	if not WIFI_ACCOUNTS_INFO["selected"]:
		LogW("There is no account in configuration file {file} yet, please new one ...".format(file=WIFI_CONFIG["file"]))
		return
	ssid = WIFI_ACCOUNTS_INFO["selected"]
	key  = WIFI_ACCOUNTS_INFO["account_list"][ssid]
	wfStart(ssid, key)
	LogN("Wifi has started !!!")

def StopWifi(*args, **kwargs):
	wfStop()
	LogN("Wifi has stopped !!!")

def ShowWifi(*args, **kwargs):
	stat = wfStatus()
	grp  = re.search(r"SSID 名称 *:“(.*)”", stat)

	accs = WIFI_ACCOUNTS_INFO["account_list"]
	ssid = (grp.group(1) if grp else "")
	key  = (accs[ssid] if ssid in accs else "")

	LogN("Wifi State as follow:")
	LogN("Wifi Name: {ssid}".format(ssid=ssid))
	LogN("Wifi Code: {key}".format(key=key))
	LogN(stat)

def ListAccount(*args, **kwargs):
	accs = acListAll()
	LogP("----------- Users Info -----------")
	for acc in accs:
		LogP("{idx}. {ssid} : {key} {selected}".format(idx=acc[0],ssid=acc[1],key=acc[2],selected=acc[3]))
	LogP("----------------------------------")

def UpdateAccount(*args, **kwargs):
	try:
		ssid, key = args[0].split(":")
		acUpdate(ssid, key)
	except IncorrectFormatError as err:
		LogW(err)
	except Exception as err:
		LogW("Mismatch input format <ssid>:<key>, your input is {}".format(args))

def DeleteAccount(*args, **kwargs):
	try:
		acidx = int(args[0])
		acDelete(acidx)
	except AccountNotFoundError as err:
		LogW(err)
	except Exception as err:
		LogW("Mismatch input format <tag>, your input is {}".format(args))

def SelectAccount(*args, **kwargs):
	try:
		acidx = int(args[0])
		acSelect(acidx)
		LogN("Account {ssid} selected !!!".format(ssid=WIFI_ACCOUNTS_INFO["selected"]))
	except AccountNotFoundError as err:
		LogW(err)
	except Exception as err:
		LogW("Mismatch input format <tag>, your input is {}".format(args))

def StartMonitor(*args, **kwargs):
	pass

def StopMonitor(*args, **kwargs):
	pass

def Clear(*args, **kwargs):
	os.system("cls")

def TipInfo():
	LogP("============== Free Wifi =============")
	LogP("""Support Command:\n  start | stop | show\n  new <ssid>:<key> | delete <tag>\n  list | select <tag>\n help | clear | quit\n""")

def Quit(*args, **kwargs):
	LogN("Wifi manger quit now ...")
	quit()

CMD_LOGFUNCS = {
	# wifi
	"start"	:	StartWifi, 
	"stop"	:	StopWifi, 
	"show"  :	ShowWifi, 
	# accounts
	"new"	:	UpdateAccount, 
	"delete":	DeleteAccount, 
	"list"	:	ListAccount, 
	"select":	SelectAccount, 
	# monitor
	# "spy"	:	StartMonitor,
	# "fade"	:	StopMonitor,
	# control
	"help"  :   TipInfo,
	"clear"	:	Clear, 
	"quit"	:	Quit, 
}

if __name__ == '__main__':
	InitWifi()
	Clear()

	cmd = CommandLines(CMD_LOGFUNCS)
	TipInfo()
	cmd.run()

