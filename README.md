# PolluComE
This script reads data from a Sensus PolluCom E heat meter and publishes the results to an MQTT broker. Because I could'nt found a working solution which runs directly on an ESP, I used [esp-link](https://github.com/jeelabs/esp-link) to provide a virtual serial port that is used by this script.
## Prerequisites
* socat
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