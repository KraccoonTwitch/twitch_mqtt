#!/usr/bin/python3
import json
import paho.mqtt.publish as publish
import socketio
import os
sio = socketio.Client()

def get_env_or_exit(name):
    if not name in os.environ:
        print(f"Error: {name} environement variable is not set")
        exit(1)
    return os.environ[name]

twitch_name = get_env_or_exit('TWITCH_NAME')
token = get_env_or_exit('SLABS_SOCKET_TOKEN')

@sio.event
def event(data):
    if data['type'] == 'donation':
        for m in data['message']:
            username = m['name']
            amount = m['amount']
            currency = m['currency']
            data_to_send = {'username': username, 'amount': amount, 'currency': currency}
            if m['isTest']:
                print(data_to_send)
            else:
                publish.single(f"/{twitch_name}/donation", json.dumps(data_to_send), hostname="localhost")


sio.connect(f'https://sockets.streamlabs.com?token={token}')
sio.wait()

