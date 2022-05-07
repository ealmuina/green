import json
import os

import django
import paho.mqtt.client as mqtt


def on_message(client, userdata, message):
    from web.models import Node, Record

    payload = json.loads(message.payload)

    if message.topic == 'green/record':
        node = Node.objects.filter(chip_id=payload['node_id']).first()

        if node:
            # Create record
            Record.objects.create(
                node=node,
                moisture=payload['moisture']
            )
            # Update node status
            node.is_open = payload['is_open']
            node.save()


def main():
    # Create mqtt_client
    mqtt_client = mqtt.Client()
    mqtt_client.on_message = on_message

    # Connect to broker
    mqtt_client.connect(os.environ['MQTT_BROKER_HOST'], int(os.environ['MQTT_BROKER_PORT']))
    mqtt_client.subscribe('green/record')

    mqtt_client.loop_forever()


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'green.settings')
    django.setup()
    main()
