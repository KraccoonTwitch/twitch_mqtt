#!/usr/bin/python3
import websocket
import _thread as thread
import time
import json
import paho.mqtt.publish as publish
import os

def get_env_or_exit(name):
    if not name in os.environ:
        print(f"Error: {name} environement variable is not set")
        exit(1)
    return os.environ[name]

twitch_name = get_env_or_exit('TWITCH_NAME')
twitch_id = get_env_or_exit('TWITCH_ID')
token = get_env_or_exit('TWITCH_TOKEN')

def on_message(ws, message):
    jsonmsg = json.loads(message)
    if jsonmsg['type']=="MESSAGE":
        jsondata = json.loads(jsonmsg['data']['message'])
        if jsonmsg['data']['topic'].startswith("channel-bits-events-v2"):
            username = None if jsondata['data']['is_anonymous'] else jsondata['data']['user_name']
            amount = jsondata['data']['bits_used']
            message = jsondata['data']['chat_message'] if 'chat_message' in jsondata['data'] else ""
            data = {'username': username, 'amount': amount, 'message': message}
            publish.single(f"/{twitch_name}/bits", json.dumps(data), hostname="localhost")
        elif jsonmsg['data']['topic'].startswith("channel-points-channel-v1"):
            username = jsondata['data']['redemption']['user']['login']
            reward_id = jsondata['data']['redemption']['reward']['id']
            message = jsondata['data']['redemption']['user_input'] if 'user_input' in jsondata['data']['redemption'] else ""
            data = {'reward_id': reward_id, 'username': username, 'message': message}
            publish.single(f"/{twitch_name}/channelpoints", json.dumps(data), hostname="localhost")
        elif jsonmsg['data']['topic'].startswith("channel-subscribe-events-v1"):
            username = None if jsondata['context']=="anonsubgift" else jsondata['user_name']
            recipient_name = jsondata['recipient_user_name'] if jsondata['is_gift'] else username
            tier = 1 if jsondata['sub_plan']=="Prime" else int(int(jsondata['sub_plan'])/1000)
            message = jsondata['sub_message']['message'] if 'message' in jsondata['sub_message'] else ""
            data = {'tier': tier, 'username': username, 'recipient_name': recipient_name, 'message': message}
            publish.single(f"/{twitch_name}/sub", json.dumps(data), hostname="localhost")
        else:
            print(jsondata)
    else:
        print(jsonmsg['type'])

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        to_send = {
                "type":"LISTEN",
                "nonce": "ofOcR2JdAz4ccp3",
                "data":{
                    "topics":[
                        f"channel-bits-events-v2.{twitch_id}",
                        f"channel-points-channel-v1.{twitch_id}",
                        f"channel-subscribe-events-v1.{twitch_id}"
                    ],
                    "auth_token":token
                }
            }
        print(to_send)
        ws.send(json.dumps(to_send))
        while True:
            time.sleep(30)
            ws.send('{"type":"PING"}')
    thread.start_new_thread(run, ())


#if __name__ == "__main__":
ws = websocket.WebSocketApp("wss://pubsub-edge.twitch.tv",
                                    on_message = on_message,
                                    on_error = on_error,
                                    on_close = on_close)
ws.on_open = on_open
ws.run_forever()

