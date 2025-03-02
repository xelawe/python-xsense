import argparse
import contextlib

from xsense.base import XSenseBase


def get_mqttenv():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mqtthost', help='MQTT Host')
    parser.add_argument('--mqttpwd', help='MQTT Password')
    parser.add_argument('--mqttusr', help='MQTT Username')
    parser.add_argument('--mqtttopic', help='MQTT Topic')
    args = parser.parse_args()

    if args.mqtthost and args.mqttusr and args.mqttpwd and args.mqtttopic:
        return args.mqtthost, args.mqttusr, args.mqttpwd, args.mqtttopic

    with contextlib.suppress(FileNotFoundError):
        with open('.env', 'r') as file:
            for line in file:
                with contextlib.suppress(ValueError):
                    key, value = line.strip().split('=')
                    if key.lower() == 'mqtthost':
                        mqtthost = value
                    elif key.lower() == 'mqttusr':
                        mqttusr = value
                    elif key.lower() == 'mqttpwd':
                        mqttpwd = value
                    elif key.lower() == 'mqtttopic':
                        mqtttopic = value

    if mqtthost and mqttusr and mqttpwd and mqtttopic:
        return mqtthost, mqttusr, mqttpwd, mqtttopic

    raise ValueError('MQTT environments not provided')


def mqtt_environment(env: XSenseBase, client, topic):

    for h_id, h in env.houses.items():
        topic_house = f'{topic}/{h.name}'
        client.publish(f'{topic_house}/id',f'{h_id}')            
        for s_id, s in h.stations.items():
            mqtt_device(s, s_id, client, topic_house)
            for d_id, d in s.devices.items():
                mqtt_device(d, d_id, client, topic_house)           

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected success")
    else:
        print(f"Connected fail with code {rc}")

def mqtt_device(d, d_id, client, topic):
    client.publish(f'{topic}/{s.name}/id',f'{d_id}')            
    client.publish(f'{topic}/{d.name}/serial',f'{d.sn}')
    client.publish(f'{topic}/{d.name}/online',f'{"yes" if d.online else "no"}')
    client.publish(f'{topic}/{d.name}/values',f'{d.data}')        
