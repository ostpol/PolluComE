# PolluComE
This script is designed to read data from a Sensus PolluCom E heat meter and publish the results to an MQTT broker. Since I couldn't find a direct solution that works on an ESP, I utilized [esp-link](https://github.com/jeelabs/esp-link) to establish a virtual serial port that is used by this script.

The entire communication aspect is based on the work of [93schlucko](https://forum-raspberrypi.de/forum/thread/57389-sensus-pollucom-e-ueber-pymeterbus-auslesen/?postID=543096#post543096). Additionally, [this thread](https://www.mikrocontroller.net/topic/438972?page=single) (in German) serves as a valuable source of information about the topic.

## Prerequisites
### Linux
* socat
### Python
* pyserial
* requests
* paho-mqtt
* pyMeterBus

## Using Docker

### Building the image
`docker build . -t fancyimagename`

### Running the container
`docker run --env=ESP_IP=x.x.x.x --env=MQTT_PORT=1883 --env=MQTT_BROKER=y.y.y.y --env=MQTT_CLIENT=ClientName --env=MQTT_TOPIC=your/topic --env=MQTT_USER=j --env=MQTT_PWD=j --env=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin --env=PYTHONUNBUFFERED=1 --runtime=runc -d fancyimagename`

### Environment Variables
| Env           | Content       |
| ------------- |-------------|
| ESP_IP        | IP of esp-link |
| MQTT_BROKER      | IP of MQTT broker      |
| MQTT_PORT | port of MQTT broker      |
| MQTT_TOPIC | topic to publish readings to      |
| MQTT_CLIENT | MQTT client name e.g. PolluComE      |
| MQTT_USER | MQTT user if needed      |
| MQTT_PWD | MQTT password if needed      |