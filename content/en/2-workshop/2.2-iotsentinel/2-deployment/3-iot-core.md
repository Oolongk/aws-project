---
weight: 3
date: "2026-05-13"
title: "Configure AWS IoT Core & IoT Rules"
chapter: false
pre: "<b>2.2.2.3. </b>"
---

#### 1. Create a "Thing" for the Truck Fleet
In AWS IoT Core, each truck is treated as a "Thing". We will create an identity representing the entire fleet.

1. Open the **IoT Core** service.
2. Go to **Manage** > **All devices** > **Things** > Click **Create things**.
3. Select **Create single thing** > Click **Next**.
4. **Thing name**: `Vaccine_Truck_Fleet` > Click **Next**.
5. Select **Auto-generate a new certificate** > Click **Next**.

**Download Security Certificates (Extremely Important):**
1. On the **Download certificates** page, download the following 3 files:
   - `Device certificate`
   - `Private key file`
   - `Amazon Root CA 1`
2. **Note**: Once you leave this page, you will never be able to download the Private key again. Save them to the `certs/` folder in your project on your computer.

![Download IoT Certificates](/aws-project/images/IoTSentinel/2-trien-khai/iot_certs.png?featherlight=false&width=90pc)

3. Click **Done**. (Skip the Attach Policy section for now, we will use the default Policy).

---

#### 2. Configure IoT Rule (Data Routing)
This Rule will automatically capture messages sent to the `telemetry/trucks` Topic and push them directly into the SQS queue created in lesson 2.2.

1. Go to the **Message routing** menu > **Rules** > Click **Create rule**.
![Configure IoT Rule](/aws-project/images/IoTSentinel/2-trien-khai/iot_rule_1.png?featherlight=false&width=90pc)

2. **Rule name**: `IoT_To_SQS_Rule`.
![Configure IoT Rule](/aws-project/images/IoTSentinel/2-trien-khai/iot_rule_2.png?featherlight=false&width=90pc)

3. **SQL statement**: Enter the statement to retrieve all data:
   ```sql
   SELECT * FROM 'telemetry/trucks'
   ```
4. Click **Next**.
![Configure IoT Rule](/aws-project/images/IoTSentinel/2-trien-khai/iot_rule_3.png?featherlight=false&width=90pc)

5. **Attach action**: Select **SQS queue**.
   - Select queue: `IoT_Fleet_Queue`.
6. Click **Create**.

![Configure IoT Rule](/aws-project/images/IoTSentinel/2-trien-khai/iot_rule_4.png?featherlight=false&width=90pc)

---

#### 3. Get the Connection Endpoint

For the truck simulator software to know "where" AWS is to send data, you need to retrieve the unique **Endpoint** address of your account. In the new UI, this information has been moved to the Domain Configuration section.

1. In the left menu bar of **AWS IoT Core**, scroll to the top.
2. Find the **Connect** menu group and select **Domain configurations**.
3. On the main interface, you will see the **Domain name** column. This is your Endpoint address.
4. Copy this address string (in the format `afjy7...-ats.iot.ap-southeast-1.amazonaws.com`) and save it for use in Chapter 3.

![Get IoT Endpoint from Domain Configuration](/aws-project/images/IoTSentinel/2-trien-khai/iot_endpoint_new.png?featherlight=false&width=90pc)
