# PolluComE
This script reads data from a Sensus PolluCom E heat meter and publishes the results to an MQTT broker. Because I could'nt found a working solution which runs directly on an ESP, I used [esp-link](https://github.com/jeelabs/esp-link) to provide a virtual serial port that is used by this script.
## Prerequisites
* socat