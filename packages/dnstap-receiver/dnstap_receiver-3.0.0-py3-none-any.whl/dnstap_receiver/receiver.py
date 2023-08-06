import argparse
import logging
import asyncio
import socket
import yaml
import sys
import re
import ssl
import pkgutil
import ipaddress

from datetime import datetime, timezone

import geoip2.database

# python3 -m pip dnspython
import dns.rcode
import dns.rdatatype
import dns.message

# create default logger for the dnstap receiver
clogger = logging.getLogger("dnstap_receiver.console")

# import framestreams and dnstap protobuf decoder
from dnstap_receiver.codecs import dnstap_pb2 
from dnstap_receiver.codecs import fstrm 

# import all inputs
from dnstap_receiver.inputs import input_unixsocket
from dnstap_receiver.inputs import input_tcpsocket

# import all outputs
from dnstap_receiver.outputs import output_stdout
from dnstap_receiver.outputs import output_file
from dnstap_receiver.outputs import output_syslog
from dnstap_receiver.outputs import output_tcp
from dnstap_receiver.outputs import output_metrics

from dnstap_receiver import api_server
from dnstap_receiver import statistics
from dnstap_receiver import dnspython_patch

class UnknownValue:
    name = "-"

DNSTAP_TYPE = dnstap_pb2._MESSAGE_TYPE.values_by_number
DNSTAP_FAMILY = dnstap_pb2._SOCKETFAMILY.values_by_number
DNSTAP_PROTO = dnstap_pb2._SOCKETPROTOCOL.values_by_number  

DFLT_LISTEN_IP = "0.0.0.0"
DFLT_LISTEN_PORT = 6000

# command line arguments definition
parser = argparse.ArgumentParser()
parser.add_argument("-l", 
                    help="IP of the dnsptap server to receive dnstap payloads (default: %(default)r)",
                    default=DFLT_LISTEN_IP)
parser.add_argument("-p", type=int,
                    help="Port the dnstap receiver is listening on (default: %(default)r)",
                    default=DFLT_LISTEN_PORT)               
parser.add_argument("-u", help="read dnstap payloads from unix socket")
parser.add_argument('-v', action='store_true', help="verbose mode")   
parser.add_argument("-c", help="external config file")   

async def cb_ondnstap(dnstap_decoder, payload, cfg, queues_list, stats, geoip_reader):
    """on dnstap"""
    # decode binary payload
    dnstap_decoder.ParseFromString(payload)
    dm = dnstap_decoder.message
    
    if cfg["trace"]["dnstap"]:
        dns_pkt = dm.query_message if (dm.type % 2 ) == 1 else dm.response_message
        clogger.debug("%s\n%s\n\n" % (dm,dns.message.from_wire(dns_pkt)) )

    # filtering by dnstap identity ?
    tap_ident = dnstap_decoder.identity.decode()
    if not len(tap_ident):
        tap_ident = UnknownValue.name
    if cfg["filter"]["dnstap-identities"] is not None:
        if re.match(cfg["filter"]["dnstap-identities"], dnstap_decoder.identity.decode()) is None:
            del dm
            return
            
    tap = { "identity": tap_ident, "qname": UnknownValue.name, "rrtype": UnknownValue.name, 
            "query-type": UnknownValue.name, "source-ip": UnknownValue.name}
    
    # decode type message
    tap["message"] = DNSTAP_TYPE.get(dm.type, UnknownValue).name
    tap["family"] = DNSTAP_FAMILY.get(dm.socket_family, UnknownValue).name
    tap["protocol"] = DNSTAP_PROTO.get(dm.socket_protocol, UnknownValue).name

    # decode query address
    qaddr = dm.query_address
    if len(qaddr) and dm.socket_family == 1:
        # condition for coredns, address is 16 bytes long so keept only 4 bytes
        qaddr = qaddr[12:] if len(qaddr) == 16 else qaddr
        # convert ip to string
        tap["source-ip"] = socket.inet_ntoa(qaddr)
    if len(qaddr) and dm.socket_family == 2:
        tap["source-ip"] = socket.inet_ntop(socket.AF_INET6, qaddr)
    tap["source-port"] = dm.query_port
    if tap["source-port"] == 0:
        tap["source-port"] = UnknownValue.name
        
    # handle query message
    # todo catching dns.message.ShortHeader exception
    # can occured with coredns if the full argument is missing
    if (dm.type % 2 ) == 1 :
        dnstap_parsed = dnspython_patch.from_wire(dm.query_message,
                                  question_only=True)                 
        tap["length"] = len(dm.query_message)
        d1 = dm.query_time_sec +  (round(dm.query_time_nsec ) / 1000000000)
        tap["timestamp"] = datetime.fromtimestamp(d1, tz=timezone.utc).isoformat()
        tap["type"] = "query"
        latency = 0.0
        
    # handle response message
    if (dm.type % 2 ) == 0 :
        dnstap_parsed = dnspython_patch.from_wire(dm.response_message,
                                  question_only=True)
        tap["length"] = len(dm.response_message)
        d2 = dm.response_time_sec + (round(dm.response_time_nsec ) / 1000000000) 
        tap["timestamp"] = datetime.fromtimestamp(d2, tz=timezone.utc).isoformat()
        tap["type"] = "response"

        # compute latency 
        d1 = dm.query_time_sec +  (round(dm.query_time_nsec ) / 1000000000)
        latency = round(d2-d1,3)
    
    tap["latency"] = latency
        
    # common params
    if len(dnstap_parsed.question):
        tap["qname"] = dnstap_parsed.question[0].name.to_text()
        tap["rrtype"] = dns.rdatatype.to_text(dnstap_parsed.question[0].rdtype)
    tap["rcode"] = dns.rcode.to_text(dnstap_parsed.rcode())
    tap["id"] = dnstap_parsed.id
    tap["flags"] = dns.flags.to_text(dnstap_parsed.flags)

    # filtering by qname ?
    if cfg["filter"]["qname-regex"] is not None:
        if re.match(cfg["filter"]["qname-regex"], tap["qname"]) is None:
            del dm; del tap;
            return

    # geoip support 
    if geoip_reader is not None:
        try:
            response = geoip_reader.city(tap["source-ip"])
            if cfg["geoip"]["country-iso"]:
                tap["country"] = response.country.iso_code
            else:
                tap["country"] = response.country.name
            if response.city.name is not None:
                tap["city"] = response.city.name
            else:
                tap["city"] = UnknownValue.name
        except Exception as e:
            tap["country"] = UnknownValue.name
            tap["city"] = UnknownValue.name
            
    # update metrics 
    stats.record(tap=tap)
        
    # append the dnstap message to the queue
    for q in queues_list:
        q.put_nowait(tap)
    
async def cb_onconnect(reader, writer, cfg, queues_list, stats, geoip_reader):
    """callback when a connection is established"""
    # get peer name
    peername = writer.get_extra_info('peername')
    if not len(peername):
        peername = "(unix-socket)"
    clogger.debug(f"Input handler: new connection from {peername}")

    # access control list check
    if len(writer.get_extra_info('peername')):
        acls_network = []
        for a in cfg["input"]["tcp-socket"]["access-control-list"]:
            acls_network.append(ipaddress.ip_network(a))
            
        acl_allow = False
        for acl in acls_network:
            if ipaddress.ip_address(peername[0]) in acl:
                acl_allow = True
        
        if not acl_allow:
            writer.close()
            clogger.debug("Input handler: checking acl refused")
            return
        
        clogger.debug("Input handler: checking acl allowed")
        
    # prepare frame streams decoder
    fstrm_handler = fstrm.FstrmHandler()
    loop = asyncio.get_event_loop()
    dnstap_decoder = dnstap_pb2.Dnstap()

    try: 
        # syntax only works with python 3.8
        # while data := await reader.read(fstrm_handler.pending_nb_bytes()) 
        running = True
        while running:
            # read bytes
            data = await reader.read(fstrm_handler.pending_nb_bytes()) 
            if not len(data):
                running = False
                break
                
            # append data to the buffer
            fstrm_handler.append(data=data)
            
            # process the buffer, check if we have received a complete frame ?
            if fstrm_handler.process():
                # Ok, the frame is complete so let's decode it
                fs, payload  = fstrm_handler.decode()

                # handle the DATA frame
                if fs == fstrm.FSTRM_DATA_FRAME:
                    loop.create_task(cb_ondnstap(dnstap_decoder, payload, cfg, queues_list, stats, geoip_reader))
                    
                # handle the control frame READY
                if fs == fstrm.FSTRM_CONTROL_READY:
                    clogger.debug(f"Input handler: control ready received from {peername}")
                    ctrl_accept = fstrm_handler.encode(fs=fstrm.FSTRM_CONTROL_ACCEPT)
                    # respond with accept only if the content type is dnstap
                    writer.write(ctrl_accept)
                    await writer.drain()
                    clogger.debug(f"Input handler: sending control accept to {peername}")
                    
                # handle the control frame READY
                if fs == fstrm.FSTRM_CONTROL_START:
                    clogger.debug(f"Input handler: control start received from {peername}")
   
                # handle the control frame STOP
                if fs == fstrm.FSTRM_CONTROL_STOP:
                    clogger.debug(f"Input handler: control stop received from {peername}")
                    fstrm_handler.reset()           
    except asyncio.CancelledError:
        clogger.debug(f'Input handler: {peername} - closing connection.')
        writer.close()
        await writer.wait_closed()
    except asyncio.IncompleteReadError:
        clogger.debug(f'Input handler: {peername} - disconnected')
    finally:
        clogger.debug(f'Input handler: {peername} - closed')

def merge_cfg(u, o):
    """merge config"""
    for k,v in u.items():
        if k in o:
            if isinstance(v, dict):
                merge_cfg(u=v,o=o[k])
            else:
                o[k] = v
   
def setup_config(args):
    """load default config and update it with arguments if provided"""
    # set default config
    try:
        cfg =  yaml.safe_load(pkgutil.get_data(__package__, 'dnstap.conf')) 
    except FileNotFoundError:
        print("default config file not found")
        sys.exit(1)
    except yaml.parser.ParserError:
        print("invalid default yaml config file")
        sys.exit(1)

    # overwrite config with external file ?    
    if args.c:
        try:
            with open(args.c) as file:
                merge_cfg(u=yaml.safe_load(file),o=cfg)
        except FileNotFoundError:
            print("external config file not found")
            sys.exit(1)
        except yaml.parser.ParserError:
            print("external invalid yaml config file")
            sys.exit(1)

    # update default config with command line arguments
    if args.v:
        cfg["trace"]["verbose"] = args.v    
    if args.u is not None:
        cfg["input"]["unix-socket"]["path"] = args.u
    if args.l != DFLT_LISTEN_IP:
        cfg["input"]["tcp-socket"]["local-address"] = args.l
    if args.l != DFLT_LISTEN_PORT:
        cfg["input"]["tcp-socket"]["local-port"] = args.p

    return cfg
    
def setup_logger(cfg):
    """setup main logger"""

    loglevel = logging.DEBUG if cfg["verbose"] else logging.INFO
    logfmt = '%(asctime)s %(levelname)s %(message)s'
    
    clogger.setLevel(loglevel)
    clogger.propagate = False
    
    if cfg["file"] is None:
        lh = logging.StreamHandler(stream=sys.stdout )
    else:
        lh = logging.FileHandler(cfg["file"])
    lh.setLevel(loglevel)
    lh.setFormatter(logging.Formatter(logfmt))    
    
    clogger.addHandler(lh)
    
def setup_outputs(cfg, stats, loop):
    """setup outputs"""
    conf = cfg["output"]

    queues_list = []
    if conf["syslog"]["enable"]:
        if not output_syslog.checking_conf(cfg=conf["syslog"]): return
        queue_syslog = asyncio.Queue()
        queues_list.append(queue_syslog)
        loop.create_task(output_syslog.handle(conf["syslog"], queue_syslog, stats))    

    if conf["tcp-socket"]["enable"]:
        if not output_tcp.checking_conf(cfg=conf["tcp-socket"]): return
        queue_tcpsocket = asyncio.Queue()
        queues_list.append(queue_tcpsocket)
        loop.create_task(output_tcp.handle(conf["tcp-socket"], queue_tcpsocket, stats))
                                               
    if conf["file"]["enable"]:
        if not output_file.checking_conf(cfg=conf["file"]): return
        queue_file = asyncio.Queue()
        queues_list.append(queue_file)
        loop.create_task(output_file.handle(conf["file"], queue_file, stats))
                                              
    if conf["stdout"]["enable"]:
        if not output_stdout.checking_conf(cfg=conf["stdout"]): return
        queue_stdout = asyncio.Queue()
        queues_list.append(queue_stdout)
        loop.create_task(output_stdout.handle(conf["stdout"], queue_stdout, stats))

    if conf["metrics"]["enable"]:
        if not output_metrics.checking_conf(cfg=conf["metrics"]): return
        queue_metrics = asyncio.Queue()
        queues_list.append(queue_metrics)
        loop.create_task(output_metrics.handle(conf["metrics"], queue_metrics, stats))

    return queues_list
    
def setup_inputs(args, cfg, queues_list, stats, loop, geoip_reader):
    """setup inputs"""
    # define callback on new connection
    cb_lambda = lambda r, w: cb_onconnect(r, w, cfg, queues_list, stats, geoip_reader)
    
    # asynchronous unix socket
    if cfg["input"]["unix-socket"]["path"] is not None:
        socket_server = input_unixsocket.start_input(cfg=cfg["input"]["unix-socket"], cb_onconnect=cb_lambda, loop=loop)

    # default mode: asynchronous tcp socket
    else:
        socket_server = input_tcpsocket.start_input(cfg=cfg["input"]["tcp-socket"], cb_onconnect=cb_lambda, loop=loop)
                                             
    # run until complete
    loop.run_until_complete(socket_server)
    
def setup_api(cfg, stats, loop):
    """setup web api"""
    if cfg["web-api"]["enable"]:
        api_svr = api_server.create_server(loop, cfg=cfg["web-api"], 
                                           stats=stats, cfg_stats=cfg["statistics"])
        loop.run_until_complete(api_svr)

def setup_geoip(cfg):
    if not cfg["enable"]: return None
    if cfg["city-database"] is None: return None
    
    reader = None
    try:
        reader = geoip2.database.Reader(cfg["city-database"])
    except Exception as e:
        clogger.error("geoip setup: %s" % e)
        
    return reader
    
def start_receiver():
    """start dnstap receiver"""
    # Handle command-line arguments.
    args = parser.parse_args()

    # setup config
    cfg = setup_config(args=args)
  
    # setup logging
    setup_logger(cfg=cfg["trace"])

    # setup geoip if enabled 
    geoip_reader = setup_geoip(cfg=cfg["geoip"])
    
    # add debug message if external config is used
    if args.c: clogger.debug("External config file loaded")
    
    # start receiver and get event loop
    clogger.debug("Start receiver...")
    loop = asyncio.get_event_loop()
    stats = statistics.Statistics(cfg=cfg["statistics"])
    loop.create_task(statistics.watcher(stats))
    
    # prepare outputs
    queues_list = setup_outputs(cfg, stats, loop)
    
    # prepare inputs
    setup_inputs(args, cfg, queues_list, stats, loop, geoip_reader)

    # start the http api
    setup_api(cfg, stats, loop)

    # run event loop 
    try:
       loop.run_forever()
    except KeyboardInterrupt:
        pass

    # close geoip
    if geoip_reader is not None: geoip_reader.close()