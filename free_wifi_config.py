import re

WIFI_CONFIG = {
	"file"    : "free-wifi-data.csv", 
	"guard"   : "#",
	"format"  : {
		"ssid" : (lambda ssid : bool(re.match(r"[a-zA-Z0-9_]+", ssid))),
		"key"  : (lambda key  : bool(re.match(r"[a-zA-Z0-9!@#$%^&*_]{8,}", key))),
	},
	"monitor" : {
		"prefix"   : "wifi_monitor_",
		"size"     : 32,
		"proc"     : "free_wifi_monitor.py",
		"interval" : 15,
	}
}