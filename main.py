import os
import requests
import faces

if os.uname()[4][:3] == "arm":
    import raspberry as dev
else:
    import laptop as dev

if os.path.exists(os.path.expanduser("~/master_ip")):
    MASTER_IP = open(os.path.expanduser("~/master_ip")).read()
else:
    MASTER_IP = "0.0.0.0" # debug

def image_handler(image_path):
    pass

dev.register_handler(image_handler)
dev.device_setup_and_idle()

