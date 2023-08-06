import socket
from datetime import datetime, date
from networktools.path import home_path
import asyncio
from asyncio import wait_for, shield
from pathlib import Path
# NetworkTools methods and classes:
from data_rdb import Rethink_DBS
from data_geo import GeoJSONData
from data_amqp import AMQPData

from networktools.library import my_random_string, check_gsof
from networktools.colorprint import gprint, bprint, rprint
from networktools.geo import (radius, deg2rad, ecef2llh, llh2ecef)
from networktools.time import get_datetime_di
from networktools.library import geojson2json

# log module
from basic_logtools.filelog import LogFile

# TaskTools for concurrency loop
from tasktools.taskloop import TaskLoop
from tasktools.scheduler import TaskScheduler

# Async Socket
# from gnsocket.gn_socket import GNCSocket

# Maths
import time
from multiprocessing import Lock
import json

# RethinkDB module
from rethinkdb import RethinkDB
rdb = RethinkDB()
rdb.set_loop_type('asyncio')


def default(o):
    if isinstance(o, (date, datetime)):
        return o.isoformat()


def qjson(x):
    return json.loads(json.dumps(x, sort_keys=True, indent=1, default=default))


class DragonGather(TaskScheduler):
    log_manager: dict = {}

    def __init__(self, queue_list, *args, **kwargs):
        # super().__init__()

        self.key = 'DT_GEN'
        self.ipt = kwargs.get('ipt')
        self.ico = kwargs.get('ico')
        self.process_queue = kwargs.get('process_queue')
        self.gui_queue = kwargs.get('gui_queue')
        self.proc_tasks = kwargs.get("proc_tasks")
        self.queue_client_n2t = kwargs.get("queue_client_n2t")
        self.queue_client_t2n = kwargs.get("queue_client_t2n")
        self.queue2client = kwargs.get("queue2client")
        self.stations = kwargs.get("stations")
        self.position = kwargs.get("position")
        self.db_data = kwargs.get("db_data")
        self.lnproc = kwargs.get("nproc")
        self.sta_init = kwargs.get("sta_init")
        self.bridge = kwargs.get("bridge")
        self.common = kwargs.get("common")
        self.rethinkdb_address = kwargs.get('rdb_address')
        self.rethinkdb_enu_address = kwargs.get('rdb_enu_address')
        self.rethinkdb_dbname = kwargs.get('rdb_dbname', 'test')
        self.sta_init = kwargs.get('status_tasks')
        self.status_tasks = kwargs.get('status_tasks')
        self.assigned_tasks = kwargs.get('assigned_tasks')
        self.group = kwargs.get('group')
        self.gui_group = kwargs.get('gui_group')
        self.gui_set = kwargs.get('gui_set')
        self.signals = kwargs.get('signals')
        self.isg = kwargs.get('isg')
        self.sigid = kwargs.get('sigid')
        self.sc = kwargs.get('send_control')
        self.dbus_queue = kwargs.get('dbus_queue')
        self.dbus_geojson_queue = kwargs.get('dbus_geojson_queue')
        self.status_keys = kwargs.get('status_keys', {'BATT_MEM', 'DOP'})
        args = []
        # call superior class
        super().__init__(*args, **kwargs)
        #
        self.enqueued = kwargs.get('enqueued')
        self.rq = queue_list[0]
        self.wq = queue_list[1]
        self.queue_list = queue_list
        self.start = 0
        self.signal = None
        self.origin_objects = {"RethinkDB": Rethink_DBS}
        self.rethinkdb = None
        self.rethinkdb_origin = {}
        self.rethinkdb_origin_enu = {}
        self.lock = None
        self.msg_process = dict(GET_LST={
            'STATION': self.load_stations,
            'DBDATA': self.load_dbdata
        })
        self.msg_server_process = dict(GET_STA=self.get_sta)

        coros_callback_dict = {
            'run_task': self.gather_data,
        }
        self.set_new_run_task(**coros_callback_dict)
        self.log_path = Path(home_path(kwargs.get('log_path', '~/log')))

    @property
    def class_name(self):
        return self.__class__.__name__

    def set_isg(self, uin=4):
        """
        Defines a new id for task related to collect data insice a worker,
        check if exists
        """
        isg = my_random_string(uin)
        while True:
            if isg not in self.isg:
                self.isg.append(isg)
                break
            else:
                isg = my_random_string(uin)
        return isg

    def msg_network_task(self):
        # get from queue status from SOCKET
        # send result
        # read_queue -> rq
        # process msg -> f(msg)
        queue_list = [self.rq, self.wq]
        loop = asyncio.get_event_loop()
        self.load_data_task(loop)
        # gprint("XDX Gestionando mensajes en engine", flush=True)
        try:
            args = []
            # Create instances

            task_client = TaskLoop(self.check_client_status, args, {},
                                   **{"name": "check_client_status"})

            task = TaskLoop(self.check_status, args, {},
                            **{"name": "check_status"})

            task_client.create()
            task.create()

            if not loop.is_running():
                loop.run_forever()
        except Exception as ex:
            print("Error o exception que se levanta con %s" %
                  format(queue_list))
            print(ex)
            raise ex

    async def check_client_status(self, *args, **kwargs):
        q2client = self.queue2client
        wq = self.queue_client_n2t
        rq = self.queue_client_t2n
        await asyncio.sleep(.5)
        try:
            # first read the msgs from system and send to client
            # check if is dict
            # check if has the main keys....(?)
            if not q2client.empty():
                for i in range(q2client.qsize()):
                    msg = q2client.get()
                    if isinstance(msg, dict):
                        wq.put(msg)
            # read the queue that receive the data on client
            # process the msg
            # do something...
            if not rq.empty():
                for i in range(rq.qsize()):
                    msg = rq.get()
                    result = await self.client_interpreter(msg)
                    rprint("Resultado recibido de client:%s" % result)
                    """
                    if not None:
                        wq.put({'msg': result,
                                'idc': idc})
                    """
            # bprint(self.instances.keys())
        except Exception as ex:
            print(ex)
            raise ex
        return args, kwargs

    async def client_interpreter(self, msg_in):
        # msg is a string JSON
        self.lock = Lock()
        result = []
        msg = msg_in.get('dt').get('msg')
        if isinstance(msg, dict):
            command = msg.get('command').get('action')
            answer = msg.get('command').get('answer')
            result = {}
            if command in self.msg_process and answer:
                varname = msg.get('command').get('varname')

                def print_dict(x):
                    return [print("%s->%s" % (k, v) for k, v in x.items())]

                msg_process = self.msg_process.get(command, {}).get(
                    varname, print_dict)
                result = msg_process(answer)
        return result

    async def check_status(self, *args, **kwargs):
        wq = self.queue_list[0]
        rq = self.queue_list[1]
        await asyncio.sleep(.5)
        try:
            if not rq.empty():
                for i in range(rq.qsize()):
                    msg = rq.get()
                    try:
                        m = msg.get('dt')
                        idc = msg.get('idc')
                        result = await self.interpreter(m)
                        if result:
                            wq.put({'msg': result, 'idc': idc})
                    except Exception as ex:
                        print("Error al transformar")
                        print(ex)
                        print(msg)
                        print(type(msg))
                        raise ex
            # bprint(self.instances.keys())
        except Exception as ex:
            print(ex)
            raise ex
        return args, kwargs

    async def interpreter(self, msg):
        # msg is a string JSON
        self.lock = Lock()
        command = msg.get('command', 'GET_STA')
        args = msg.get('args', [])
        result = None
        if command == 'init_gui':
            # if self.gui_group empty:
            if not self.gui_group:
                with self.lock:
                    self.sc.value = not self.sc.value
            # add group and id
            idg = args[0]
            group = args[1]
            # relationship between a gui and a group of stations
            self.gui_group.update({idg: group})

        if command in self.msg_server_process:
            result = self.msg_server_process.get(command)(*args)
        return result

    def get_sta(self, *answer):
        stations = self.stations
        # gprint("XDX stations keys : %s" %stations.keys())
        for ids in stations.keys():
            # bprint("XDX Cargando data a process")
            dataset = stations[ids]
            try:
                if dataset.get('code') in self.group or 'ALL' in self.group:
                    # if self.sc.value:
                    self.dbus_queue.put({
                        'command': 'station',
                        'data': {
                            ids: self.stations[ids]
                        }
                    })
                    self.dbus_queue.put({
                        'command': 'position',
                        'data': {
                            ids: self.position[ids]
                        }
                    })
                    self.gui_set.append(dataset['code'])
                    # print("XDX .sds", flush=True)

                # gprint(self.queue_process.qsize())
            except Exception as exc:
                print("Error al cargar ids a queue")
                raise exc
        self.dbus_queue.put({
            'channel': 'data',
            'command': 'load_chart',
            'data': []
        })
        return json.dumps({
            'channel': 'data',
            'command': 'GET_STA',
            'args': ['dbus']
        })

    def add_process_queue(self, process_queue):
        self.process_queue = process_queue

    def load_stations(self, msg):
        qs = msg
        POSITION = dict()
        for ids in qs:
            qs[ids]['STATUS'] = 'OFF'
            POSITION[ids] = dict()
            POSITION[ids]['ECEF'] = dict()
        for ids in qs:
            self.stations[ids] = qs.get(ids)
            print("Station", qs.get(ids))
            if 'ECEF_Z' in qs[ids]:
                Z = qs[ids]['ECEF_Z']
                POSITION[ids]['ECEF'].update({'Z': Z})
            if 'ECEF_X' in qs[ids]:
                X = qs[ids]['ECEF_X']
                POSITION[ids]['ECEF'].update({'X': X})
            if 'ECEF_Y' in qs[ids]:
                Y = qs[ids]['ECEF_Y']
                POSITION[ids]['ECEF'].update({'Y': Y})
            if 'position' in qs[ids]:
                pst = json.loads(qs[ids]['position'])
                coords = pst['coordinates']
                [lat, lon] = deg2rad(*coords)
                POSITION[ids].update({'lat': lat})
                POSITION[ids].update({'lon': lon})
                POSITION[ids].update({'radius': radius(lat)[0]})
                XYZ = llh2ecef(lat, lon, Z)
                # bprint(XYZ) ok, correct
                POSITION[ids].update({'ECEF': dict(zip(['X', 'Y', 'Z'], XYZ))})
            x = POSITION[ids]['ECEF']['X']
            y = POSITION[ids]['ECEF']['Y']
            z = POSITION[ids]['ECEF']['Z']
            (lat, lon, h) = ecef2llh(x, y, z)
            POSITION[ids].update({'llh': {'lat': lat, 'lon': lon, 'z': h}})
            self.position[ids] = POSITION[ids]
            if 'code' in qs:
                self.common[qs][ids] = dict()
            dataset = self.stations.get(ids)
            # code = dataset.get('code')
            self.process_queue.put(ids)
            self.enqueued.append(ids)
            self.gui_set.append(dataset['code'])
            for k, s in self.stations.items():
                bprint(f"{k} : {s}")

    def load_dbdata(self, msg):
        for k, v in msg.items():
            self.db_data[k] = v

    def msg_load_stations(self):
        get_lst = {
            'user': 'admin',
            'group': 'admin',
            'command': {
                'action': 'GET_LST',
                'varname': 'STATION'
            }
        }
        return get_lst

    def msg_load_dbdata(self):
        get_lst = {
            'user': 'admin',
            'group': 'admin',
            'command': {
                'action': 'GET_LST',
                'varname': 'DBDATA'
            }
        }
        return get_lst

    def init_datawork_data(self):
        rprint("Inicializando datawork data")
        msg_list = [self.msg_load_stations(), self.msg_load_dbdata()]
        for msg in msg_list:
            print("Mensaje ->", msg)
            self.queue2client.put(msg)

    def activate_stations(self, stations):
        for ids in stations.keys():
            dataset = stations.get(ids)
            self.activate_station(dataset, ids)

    def activate_station(self, dataset, ids):
        try:
            if dataset['code'] in self.group:
                self.process_queue.put(ids)
                self.gui_set.append(dataset['code'])
        except Exception as exc:
            print("Error al cargar ids a queue")
            raise exc

    async def load_data(self, *args, **kwargs):
        """
        Load main data at the beggining
        In the future, must handle messages betwen
        DragonDataWork and Collector

        """
        if self.start == 0:
            print("Enviando msg inicial")
            self.init_datawork_data()
            self.start = 1
            ###
        else:
            await asyncio.sleep(25)
        return args, kwargs

    def load_data_task(self, loop):
        # bprint("Load data task")
        args = []
        task = TaskLoop(self.load_data, args, {}, **{"name": "load_data_task"})
        task.create()

    def add_sta_instance_origin(self, ids, loop):
        # create bridge instance
        # bprint("Station %s and port %s" % (self.stations[ids]['code'], self.bridge))
        # gprint("Bridge: %s" % format(self.bridge))
        # local_port = self.create_bridge(ids)
        # rprint("Local port %s" %local_port)
        code = self.stations[ids]['code']
        code_db = self.stations[ids]['db']
        # idd = self.get_id_by_code('DBDATA', code_db)
        # bprint("The db_data's id: %s" % idd)
        db_datos = dict(host='localhost',
                        name="Source_%s" % code_db,
                        code=code_db,
                        port=self.rethinkdb_address[1],
                        address=self.rethinkdb_address,
                        dbname=self.rethinkdb_dbname,
                        io_loop=loop,
                        log_path=str(self.log_path / "source_rdb"),
                        env='gather_%s' % code)
        name = 'RethinkDB'
        self.sta_init[ids] = True
        if name == 'RethinkDB':
            self.rethinkdb_origin[ids] = True
        try:
            RDB_C = self.origin_objects[name]
            rethinkdb_c = RDB_C(**db_datos)
            return rethinkdb_c
        except Exception as ex:
            print("Error al inicializar conexión %s" % ex)
            raise ex

    def add_sta_instance_destiny(self, ids, loop):
        # create bridge instance
        # bprint("Station %s and port %s" % (self.stations[ids]['code'], self.bridge))
        # gprint("Bridge: %s" % format(self.bridge))
        # local_port = self.create_bridge(ids)
        # rprint("Local port %s" %local_port)
        code = self.stations[ids]['code']
        code_db = self.stations[ids]['db']
        # idd = self.get_id_by_code('DBDATA', code_db)
        # bprint("The db_data's id: %s" % idd)
        db_datos_enu = dict(host='localhost',
                            name="Destiny_enu",
                            code=code_db,
                            port=self.rethinkdb_enu_address[1],
                            address=self.rethinkdb_enu_address,
                            dbname='enu_data',
                            io_loop=loop,
                            log_path=str(self.log_path / "enu_rdb"),
                            env='enu_%s' % code)

        name = 'RethinkDB'
        self.sta_init[ids] = True
        if name == 'RethinkDB':
            self.rethinkdb_origin_enu[ids] = True
        try:
            RDB_C = self.origin_objects[name]
            rethinkdb_c_enu = RDB_C(**db_datos_enu)
            return rethinkdb_c_enu
        except Exception as ex:
            print("Error al inicializar conexión %s" % ex)
            raise ex

        # self.common[code] = dict()

    # CREATE QUEUE INSTANCES

    # GET DATA AND SEND TO PLOT
    #
    #

    def add_process_instance(self, ids):
        CODE = self.stations[ids]['protocol'].upper()
        station = self.stations[ids]['code']
        kwargs = dict()
        kwargs['code'] = CODE
        kwargs['station'] = self.stations[ids]
        kwargs['position'] = self.position[ids]
        kwargs['log_path'] = str(self.log_path / 'geo_json_data')
        process_instance = GeoJSONData(**kwargs)
        return process_instance

    async def gather_data(self, ipt, ids, *args, **kwargs):
        """
        This method it's maybe the most important because generate
        the instances and gather the data in a general loop

        The logging system is a task by process
        """
        # input : ids, loop, sta
        uin = 3
        idi = my_random_string(uin)
        loop = asyncio.get_event_loop()
        v = int(args[0])
        sta = args[1]
        di, control, (rc, rc_enu), process_data = sta
        sta_init_flag = self.sta_init.get(ids)
        code = self.stations[ids]['code']
        code_db = self.stations[ids]['db']
        start_rdb_rc = kwargs.get('start_rdb_rc')
        start_rdb_rc_enu = kwargs.get('start_rdb_rc_enu')
        log = kwargs.get('log')
        await asyncio.sleep(.5)
        """
        Objetos centrales, de operacion
        """
        body, origin, destiny = False, False, False
        cursor = []
        control_rc = list(map(kwargs.get, ["init_rc", "init_rc_enu"]))
        if not sta_init_flag:
            # para controlar que?
            control = None
            # punto de inicio a consultar
            di = rdb.iso8601(get_datetime_di(delta=30))
            # el operador o procesador de la info
            process_data = self.add_process_instance(ids)
            self.sta_init[ids] = True
            body = True

        if start_rdb_rc:
            rc = self.add_sta_instance_origin(ids, loop)
            kwargs["start_rdb_rc"] = False
            kwargs["init_rc"] = True

        if start_rdb_rc_enu:
            rc_enu = self.add_sta_instance_destiny(ids, loop)
            kwargs["start_rdb_rc_enu"] = False
            kwargs["init_rc_enu"] = True
        """
        Iniciar objeto database fuente
        """
        if kwargs.get("init_rc"):
            # las dos instancias a dbs rethinkdb
            # rc: origen
            # rec_enu: destino
            try:
                kwargs["step"] = "CREATE_RC"
                idex = my_random_string(uin)
                await shield(wait_for(rc.async_connect(), timeout=120))
                rc.set_defaultdb(self.rethinkdb_dbname)
                await rc.list_dbs()
                await rc.select_db(self.rethinkdb_dbname)
                table_name = self.stations[ids]['db']  # created on datawork
                indexes = await rc.get_indexes(table_name)
                rprint(
                    f"Obteniendo indexes  {code_db}, {table_name}, indices {indexes}"
                )
                await rc.list_tables(rc.default_db)
                origin = True
                bprint(
                    f"Continuando a etapa siguiente, desde CREAR RDB RC, {code_db}"
                )
                kwargs["init_rc"] = False
            except asyncio.CancelledError as ce:
                bprint("CancelledError...RC_00")
                idex = my_random_string(uin)
                kwargs["origin_exception"] = f'''PD_TOA_-2 + {idex} + {code} +
                {ce}, ConnectionClosed rc_enu connection....'''
                log.exception(kwargs["origin_exception"])
                kwargs["init_rc"] = True
                await rc.close()
                return [
                    ipt, ids, v, [di, control, (rc, rc_enu), process_data]
                ], kwargs

            except (socket.error, ConnectionResetError,
                    ConnectionAbortedError) as conn_error:
                bprint("CancelledError...RC_01")
                idex = my_random_string(uin)
                kwargs["origin_exception"] = f'''PD_TOA_-1 + {idex} + {code} +
                {conn_error}, ConnectionClosed rc_enu connection....'''
                log.exception(kwargs["origin_exception"])
                kwargs["init_rc"] = True
                await rc.close()
                bprint(kwargs)
                return [
                    ipt, ids, v, [di, control, (rc, rc_enu), process_data]
                ], kwargs

            except asyncio.TimeoutError as e:
                bprint(f"CancelledError...RC_02->{e}")
                idex = my_random_string(uin)
                kwargs[
                    "origin_exception"] = f"PD_TO1_00 + {idex} + {code} + {e}"
                log.exception(kwargs["origin_exception"])
                kwargs["init_rc"] = True
                await rc.close()
                return [
                    ipt, ids, v, [di, control, (rc, rc_enu), process_data]
                ], kwargs

            except Exception as e:
                bprint(f"CancelledError...RC_03 -> {e}")
                kwargs["init_rc"] = True
                await rc.close()
                return [
                    ipt, ids, v, [di, control, (rc, rc_enu), process_data]
                ], kwargs
        """
        Iniciar objeto database destino
        """
        if kwargs.get('init_rc_enu'):
            # las dos instancias a dbs rethinkdb
            # rc: origen
            # rec_enu: destino
            try:
                kwargs["step"] = "CREATE_RC_ENU"
                idex = my_random_string(uin)
                await shield(wait_for(rc_enu.async_connect(), timeout=60))
                await rc_enu.list_dbs()
                await rc_enu.select_db('enu_data')
                table_name = self.stations[ids]['db']  # created on datawork
                await rc_enu.create_table(table_name, rc_enu.default_db)
                indexes = await rc_enu.get_indexes(table_name)
                if 'DT_GEN' not in indexes:
                    await rc_enu.create_index(table_name, index='DT_GEN')
                indexes = await rc_enu.get_indexes(table_name)
                await rc_enu.list_tables(rc_enu.default_db)
                destiny = True
                kwargs["init_rc_enu"] = False
            except asyncio.CancelledError as ce:
                idex = my_random_string(uin)
                kwargs["origin_exception"] = f'''PD_TOB_-2 + {idex} + {code} +
                {ce}, ConnectionClosed rc_enu connection....'''
                log.exception(kwargs["origin_exception"])
                kwargs["init_rc_enu"] = True
                bprint(kwargs)
                return [
                    ipt, ids, v, [di, control, (rc, rc_enu), process_data]
                ], kwargs

            except (socket.error, ConnectionResetError,
                    ConnectionAbortedError) as conn_error:
                idex = my_random_string(uin)
                kwargs["origin_exception"] = f'''PD_TOB_-1 + {idex} + {code} +
                {conn_error}, ConnectionClosed rc_enu connection....'''
                log.exception(kwargs["origin_exception"])
                kwargs["init_rc_enu"] = True
                bprint(kwargs)
                return [
                    ipt, ids, v, [di, control, (rc, rc_enu), process_data]
                ], kwargs

            except asyncio.TimeoutError as e:
                idex = my_random_string(uin)
                kwargs["origin_exception"] = f"PD_TO1_00 + {code} + {e}"
                log.exception(kwargs["origin_exception"])
                kwargs["init_rc_enu"] = True
                bprint(kwargs)
                return [
                    ipt, ids, v, [di, control, (rc, rc_enu), process_data]
                ], kwargs

        if body or origin or destiny:
            v = 2
            wargs = [ipt, ids, v, [di, control, (rc, rc_enu), process_data]]
        elif sta_init_flag:
            code = self.stations[ids]['code']
            table_name = self.stations[ids]['db']
            key = self.key
            try:
                kwargs["step"] = "GET_DATA_FROM_RC"
                df = rdb.iso8601(get_datetime_di(delta=0))  # now
                filter_opt = {'left_bound': 'open', 'index': key}
                cursor = await wait_for(rc.get_data_filter(
                    table_name, [di, df], filter_opt, key),
                                        timeout=120)
            except asyncio.CancelledError as ce:
                idex = my_random_string(uin)
                kwargs["origin_exception"] = f'''PD_TOA_-2 + {idex} + {code} +
                {ce}, ConnectionClosed rc_enu connection....'''
                log.exception(kwargs["origin_exception"])
                self.rethinkdb_origin[ids] = False
                bprint(kwargs)
                return [
                    ipt, ids, v, [di, control, (rc, rc_enu), process_data]
                ], kwargs

            except (socket.error, ConnectionResetError,
                    ConnectionAbortedError) as conn_error:
                idex = my_random_string(uin)
                kwargs["origin_exception"] = f'''PD_TO3_-1 + {idex} + {code} +
                {conn_error}, ConnectionClosed rc connection....'''
                log.exception(kwargs["origin_exception"])
                kwargs["init_rc"] = True
                bprint(kwargs)
                return [
                    ipt, ids, v, [di, control, (rc, rc_enu), process_data]
                ], kwargs

            except asyncio.TimeoutError as e:
                idex = my_random_string(uin)
                kwargs[
                    "origin_exception"] = f"PD_TO3_00 + {idex} + {code} + {e}"
                log.exception(kwargs["origin_exception"])
                kwargs["init_rc"] = True
                bprint(kwargs)
                return [
                    ipt, ids, v, [di, control, (rc, rc_enu), process_data]
                ], kwargs

            except Exception as ex:
                idex = my_random_string(uin)
                print(
                    f"IDEX {idex} Exception {ex}, table {table_name}, cursor={cursor}"
                )
                print("Error en obtención de data desde rethinkdb")
                bprint(
                    f"IDEX {idex}, table_name {table_name}, di {di}, df {df}, opts {filter_opt}"
                )
                rc.logerror(
                    f'''IDEX = {idex}, Error en la obtención de datos para
                    estación {code} en {ex}''')
                kwargs[
                    "origin_exception"] = f"PD_TO4_00 + {code} + {idex} + {ex}"
                log.exception(kwargs["origin_exception"])
                kwargs["init_rc"] = True
                return [
                    ipt, ids, v, [di, control, (rc, rc_enu), process_data]
                ], kwargs

            # signal.message({"msg":"cursor len %s" %len(cursor)})
            list_ok = []
            element = None
            #counter = 0
            for c in cursor:
                if check_gsof(c):
                    element = c
                    kwargs["step"] = "SAVE_DATA_TO_RC_ENU"
                    try:
                        this_dt = c.get("DT_GEN")
                        result = process_data.manage_data(c)
                        # to_plot = geojson2json(result)
                        to_db = geojson2json(result, destiny='db')
                        # result_enu =
                        try:
                            # rprint(
                            #    f"Saving {table_name}, dt {this_dt}, count {counter}"
                            # )
                            #bprint(f"To db {to_db}")
                            await wait_for(rc_enu.save_data(table_name, to_db),
                                           timeout=10)
                            await asyncio.sleep(.01)
                            #counter += 1
                        except asyncio.InvalidStateError as inv_e:
                            idex = my_random_string(uin)
                            kwargs[
                                "origin_exception"] = f'''PD_TO3_-3 + {idex} + {code} +
                            {inv_e}, InvalidStateError....'''
                            log.exception(kwargs["origin_exception"])
                            self.rethinkdb_origin_enu[ids] = False
                            kwargs["init_rc_enu"] = True
                            await rc_enu.close()
                            bprint(kwargs)
                            return [
                                ipt, ids, v,
                                [di, control, (rc, rc_enu), process_data]
                            ], kwargs

                        except asyncio.CancelledError as ce:
                            idex = my_random_string(uin)
                            kwargs[
                                "origin_exception"] = f'''PD_TO3_-2 + {idex} + {code} +
                            {ce}, ConnectionClosed rc_enu connection....'''
                            log.exception(kwargs["origin_exception"])
                            self.rethinkdb_origin_enu[ids] = False
                            kwargs["init_rc_enu"] = True
                            await rc_enu.close()
                            bprint(kwargs)
                            return [
                                ipt, ids, v,
                                [di, control, (rc, rc_enu), process_data]
                            ], kwargs

                        except (socket.error, ConnectionResetError,
                                ConnectionAbortedError) as conn_error:
                            idex = my_random_string(uin)
                            kwargs[
                                "origin_exception"] = f'''PD_TO3_-1 + {idex} + {code} + {conn_error}, ConnectionClosed rc_enu connection....'''
                            log.exception(kwargs["origin_exception"])
                            kwargs["init_rc_enu"] = True
                            await rc_enu.close()
                            return [
                                ipt, ids, v,
                                [di, control, (rc, rc_enu), process_data]
                            ], kwargs

                        except Exception as e:
                            kwargs["init_rc_enu"] = True
                            bprint(f"Algo pasa con rc_enu....{e}")
                            await rc_enu.close()
                            return [
                                ipt, ids, v,
                                [di, control, (rc, rc_enu), process_data]
                            ], kwargs

                        # send normal json
                        msg_result = qjson(result)
                        send = {
                            'channel': 'earlybird',
                            'command': 'add_data',
                            'data': msg_result
                        }
                        self.dbus_queue.put(send)
                        # send to earlybird
                        await asyncio.sleep(.1)
                        send_eb = {
                            'channel': 'earlybird',
                            'command': 'add_data',
                            'data': msg_result
                        }
                        try:
                            self.dbus_queue.put(send_eb)
                        except Exception as e:
                            rprint("Error al enviar send_ev")
                            bprint(e)
                            return [
                                ipt, ids, v,
                                [di, control, (rc, rc_enu), process_data]
                            ], kwargs
                        intersection = self.status_keys.intersection(c.keys())
                        if intersection:
                            data_msg = {
                                key: qjson(c.get(key))
                                for key in intersection
                            }
                            send = {
                                'channel': 'status',
                                'command': 'add_status',
                                'station': code,
                                'data': data_msg
                            }
                            self.dbus_queue.put(send)
                        if self.dbus_geojson_queue:
                            self.dbus_geojson_queue.put(send)
                    except asyncio.TimeoutError as e:
                        kwargs[
                            "origin_exception"] = f"PD_TO5_01 + {code} + {e}"
                        log.exception(kwargs["origin_exception"])
                        kwargs["init_rc_enu"] = True
                        await rc_enu.close()
                        return [
                            ipt, ids, v,
                            [di, control, (rc, rc_enu), process_data]
                        ], kwargs
                    except Exception as ex:
                        print("WS Error al enviar %s a cola %s" % (code, ex),
                              flush=True)
                        kwargs["origin_exception"] = "PD_TO5_02 + %s" % code
                        log.exception(kwargs["origin_exception"])
                        kwargs["init_rc_enu"] = True
                        await rc_enu.close()
                        bprint(kwargs)
                        return [
                            ipt, ids, v,
                            [di, control, (rc, rc_enu), process_data]
                        ], kwargs

                    list_ok.append(c)
                else:
                    msg = "Error en estacixon %s  ----> %s" % (code, c)
                    await rc.msg_log(msg, "DEBUG")
            if element:
                dt_recv = element['DT_RECV']
                di = element['DT_GEN']
                control = True
        return [ipt, ids, v, [di, control, (rc, rc_enu), process_data]], kwargs

    def set_pst(self, ids, args, kwargs):
        return [args[0], ids, *args[1:]], kwargs

    def set_init_args_kwargs(self, ipt):
        """
        This definition is for collector instance
        """
        log = print
        log = LogFile("Engine@Datawork",
                      "CORE_%s" % ipt,
                      "localhost@pineiden",
                      path=str(self.log_path / "engine"))
        self.log_manager[ipt] = log
        di= rdb.iso8601(get_datetime_di(delta=0))  # now
        return [ipt, 1, (di, None, (None, None), None)], {
            "log": log,
            "start_rdb_rc": True,
            "start_rdb_rc_enu": True
        }
