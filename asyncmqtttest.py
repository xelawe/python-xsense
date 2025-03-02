import asyncio

from xsense.async_xsense import AsyncXSense
from xsense.utils import dump_environment, get_credentials
from xsense.utils_mqtt import mqtt_environment, get_mqttenv
import paho.mqtt.client as mqtt

async def run(username: str, password: str):
    api = AsyncXSense()
    await api.init()
    await api.login(username, password)
    await api.load_all()

  

    for _, h in api.houses.items():
        await api.get_house_state(h)
        for _, s in h.stations.items():
            await api.get_station_state(s)
            await api.get_state(s)

    dump_environment(api)

    client = mqtt.Client()
    mqtthost, mqttusr, mqttpwd, mqtttopic = get_mqttenv()
    client.username_pw_set(mqttusr,mqttpwd)  
    mqtt_enwironment(api, client, mqtttopic)


username, password = get_credentials()
asyncio.run(run(username, password))
