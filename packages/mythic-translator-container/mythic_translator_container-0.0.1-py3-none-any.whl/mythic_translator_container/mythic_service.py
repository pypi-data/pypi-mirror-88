#!/usr/bin/env python3
import aio_pika
import sys
import json
import socket
import asyncio
import pathlib
from importlib import import_module, invalidate_caches
from functools import partial

credentials = None
connection_params = None
hostname = ""
exchange = None


def import_all_c2_functions():
    import glob

    # Get file paths of all modules.
    modules = glob.glob("c2_functions/*.py")
    invalidate_caches()
    for x in modules:
        if not x.endswith("__init__.py") and x[-3:] == ".py":
            module = import_module("c2_functions." + pathlib.Path(x).stem, package=None)
            for el in dir(module):
                if "__" not in el:
                    globals()[el] = getattr(module, el)


async def rabbit_c2_rpc_callback(
    exchange: aio_pika.Exchange, message: aio_pika.IncomingMessage
):
    with message.process():
        try:
            request = json.loads(message.body.decode())
            response = await globals()[request["action"]](request)
            if request["action"] == "translate_from_c2_format":
                response = json.dumps(response).encode()
        except Exception as e:
            print(str(e))
            sys.stdout.flush()
            response = b""
        try:
            await exchange.publish(
                aio_pika.Message(body=response, correlation_id=message.correlation_id),
                routing_key=message.reply_to,
            )
        except Exception as e:
            print(
                "[-] Exception trying to send message back to container for rpc! " + str(e)
            )
            sys.stdout.flush()


async def mythic_service():
    global hostname
    global exchange
    connection = None
    config_file = open("rabbitmq_config.json", "rb")
    main_config = json.loads(config_file.read().decode("utf-8"))
    config_file.close()
    if main_config["name"] == "hostname":
        hostname = socket.gethostname()
    else:
        hostname = main_config["name"]
    import_all_c2_functions()
    while connection is None:
        try:
            connection = await aio_pika.connect_robust(
                host=main_config["host"],
                login=main_config["username"],
                password=main_config["password"],
                virtualhost=main_config["virtual_host"],
            )
            channel = await connection.channel()
            # get a random queue that only the apfell server will use to listen on to catch all heartbeats
            queue = await channel.declare_queue("{}_rpc_queue".format(hostname), auto_delete=True)
            await channel.set_qos(prefetch_count=50)
            try:
                task = queue.consume(
                    partial(rabbit_c2_rpc_callback, channel.default_exchange)
                )
                result = await asyncio.wait_for(task, None)
            except Exception as e:
                print("[-] Exception in connect_and_consume .consume: {}\n trying again...".format(str(e)))
                sys.stdout.flush()
        except (ConnectionError, ConnectionRefusedError) as c:
            print("[-] Connection to rabbitmq failed, trying again...")
            sys.stdout.flush()
        except Exception as e:
            print("[-] Exception in connect_and_consume_rpc connect: {}\n trying again...".format(str(e)))
            # print("Exception in connect_and_consume connect: {}".format(str(e)))
            sys.stdout.flush()
        await asyncio.sleep(2)

def start_service():
    # start our service
    loop = asyncio.get_event_loop()
    loop.create_task(mythic_service())
    loop.run_forever()
