import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import sdm_modbus
import time
import json
from os import environ

if environ.get("UPDATE_TIME"):
    update_time = int(environ.get("UPDATE_TIME"))
else:
    update_time = 5


sdm_ip = environ.get('SDM_IP')
sdm_port = int(environ.get('SDM_PORT'))
sdm_type = environ.get('SDM_TYPE')
sdm_network_type = environ.get('SDM_NETWORK_TYPE')
sdm_id = int(environ.get('SDM_ID'))

mqtt_broker_ip = environ.get('MQTT_BROKER_IP')
mqtt_broker_port = int(environ.get('MQTT_BROKER_PORT'))
mqtt_broker_auth = environ.get('MQTT_BROKER_AUTH')
if mqtt_broker_auth:
    mqtt_broker_auth = json.loads(mqtt_broker_auth)
mqtt_meter_topic = environ.get('MQTT_SDM_TOPIC')


def publish_message(topic, data, ip, port, auth):
    """ publish the message to the mqtt broker
    --- accepts a JSON payload
    --- publishs to the """
    ## following line is for local broker
    client = mqtt.Client(client_id="SDM_Meter")
    if auth:
        client.username_pw_set(username=auth["username"], password=auth["password"])
    client.connect(ip, port, 60)
    client.publish(topic + "/Full_Status", json.dumps(data))
    # client.publish(topic, json.dumps(data))
    # publish.single(topic, payload=json.dumps(data), hostname=ip, port=port, auth=json.loads(auth), client_id="Energymeter",)
    for i in data:
        # publish.single(topic+"/"+field_map_s0[i], payload=str(data[i]["Value"]), hostname=ip, port=port, auth=json.loads(auth), client_id="Energymeter",)
        client.publish(topic+"/"+i, data[i])
        time.sleep(0.005)
    print ('published: ' + json.dumps(data) + '\n' + 'to topic: ' + topic)
    client.disconnect()
    return

def read_data(device):
    data = device.read_all(sdm_modbus.registerType.INPUT)
    return data

def connect_to_device(ip, port, network_type, device_type, device_id):
    dev = getattr(sdm_modbus, device_type)
    if network_type == "tcp":
        return dev(host=ip, port=port, unit=device_id)
    # 
    elif network_type == "udp":
        return dev(host=ip, port=port, udp=True, unit=device_id)
    else:
        raise Exception("Unknown network type: " + network_type)

def main():
    print ("starting...")
    device = connect_to_device(sdm_ip, sdm_port, sdm_network_type.lower(), sdm_type, sdm_id)
    print ("connected to device")        
    while True:
        try:
            if device.connected():
                data = read_data(device)
            else:
                print ("failed to connect to sdm meter")
                time.sleep(10)
                continue
            publish_message(topic=mqtt_meter_topic, data=data, ip=mqtt_broker_ip, port=mqtt_broker_port, auth=mqtt_broker_auth)
            time.sleep(update_time)

        except Exception as ex:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print (message)
            continue

main()