import uuid
import asyncio

from xsense.async_xsense import AsyncXSense
from xsense.utils import dump_environment, get_credentials
from xsense.utils_mqtt import mqtt_environment, get_mqttenv, on_connect
from paho.mqtt import client as mqtt

async def run(username: str, password: str):
  
    client = mqtt.Client(client_id=str(uuid.uuid4()))
    mqtthost, mqttusr, mqttpwd, mqtttopic = get_mqttenv()
    client.username_pw_set(mqttusr,mqttpwd)  
    client.on_connect = on_connect
    client.connect(mqtthost, 1883, 60)
    client.loop_start()
  
    api = AsyncXSense()

  while True:
    await api.init()
    await api.login(username, password)
    await api.load_all()

    for _, h in api.houses.items():
        await api.get_house_state(h)
        for _, s in h.stations.items():
            await api.get_station_state(s)
            await api.get_state(s)

    dump_environment(api)
    mqtt_environment(api, client, mqtttopic)

#    client.loop_stop()
    time.sleep(1*60)
  
username, password = get_credentials()
asyncio.run(run(username, password))
