"""
Test django data test manager
"""
from asyncio import Queue
from networktools.ip import network_ip
from networktools.environment import get_env_variable
from web_dj_collector.manage import setup

"""
inputs:

queue_set
engine_opts
dj_opts

PARA QUE FUNCIONE:

copiar en la carpeta donde esta manage.py del proyecto django

"""

if __name__ == "__main__":
    setup()
    from websocketdatamanager.DjangoDataTestManager import DjangoDataTestManager
    # async queue
    # doc: https://docs.python.org/3.6/library/asyncio-queue.html
    queue2dj = Queue()
    queue2mq = Queue()
    # datos de conexión a la cola rmq
    # los datos de conexión adonde se envían
    djdm = DjangoDataTestManager({'status': queue2dj, 'status_recv': queue2mq},
                                 engine_opts, dj_opts, step=1, django=False)
    djdm.task_cycle()
