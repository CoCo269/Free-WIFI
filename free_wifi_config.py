import re

WIFI_CONFIG = {
	"file"    : "free-wifi-data.csv", 
	"guard"   : "#",
	"format"  : {
		"ssid" : (lambda ssid : bool(re.match(r"[a-zA-Z0-9_]+", ssid))),
		"key"  : (lambda key  : bool(re.match(r"[a-zA-Z0-9!@#$%^&*_]{8,}", key))),
	},
	"monitor" : {
		"state"    : {
			"prefix" : "wifi_monitor_",
			"size"   : 32,
		},
		"vbs"      : "tmp/free_wifi_monitor_backgroud.vbs",
		"boost"    : "free_wifi_monitor_boost.py",
		"proc"     : "free_wifi_monitor.py",
		"interval" : 3,
		"stdio"    : {
			"stdout" : "log/free_wifi_stdout.txt",
			"stderr" : "log/free_wifi_stderr.txt",
		},
	}
}