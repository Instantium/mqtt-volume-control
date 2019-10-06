#!/usr/bin/python3

import smbus
import paho.mqtt.client as mqtt
import yaml

# Initial volume:
default_volume = 0.8

# Generic class to control audio volumes
class VolumeControl:

  def __init__(self, id, config):
    self.id = id
    if default_volume in config:
      self.volume = config.default_volume
    self.muted = 'OFF'
    self.volume_topic = topic_prefix + '/sensor/' + self.id + '/volume'
    self.mute_topic = topic_prefix + '/binary_sensor/' + self.id + '/mute'
    self.publish()

  # def discovery(self):
  
  def publish(self):
    # publish current volume level
    mqttc.publish(self.volume_topic, self.volume)
    mqttc.publish(self.mute_topic, self.muted)

class PT2259VolumeControl(VolumeControl):
  
  def __init__(self, id, config):
    super().__init__(id, config)

class AlsaVolumeControl(VolumeControl):
  
  def __init__(self,id, config):
    super().__init__(id, config)

def load_config():
  # Read the configuration file
  config_file = open('configuration.yaml', 'r')
  # Parse the configuration into a dictionary
  config = yaml.safe_load(config_file)
  config_file.close
  return config

def on_message(client, userdata, message):
  payload = str(message.payload.decode("utf-8"))
  topic = message.topic
  if topic == vc_set_topic:
    vc_set(payload)

## Main routine ##

# Load the configuration file
config = load_config()
print(config)

# Initialize the mqtt client
mqttc = mqtt.Client()


# Populate the device list
devices = {}
for device_id, device_config in config['devices'].items():
  if device_config['platform'] == 'pt2259':
    devices[device_id] = PT2259VolumeControl(device_id, device_config)

# Loop


# import smbus
# bus = smbus.SMBus(1)
# bus.write_byte(0x44,0xF0)
# >>> bus.write_i2c_block_data(0x44,0x74,[0xE2,0xD0])
# >>> bus.write_i2c_block_data(0x44,0x74,[0xE0,0xD0])
# bus.write_i2c_block_data(0x44,0xF0,[0x74,0xE0,0xD0])
