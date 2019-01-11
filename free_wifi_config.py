import re

WIFI_CONFIG = {
	"account" : "free-wifi-account.csv", 
	"guard"   : "#",
	"format"  : {
		"ssid" : (lambda ssid : bool(re.match(r"[a-zA-Z0-9_]+", ssid))),
		"key"  : (lambda key  : bool(re.match(r"[a-zA-Z0-9!@#$%^&*_]{8,}", key))),
	},
	"monitor" : {
		"state"    : {
			"prefix" : "wifi_monitor_",
			"size"   : 32, # UUID 长度
		},
		"script"   : {
			"vbs"    : "free_wifi_monitor_backgroud.vbs",
			"boost"  : "free_wifi_monitor_boost.py",
			"proc"   : "free_wifi_monitor.py",
		},
		"stdio"    : {
			"stdout" : "free_wifi_stdout.txt",
			"stderr" : "free_wifi_stderr.txt",
		},
		"interval" : 15, # 定时检查秒数
	},
	"dir"     : {
		"log" 	: "./log",
		"tmp" 	: "./tmp",
		"data"	: "./data", 
	}
}