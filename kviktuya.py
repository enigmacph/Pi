from tuya_iot import TuyaOpenAPI

# Cloud project authorization info
ACCESS_ID = "33d9eey4kujyy9w4rs8q"
ACCESS_KEY = "faf5dd5be9b446c2aa23753fcdd29e41"

# Select an endpoint base on your project availability zone
# For more info, refer to: https://developer.tuya.com/en/docs/iot/api-request?id=Ka4a8uuo1j4t4
ENDPOINT = "https://openapi.tuyaeu.com"

# Project configuration
USERNAME = "esben@kran.ai"
PASSWORD = "2i:!UTVye4DV:sd"

DEVICE_ID = "bf14d5aed474c2ef8bopuj"

# Initialization of tuya openapi
openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect(USERNAME, PASSWORD)

commands = {"commands": [{"code": "switch_led", "value": True}]}
request = openapi.post(f"/v1.0/iot-03/devices/{DEVICE_ID}/commands", commands)
print(request)


# # Example Usage of TinyTuya
# import tinytuya

# d = tinytuya.OutletDevice(
#     "bfcfd63b955077f2616mqc", "192.168.50.168", "4eb0ba087dbfc058"
# )
# d.set_version(3.3)
# data = d.status()
# print("Device status: %r" % data)
