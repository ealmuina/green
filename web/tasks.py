import json
import os

import paho.mqtt.client as mqtt

from green.celery import app
from web.models import Node


@app.task(ignore_result=True)
def refresh_node_settings():
    client = mqtt.Client()
    client.connect(os.environ['MQTT_BROKER_HOST'], int(os.environ['MQTT_BROKER_PORT']))

    for node in Node.objects.filter(node_type__in=(Node.TYPE_FULL, Node.TYPE_VALVE)):
        client.publish(
            f"green/settings/{node.chip_id}",
            json.dumps({
                "min_moisture": node.min_moisture,
                "max_moisture": node.max_moisture,
                "max_open_time": node.max_open_time
            }),
            retain=True,
            qos=2
        )

    client.disconnect()
