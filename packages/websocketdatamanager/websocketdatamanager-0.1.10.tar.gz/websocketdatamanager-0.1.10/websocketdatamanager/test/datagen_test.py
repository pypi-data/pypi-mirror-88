import asyncio
import random
from datetime import datetime

from websocketdatamanager.gendata_engine import GenDataEngine

stations = ["CADC","PERN", "QLCQ", "UTIN"]


base_gen = {
    'station': lambda : random.choice(stations),
    'BATT_MEM':{
        'TIMESTAMP': lambda : datetime.now().timestamp(),
        "BATT_CAPACITY": lambda: random.randint(0,100),
        "REMAINING_MEM": lambda: random.randint(0,100),
    },
    'DOP':{
        "HDOP": lambda:random.randint(0,20),
        "VDOP": lambda:random.randint(0,20),
        "PDOP": lambda:random.randint(0,20),
        "TDOP": lambda:random.randint(0,20)
    }
}

def new_data():
    data = {}
    for key, elem in base_gen.items():
        if isinstance(elem, dict):
            data[key]={}
            for sec_key, fn in elem.items():
                data[key][sec_key]=fn()
        else:
            data[key]=elem()
    return data


queue = asyncio.Queue()
gendata =  GenDataEngine(base_gen=base_gen, queue_destiny=queue)

new_data = gendata.create_data()
print(new_data)
