import json
import logging
import os
import time

import django
import paho.mqtt.client as mqtt


def start_pumping(client, node):
    # Open valve
    client.publish(
        f'green/settings/{node.chip_id}',
        {'is_open': True},
        qos=2
    )

    # Ask for pump to start
    time.sleep(5)
    client.publish(
        f'green/settings/{node.pump.chip_id}',
        {'is_open': True},
        qos=2
    )

    logging.info(f'Pumping started: {node.pump.chip_id} -> {node.chip_id}')


def stop_pumping(client, node):
    # Ask for pump to stop
    client.publish(
        f'green/settings/{node.pump.chip_id}',
        {'is_open': False},
        qos=2
    )

    # Close valve
    time.sleep(5)
    client.publish(
        f'green/settings/{node.chip_id}',
        {'is_open': False},
        qos=2
    )

    logging.info(f'Pumping stopped: {node.pump.chip_id} -> {node.chip_id}')


def on_message(client, userdata, message):
    from web.models import Node, Record

    logging.info('Received message: %s', message.payload.decode('utf-8'))
    payload = json.loads(message.payload)

    if message.topic == 'green/record':
        node = Node.objects.filter(chip_id=payload['node_id']).first()

        if node:
            # Create record
            record = Record.objects.create(
                node=node,
                moisture=payload['moisture']
            )

            match node.node_type:
                case Node.TYPE_FULL:
                    node.is_open = payload['is_open']
                    node.save()

                case Node.TYPE_VALVE:
                    if node.min_moisture and record.moisture < node.min_moisture:
                        start_pumping(client, node)
                        Node.objects.filter(id__in=(node.id, node.pump.id)).update(is_open=True)

                    if node.max_moisture and record.moisture > node.max_moisture:
                        stop_pumping(client, node)
                        Node.objects.filter(id__in=(node.id, node.pump.id)).update(is_open=False)


def main():
    # Create client
    client = mqtt.Client()
    client.on_message = on_message

    # Connect to broker
    client.connect(os.environ['MQTT_BROKER_HOST'], int(os.environ['MQTT_BROKER_PORT']))
    client.subscribe('green/record')

    logging.info('Monitor started')

    client.loop_forever()


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(asctime)s] %(levelname)s: %(message)s',
        level=logging.INFO
    )
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'green.settings')
    django.setup()
    main()
