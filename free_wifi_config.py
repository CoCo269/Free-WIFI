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
		"proc"     : "free_wifi_monitor_boost.py",
		"interval" : 15,
		"stdio"    : {
			"stdout" : "free_wifi_stdout.txt",
			"stderr" : "free_wifi_stderr.txt",
		},
	}
}