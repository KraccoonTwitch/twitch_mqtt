# Twitch MQTT
## Get realtime events from Twitch Pub/Sub and Streamlabs SocketIO  and pub it to MQTT for a easier use

![Diagram showing the link between the APIs and the MQTT server] (https://github.com/KraccoonTwitch/twitch_mqtt/blob/master/images/diagram.png?raw=true)

## Requirements

### 1. You need to install a MQTT broker on the same server that will run this scripts.
I used [Mosquitto](https://mosquitto.org/)

### 2. Create a python virtenv and run `pip install -r requirements.txt`

### 3. You have to add several envirnement variables:
* TWITCH\_NAME: your twitch username
* TWITCH\_ID: your twitch id (only needed for the "twitch\_pubsub" script)
* TWITCH\_TOKEN: twitch token with access of this scopes: channel:read:redemptions+bits:read+channel\_subscriptions (only needed for the "twitch\_pubsub" script)
* SLABS\_SOCKET\_TOKEN: streamlabs socket token (only needed for the "streamlans\_socketio" script)

## Format of MQTT messages

### /{streamernanme}/bits Topic
```json
{
    "amount": 0,
    "username": "name"
}
```
*username is None for anonymous cheer*

### /{streamernanme}/channelpoints Topic
```json
{
    "reward_id": 0,
    "username": "name"
}
```

### /{streamernanme}/sub Topic
```json
{
    "tier": 1,
    "username": "name",
    "recipient_name": "name"
}
```
*recipient_name if different of username ifthis is a gift*

*username is None for anonymous gift sub*

### /{streamernanme}/donation Topic
```json
{
    "amount": 1,
    "username": "name",
    "currency": "EUR"
}
```
