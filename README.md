# SDM Meter via Modbus to mqtt agent

Python script which polls a Eastron SDM Meter via Modbus TCP or UDP and publishes the data to an mqtt broker.

Based on the excellent sdm_modbus (https://github.com/nmakel/sdm_modbus) library

## Features:
- Parameters are set with environment variables
- Exception Handling without exiting
- Docker Image available

## dependencies
 - sdm_modbus (https://github.com/oschick/sdm_modbus_udp)
 - paho-mqtt  (https://pypi.org/project/paho-mqtt/)
