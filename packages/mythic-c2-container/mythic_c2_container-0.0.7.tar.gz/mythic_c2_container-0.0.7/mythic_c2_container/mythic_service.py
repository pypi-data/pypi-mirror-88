#!/usr/bin/env python3
import aio_pika
import os
import time
import sys
import subprocess
import _thread
import base64
import json
import socket
import asyncio
import pathlib
import traceback
from . import C2ProfileBase
from importlib import import_module, invalidate_caches
from functools import partial

credentials = None
connection_params = None
running = False
process = None
thread = None
hostname = ""
output = ""
exchange = None
container_files_path = None


def deal_with_stdout():
    global process
    global output
    while True:
        try:
            for line in iter(process.stdout.readline, b""):
                output += line.decode("utf-8")
        except Exception as e:
            print_flush("[-] Exiting thread due to: {}\n".format(str(e)))
            break


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


async def send_status(message="", routing_key=""):
    global exchange
    try:
        message_body = aio_pika.Message(message.encode())
        await exchange.publish(message_body, routing_key=routing_key)
    except Exception as e:
        print_flush("[-] Exception in send_status: {}".format(str(e)))


async def callback(message: aio_pika.IncomingMessage):
    global running
    global process
    global output
    global thread
    global hostname
    global container_files_path
    with message.process():
        # messages of the form: c2.modify.PROFILE NAME.command
        try:
            command = message.routing_key.split(".")[3]
            username = message.routing_key.split(".")[4]
            server_path = container_files_path / "server"
            # command = body.decode('utf-8')
            if command == "start":
                if not running:
                    # make sure to start the /Apfell/server in the background
                    os.chmod(server_path, mode=0o777)
                    output = ""
                    process = subprocess.Popen(
                        str(server_path),
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        cwd=str(container_files_path),
                    )
                    thread = _thread.start_new_thread(deal_with_stdout, ())
                    time.sleep(3)
                    process.poll()
                    if process.returncode is not None:
                        # this means something went wrong and the process is dead
                        running = False
                        await send_status(
                            message="Failed to start\nOutput: {}".format(output),
                            routing_key="c2.status.{}.stopped.start.{}".format(
                                hostname, username
                            ),
                        )
                        output = ""
                    else:
                        running = True
                        await send_status(
                            message="Started with pid: {}...\nOutput: {}".format(
                                str(process.pid), output
                            ),
                            routing_key="c2.status.{}.running.start.{}".format(
                                hostname, username
                            ),
                        )
                        output = ""
                else:
                    await send_status(
                        message="Already running...\nOutput: {}".format(output),
                        routing_key="c2.status.{}.running.start.{}".format(
                            hostname, username
                        ),
                    )
                    output = ""
            elif command == "stop":
                if running:
                    try:
                        process.kill()
                        process.communicate()
                    except Exception as e:
                        pass
                    try:
                        thread.exit()
                    except Exception as e:
                        pass
                    running = False
                    await send_status(
                        message="Process killed...\nOld Output: {}".format(output),
                        routing_key="c2.status.{}.stopped.stop.{}".format(
                            hostname, username
                        ),
                    )
                    output = ""
                else:
                    await send_status(
                        message="Process not running...\nOld Output: {}".format(output),
                        routing_key="c2.status.{}.stopped.stop.{}".format(
                            hostname, username
                        ),
                    )
                    output = ""
                # make sure to stop the /Apfell/server in the background
            elif command == "status":
                if running:
                    await send_status(
                        message="Output: {}".format(output),
                        routing_key="c2.status.{}.running.status.{}".format(
                            hostname, username
                        ),
                    )
                    output = ""
                else:
                    await send_status(
                        message="C2 is not running",
                        routing_key="c2.status.{}.stopped.status.{}".format(
                            hostname, username
                        ),
                    )
            elif command == "get_config":
                try:
                    path = container_files_path / "config.json"
                    file_data = open(path, "rb").read()
                except Exception as e:
                    file_data = b"File not found"
                encoded_data = json.dumps(
                    {
                        "filename": "config.json",
                        "data": base64.b64encode(file_data).decode("utf-8"),
                    }
                )
                await send_status(
                    message=encoded_data,
                    routing_key="c2.status.{}.{}.get_config.{}".format(
                        hostname, "running" if running else "stopped", username
                    ),
                )
            elif command == "writefile":
                try:
                    message = json.loads(message.body.decode("utf-8"))
                    file_path = container_files_path / message["file_path"]
                    file_path = file_path.resolve()
                    if container_files_path not in file_path.parents:
                        response = {
                            "status": "error",
                            "error": "trying to break out of path",
                        }
                    else:
                        file = open(file_path, "wb")
                        file.write(base64.b64decode(message["data"]))
                        file.close()
                        response = {"status": "success", "file": message["file_path"]}
                except Exception as e:
                    response = {"status": "error", "error": str(e)}
                await send_status(
                    message=json.dumps(response),
                    routing_key="c2.status.{}.{}.writefile.{}".format(
                        hostname, "running" if running else "stopped", username
                    ),
                )
            elif command == "sync_classes":
                try:
                    import_all_c2_functions()
                    # c2profile = {}
                    for cls in C2ProfileBase.C2Profile.__subclasses__():
                        c2profile = cls().to_json()
                        break
                    await send_status(
                        message=json.dumps(c2profile),
                        routing_key="c2.status.{}.{}.sync_classes.{}".format(
                            hostname, "running" if running else "stopped", username
                        ),
                    )
                except Exception as e:
                    await send_status(
                        message='{"message": "Error while syncing info: {}"}'.format(
                            str(traceback.format_exc())
                        ),
                        routing_key="c2.status.{}.{}.sync_classes.{}".format(
                            hostname, "running" if running else "stopped", username
                        ),
                    )
            else:
                print("Unknown command: {}".format(command))
                sys.stdout.flush()
        except Exception as e:
            print("Failed overall message processing: " + str(e))
            sys.stdout.flush()


async def sync_classes():
    global running
    try:
        import_all_c2_functions()
        c2profile = {}
        for cls in C2ProfileBase.C2Profile.__subclasses__():
            c2profile = cls().to_json()
            break
        await send_status(
            message=json.dumps(c2profile),
            routing_key="c2.status.{}.{}.sync_classes.{}".format(
                hostname, "running" if running else "stopped", ""
            ),
        )
    except Exception as e:
        await send_status(
            message='{"message": "Error while syncing info: {}"}'.format(
                str(traceback.format_exc())
            ),
            routing_key="c2.status.{}.{}.sync_classes.{}".format(
                hostname, "running" if running else "stopped", ""
            ),
        )


def print_flush(message: str):
    print(message)
    sys.stdout.flush()


async def rabbit_c2_rpc_callback(
    exchange: aio_pika.Exchange, message: aio_pika.IncomingMessage
):
    with message.process():
        request = json.loads(message.body.decode())
        if "action" in request:
            response = await globals()[request["action"]](request)
            response = json.dumps(response.to_json()).encode()
        else:
            response = json.dumps(
                {"status": "error", "error": "Missing action"}
            ).encode()
        try:
            await exchange.publish(
                aio_pika.Message(body=response, correlation_id=message.correlation_id),
                routing_key=message.reply_to,
            )
        except Exception as e:
            print_flush(
                "Exception trying to send message back to container for rpc! " + str(e)
            )


async def connect_and_consume_rpc(main_config: dict, debug):
    connection = None
    global hostname
    while connection is None:
        try:
            if debug:
                print_flush("Connecting to rabbitmq in connect_and_consume_rpc")
            connection = await aio_pika.connect_robust(
                host=main_config["host"],
                login=main_config["username"],
                password=main_config["password"],
                virtualhost=main_config["virtual_host"]
            )
            if debug:
                print_flush("Successfully connected in connect_and_consume_rpc")
        except (ConnectionError, ConnectionRefusedError) as c:
            print_flush("Connection to rabbitmq failed, trying again...")
        except Exception as e:
            print_flush("Exception in connect_and_consume_rpc connect: {}\n trying again...".format(str(e)))
        await asyncio.sleep(5)
    channel = await connection.channel()
    # get a random queue that only the apfell server will use to listen on to catch all heartbeats
    if debug:
        print_flush("Declaring container specific rpc queue in connect_and_consume_rpc")
    queue = await channel.declare_queue("{}_rpc_queue".format(hostname), auto_delete=True)
    await channel.set_qos(prefetch_count=10)
    try:
        if debug:
            print_flush("Starting to consume callbacks in connect_and_consume_rpc")
        task = queue.consume(
            partial(rabbit_c2_rpc_callback, channel.default_exchange)
        )
    except Exception as e:
        print_flush("Exception in connect_and_consume_rpc .consume: {}".format(str(e)))


async def mythic_service(debug: bool):
    global hostname
    global exchange
    global container_files_path
    connection = None
    config_file = open("rabbitmq_config.json", "rb")
    main_config = json.loads(config_file.read().decode("utf-8"))
    config_file.close()
    if main_config["name"] == "hostname":
        hostname = socket.gethostname()
    else:
        hostname = main_config["name"]
    container_files_path = pathlib.Path(
        os.path.abspath(main_config["container_files_path"])
    )
    container_files_path = container_files_path / "c2_code"
    while True:
        try:
            if debug:
                print_flush("Connecting to rabbitmq from mythic_service")
            connection = await aio_pika.connect_robust(
                host=main_config["host"],
                login=main_config["username"],
                password=main_config["password"],
                virtualhost=main_config["virtual_host"],
            )
            if debug:
                print_flush("Successfully connected to rabbitmq from mythic_service")
            try:
                channel = await connection.channel()
                if debug:
                    print_flush("Declaring exchange in mythic_service")
                exchange = await channel.declare_exchange(
                    "mythic_traffic", aio_pika.ExchangeType.TOPIC
                )
                if debug:
                    print_flush("Declaring queue in mythic_service")
                queue = await channel.declare_queue("", exclusive=True)
                await queue.bind(
                    exchange="mythic_traffic", routing_key="c2.modify.{}.#".format(hostname)
                )
                # just want to handle one message at a time so we can clean up and be ready
                await channel.set_qos(prefetch_count=30)
                if debug:
                    print_flush("Creating task to consume in mythic_service")
                task = queue.consume(callback)
                await sync_classes()
                print("Listening for c2.modify.{}.#".format(hostname))
                if debug:
                    print_flush("Creating task for connect_and_consume_rpc from mythic_service")
                task4 = asyncio.ensure_future(connect_and_consume_rpc(main_config, debug))
                if debug:
                    print_flush("Waiting for all tasks to finish in mythic_service")
                result = await asyncio.gather(task, task4)
                if debug:
                    print_flush("All tasks finished in mythic_service, repeating loop")
            except Exception as e:
                print_flush("Exception in mythic_service: " + str(traceback.format_exc()))
        except (ConnectionError, ConnectionRefusedError) as c:
            print_flush("Connection to rabbitmq failed, trying again...")
        except Exception as e:
            print_flush("Exception in mythic_service: " + str(traceback.format_exc()))
        await asyncio.sleep(5)
    


async def heartbeat_loop(debug: bool):
    config_file = open("rabbitmq_config.json", "rb")
    main_config = json.loads(config_file.read().decode("utf-8"))
    config_file.close()
    if main_config["name"] == "hostname":
        hostname = socket.gethostname()
    else:
        hostname = main_config["name"]
    while True:
        try:
            if debug:
                print_flush("Connecting to rabbitmq from heartbeat_loop")
            connection = await aio_pika.connect_robust(
                host=main_config["host"],
                login=main_config["username"],
                password=main_config["password"],
                virtualhost=main_config["virtual_host"],
            )
            if debug:
                print_flush("Successfully connected to rabbitmq from heartbeat_loop")
            channel = await connection.channel()
            if debug:
                print_flush("Declaring exchange in heartbeat_loop for channel")
            exchange = await channel.declare_exchange(
                "mythic_traffic", aio_pika.ExchangeType.TOPIC
            )
        except (ConnectionError, ConnectionRefusedError) as c:
            print_flush("Connection to rabbitmq failed, trying again...")
            await asyncio.sleep(5)
            continue
        except Exception as e:
            print_flush("Exception in heartbeat_loop: " + str(traceback.format_exc()))
            await asyncio.sleep(5)
            continue
        while True:
            try:
                # routing key is ignored for fanout, it'll go to anybody that's listening, which will only be the server
                if debug:
                    print_flush("Sending heartbeat in heartbeat_loop")
                await exchange.publish(
                    aio_pika.Message("heartbeat".encode()),
                    routing_key="c2.heartbeat.{}".format(hostname),
                )
                await asyncio.sleep(10)
            except Exception as e:
                print_flush("Exception in heartbeat_loop trying to send heartbeat: " + str(e))
                # if we get an exception here, break out to the bigger loop and try to connect again
                break

# start our service
def start_service_and_heartbeat(debug=False):
    loop = asyncio.get_event_loop()
    loop.create_task(mythic_service(debug))
    loop.create_task(heartbeat_loop(debug))
    loop.run_forever()
