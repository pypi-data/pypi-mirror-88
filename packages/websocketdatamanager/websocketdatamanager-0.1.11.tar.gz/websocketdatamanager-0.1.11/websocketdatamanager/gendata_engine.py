import math
import random
from datetime import datetime, timedelta
import pytz
import queue
import asyncio

class GenDataEngine:
    def __init__(self, *args, **kwargs):
        self.__queue_name = kwargs.get('queue_destiny')
        self.__status = False
        self.__base_gen = kwargs.get('base_gen',{})
        self.multi = kwargs.get('multiprocessing', False)

    @property
    def status(self):
        return self.__status

    def connect(self):
        return True

    async def getdata(self, queue_destiny, check):
        """
        Generate data
        and put on the queue
        """
        print("Queue destiny", queue_destiny)
        print(queue)
        print(asyncio.Queue)
        new_json = self.create_data()
        if isinstance(queue_destiny, queue.Queue):
            queue_destiny.put(new_json)
        elif isinstance(queue_destiny, asyncio.Queue):
            await queue_destiny.put(new_json)
        elif self.multi:
            queue_destiny.put(new_json)
        else:
            print("No enviado")
        return queue, True


    def create_data(self):
        data = {}
        for key, elem in self.__base_gen.items():
            if isinstance(elem, dict):
                data[key]={}
                for sec_key, fn in elem.items():
                    data[key][sec_key]=fn()
            else:
                data[key]=elem()
        return data



