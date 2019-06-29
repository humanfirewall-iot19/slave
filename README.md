# slave

This repo contains the slave of the Human-firewall project.
The code was written using Python3 and comes in two "flavors":
- Laptop: supports image taking from the laptop's webcam and provides a basic GUI.
- PI: supports image taking from the PI Camera and the doorbell button input.

## Features

The slave system takes care of the following operations:
- Searching of the master over the LAN.
- Image taking (from webcam or PI Camera).
- Face recognition and encoding.
- Management of the user feedback using a local DB.
- Notifying the master by sending the photo and all the relevant information about the subject in it.
- Receiving the users' feedback over an MQTT queue.

## How to deploy 
For the deployment use the [slave-scripts](https://github.com/humanfirewall-iot19/slave-scripts).
The script will take care of installing all the needed dependencies and executing the slave in a correct manner.

## Dependencies

For the full list of dependencies refer to the [requirements file](requirements.txt)
