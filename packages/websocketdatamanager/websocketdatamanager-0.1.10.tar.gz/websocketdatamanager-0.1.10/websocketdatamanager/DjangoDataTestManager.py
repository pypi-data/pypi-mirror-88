# Contrib csn:
from websocketdatamanager.gendata_engine import GenDataEngine
from data_amqp import AMQPData
from networktools.colorprint import gprint, bprint, rprint
from networktools.time import timestamp
from tasktools.taskloop import coromask, renew, simple_fargs, simple_fargs_out, TaskLoop
# Standar lib
import math
import codecs
import logging
import asyncio
import functools as fc
from basic_queuetools.queue import read_async_queue
from asgiref.sync import async_to_sync, sync_to_async
from channels.db import database_sync_to_async as dbaccess
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from multiprocessing import Pool
from web_dj_collector.manage import main
from pprint import pprint

# run django configs set
main()

from apps.station.models import InstallationEndPoint
from apps.status_unidad.models import LogUnidadGNSS

from datetime import datetime, timezone
import pytz

from asgiref.sync import sync_to_async
"""
Contrib
"""
import ujson as json
import os

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

"""
caching installations

"""
from networktools.colorprint import rprint, gprint, bprint
from pprint import pprint
from django.core.cache import cache
async def cache_installation(code):
    installation = cache.get(f"installation_{code}", None)
    print("Installation")
    pprint(installation)
    if not installation:
        query_installation = await dbaccess(InstallationEndPoint.objects.filter)(
            Q(activated=True) & Q(station__code=code))
        installation = await dbaccess(query_installation.first)()
        try:
            result = await sync_to_async(installation.to_json)()
            rprint(result)
            cache.set(f'installation_{code}', installation)
            ins = cache.get(f"installation_{code}",None)
            return result
        except Exception as ex:
            gprint("Excepcion al pasar a json")
            rprint(ex)
            gprint("Errrror in cache installation")
            raise ex
    else:
        bprint(f"==old insllation==< {type(installation)} >")
        result = await sync_to_async(installation.to_json)()
        return result


async def crear_nuevo_log(data):
    inst_pk = data.get('installation_ep')
    ins = await dbaccess(InstallationEndPoint.objects.get)(pk=inst_pk)
    data["installation_ep"] = ins
    gprint("==(0)==="*10)
    #bprint(str(ins))
    #pprint(data)
    gprint("====="*10)
    rprint("Saving LOG UNIDAD")
    try:
        print(data.keys())
        for elem,value in data.items():
            print(elem)
        log = LogUnidadGNSS(**data)
        print("Log->")
        print("Presave", "/")
        await dbaccess(log.save)()
        gprint(f"ID )> {log.pk}")
        rprint(log.installation_ep.station)
        gprint("=END===="*10)
    except Exception as excep:
        gprint("====="*10)
        bprint("Error on save data")
        print(excep)
        gprint("====="*10)
        raise excep
    return log

def save_log(log):
    log.save()

async def data_save(elem):
    log = await crear_nuevo_log(elem)
    return log
    
async def statusdata2log(station, **data):
    installation = None
    #breakpoint()
    try:
        installation = await cache_installation(station)
        if installation:
            dt_gen_time = data.get('BATT_MEM',data.get("DOP", {})).get('TIMESTAMP')
            this_time = datetime.fromtimestamp(dt_gen_time).astimezone(pytz.utc)
            data_log = {
                'installation_ep': installation.get("pk"),
                'dt_gen': this_time,
                'batt_cap': data.get('BATT_MEM',{}).get('BATT_CAPACITY', 0),
                'remaining_mem': data.get('BATT_MEM',{}).get('REMAINING_MEM', 0),
                'hdop': data.get('DOP',{}).get('HDOP', 20),
                'vdop': data.get('DOP',{}).get('VDOP', 20),
                'pdop': data.get('DOP',{}).get('PDOP', 20),
                'tdop': data.get('DOP',{}).get('TDOP', 20),
            }
            return data_log
    except AttributeError as ae:
        gprint("Error de atributo")
        print("No existe el atributo para el elemento", station, data, type(data), ae)
    except ObjectDoesNotExist as e:
        print("Error al cargar instalaciones", e)
        raise e


class DjangoDataTestManager:
    """
    This class pretends to create a knut in what receive data from RMQ queues and send directly to the objects form dj-collector on the database
    """

    def __init__(self, queue_set, engine_opts, dj_opts, step=0.1,
                 processes=2, *args, **kwargs):
        self.step = step
        self.queue_set = queue_set
        self.engine_opts = engine_opts
        self.dj_opts = dj_opts
        self.engine = False
        self.pool = Pool(processes=processes)
        self.django=kwargs.get('django', True)

    async def cycle_read_from_datagen(self, *args, **kwargs):
        engine = args[0]
        v = args[1]
        channels = args[2]
        print("Datagen new...", channels, "engine", engine)
        for channel, datagen in engine.items():
            try:

                queue = self.queue_set.get(channel)
                queue, active = await datagen.getdata(queue, True)
            except Exception as e:
                print("Error en cycle send to dj es->%s" % e)
                v = 0
                channels.add(channel)
        await asyncio.sleep(self.step)
        return [engine, v, channels], {}
 
    async def cycle_send_to_dj(self, *args, **kwargs):
        """
        Leer la cola que recibe de rmq
        Enviar cada dato recibido de la cola y cargarlo
        """
        queue = args[0]
        data = []
        await asyncio.sleep(1)
        try:
            #breakpoint()
            async for elem in read_async_queue(queue):
                # transformar elem para que sea guardable
                print("Elemem dict")
                pprint(elem, indent=2)
                if isinstance(elem, dict):
                    try:

                        data_log = await statusdata2log(**elem)
                        if data_log:
                            try:
                                data.append(data_log)
                            except Exception as e:
                                bprint("Creando lista de logs, error %s, LogUnidadGNSS create" % e)
                                raise e
                    except Exception as e:
                        print("Error al transformar elem %s" % e)
            if data and self.django:
                for elem in data:
                    await data_save(elem)
            elif not self.django:
                print("New data test")
                pprint(data)
        except Exception as e:
            print("Hubo una excepción al guardar los datos de LogGNSS")
            raise e
        data = []
        return args, kwargs

    def task_cycle(self):
        loop = asyncio.get_event_loop()
        tasks_list = []
        """
        RMQ Task
        """
        data_engine = {channel: GenDataEngine(**value_dict)
                      for channel, value_dict in self.engine_opts.items()}
        # se crea el conjunto de canales existentes
        channels = set(self.engine_opts.keys())
        # mq 2 ws
        # la args de rmq
        # se activa ciclo de lectura rmq

        cycle_rmq_args = [data_engine, 0, channels]
        task = TaskLoop(self.cycle_read_from_datagen,
                                    cycle_rmq_args, {},
                                    simple_fargs_out)
        task.create()
        tasks_list.append(task)


        # se activa ciclo de escritura dj, leyendo cola async
        queue_dj = self.queue_set.get('test')
        cycle_dj_args = [queue_dj]
        task = TaskLoop(self.cycle_send_to_dj,
                                    cycle_dj_args,{},
                                    simple_fargs_out)
        task.create()
        # se agrega a lista de tareas:
        tasks_list.append(task)

        if not loop.is_running():
            loop.run_forever()
