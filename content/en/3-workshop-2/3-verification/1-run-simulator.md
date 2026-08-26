---
weight: 1
date: "2026-05-13"
title: "Run IoT Device Simulator"
chapter: false
pre: "<b>2.2.3.1. </b>"
---

#### 1. Update the Python Source Code

Return to your project folder on your computer, open the `truck_simulator.py` file (created in Chapter 1) and update the 2 most important pieces of information we just retrieved from AWS IoT Core in Lesson 2.3:

1. **IOT_ENDPOINT**: Paste your Endpoint address here.
2. **Security certificates**: Make sure the paths to the 3 certificate files (`Root CA`, `Certificate`, `Private Key`) are correct.

```python
# ==========================================
# CONFIGURATION SETTINGS
# ==========================================
IOT_ENDPOINT = "afjy7...-ats.iot.ap-southeast-1.amazonaws.com" # Replace with yours

PATH_TO_ROOT_CA = "certs/AmazonRootCA1.pem"
PATH_TO_CERT = "certs/128eb8547f...-certificate.pem.crt" # Update to your file name
PATH_TO_PRIVATE_KEY = "certs/128eb8547f...-private.pem.key" # Update to your file name
```

Save the file.

#### 2. Activate the Truck Fleet

Now, open a **Terminal** (or Command Prompt) in the directory containing the `truck_simulator.py` file and run the following command:

```bash
python truck_simulator.py
```

If all settings are correct, you will see the Terminal print a successful connection message and continuously push GPS and temperature data (from 2°C - 8°C) to AWS every second!

![Run Python script](/aws-project/images/IoTSentinel/3-kiem-tra/run_script.png?featherlight=false&width=90pc)

> **Tip:** Let the Terminal keep running to simulate trucks on the road. We will switch to the browser to see how AWS is "receiving" this data.