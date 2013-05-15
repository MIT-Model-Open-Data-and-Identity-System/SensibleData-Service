DATABASE= {
			"username":"",
			"password":""
}

AUTH_DATABASE= {
			"username":"",
			"password":""
}

CONNECTORS= {
		"connector_funf": {
			"db_pass": ""
		}

}

SERVICE_CLIENT_ID = ""
SERVICE_CLIENT_SECRET = ""

PROBE_KEYS= {
        "edu_mit_media_funf_probe_builtin_CellProbe": "",
        "edu_mit_media_funf_probe_builtin_WifiProbe": "",
        "edu_mit_media_funf_probe_builtin_BluetoothProbe": "",
        "edu_mit_media_funf_probe_builtin_LocationProbe": "",
        "edu_mit_media_funf_probe_builtin_CallLogProbe": "",
        "edu_mit_media_funf_probe_builtin_SMSProbe": "",
        "edu_mit_media_funf_probe_builtin_HardwareInfoProbe": "",
        "edu_mit_media_funf_probe_builtin_ContactProbe": "",

}


#TODO
PIIS= {
	"edu_mit_media_funf_probe_builtin_CellProbe": {
		"cid": "",
		"lac": "",
	},
	"edu_mit_media_funf_probe_builtin_WifiProbe": {
		"SCAN_RESULTS": {
			"SSID": "",
			"BSSID": "",
		}
	},
	"edu_mit_media_funf_probe_builtin_BluetoothProbe": {
		"DEVICES": {
			"android_bluetooth_device_extra_DEVICE":{
				"mAddress": ""
			}
		}
	},
}

VALUE_KEYS= {
	"user": "",
	"device_id": "",
	"bluetooth_mac": PROBE_KEYS["edu_mit_media_funf_probe_builtin_BluetoothProbe"],
	"wifi_mac": PROBE_KEYS["edu_mit_media_funf_probe_builtin_WifiProbe"],
	"android_id": "",
}

IV= {
	"iv": ""
}
