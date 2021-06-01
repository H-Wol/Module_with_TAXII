import os
import gc
import re
import time
import json 
import requests
import importlib
from datetime import datetime, timedelta, tzinfo
from logger import inter_error_logger, interlocker_logger
from urllib.parse import urlparse
from stix2 import IPv4Address, Bundle, NetworkTraffic, MemoryStore, Filter
from config.ConfigManager import JsonConfigFileManager
from utils import JsonConfigFileManager, load_module_func, configure_url, confirm_Connection, add_slash, del_slash

STIX_SAVE_DIR = './STIX/'

LOG_DIR = './log/'

class simple_utc(tzinfo):
    def tzname(self,**kwargs):
        return "UTC"
    def utcoffset(self, dt):
        return timedelta(0)
        
class logParser:
    def __init__(self,log):
        logs = log.split(',')
        self.src_ip = logs[2]
        self.dst_ip = logs[3]
        self.protocol = logs[4]
        start = datetime.strptime(logs[6],"%Y-%m-%d %H:%M:%S.%f") -timedelta(hours=9) # UTC 시간의 경우 timedelta 제외
        self.start = start.replace(tzinfo=simple_utc()).isoformat().replace('+00:00','Z')
        self.pkt_counts = logs[7]
        self.pkt_bypes = logs[8]

def convert_log_to_STIX(logs):
    ip_1 = IPv4Address(value = logs.src_ip)
    ip_2 = IPv4Address(value = logs.dst_ip)
    traffic = NetworkTraffic(start = logs.start,
            src_ref = ip_1.id,
            dst_ref = ip_2.id,
            protocols = [logs.protocol],
            src_packets = logs.pkt_counts,
            src_byte_count = logs.pkt_bypes
        ).serialize()
    return [json.loads(ip_1.serialize()),json.loads(ip_2.serialize()),json.loads(traffic)]


def convert_log_to_STIX_ip(ip):
    stix_ip = IPv4Address(value = ip)
    return stix_ip


def convert_log_to_STIX_traffic(logs,mem):
    src = mem.query([Filter("value","=",logs.src_ip)])[0].id
    dst = mem.query([Filter("value","=",logs.dst_ip)])[0].id
    traffic = NetworkTraffic(start = logs.start,
            src_ref = src,
            dst_ref = dst,
            protocols = [logs.protocol],
            src_packets = logs.pkt_counts,
            src_byte_count = logs.pkt_bypes
        )
    return traffic.serialize()

def open_log_file(name):
    with open('log/{}'.format(name),'r') as f:
        lines = f.read()
    return lines

def extract_ip_from_file(log,mem):
    pattren = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
    ip_candidates = list(set(re.findall(pattren,log)))
    returnVal = list()
    for ip in ip_candidates:
        stix = convert_log_to_STIX_ip(ip)
        mem.add(stix)
        returnVal.append(stix.serialize())
    return returnVal


def extract_log_from_file(log_type,log_name,conf):
    target_log = LOG_DIR+log_name

    start_index_session = conf.index['session']
    log_total_index =  os.popen('wc -l {}'.format(target_log)).read().split(' ')[0] 
    total_log = open_log_file(log_name)
    return total_log

def convert_form_log_to_file(conf,total_log):
    mem = MemoryStore()
    tmp_list = extract_ip_from_file(total_log,mem)
    total_log = total_log.splitlines()

    
    for line in total_log:
        logs = logParser(line)
        tmp_list.append(convert_log_to_STIX_traffic(logs,mem))
    dump = json.loads(Bundle(tmp_list).serialize())

    now = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")

    with open('{}{}.json'.format(STIX_SAVE_DIR,now), 'w', encoding='utf-8') as f:
        json.dump((dump),f, indent="\t")

    del mem
    gc.collect()

def upload(conf):

    taxii = load_module_func("taxii2client.{}".format(conf.version.TAXII))

    url = configure_url(conf)

    if confirm_Connection(conf,taxii):
        inter_error_logger.error("Server Connection Error {}".format(url))
        return 0

    url = configure_url(conf,'collection',conf)
    
    collection = taxii.Collection(url,user=conf.id, password=conf.pw)

    if not collection.can_write:
        inter_error_logger.error("Selected collection cannot be written. URL : {}".format(url))
        return 0
    for bundle in os.listdir(STIX_SAVE_DIR):
        with open(os.path.join(STIX_SAVE_DIR,bundle)) as json_file:
            stix_bundle = json.load(json_file)
        try:
            collection.add_objects(stix_bundle)
            interlocker_logger.info("Finished uploading. Bundle : {}".format(bundle))
        except Exception as e:
            inter_error_logger.error("Failed to Upload. Bundle : {}".format(bundle))
            inter_error_logger.error(e)
            continue
        os.system('rm {}'.format(os.path.join(STIX_SAVE_DIR,bundle)))


def main():
    conf_file = "Log_interlocker_config.json"

    try:
        print("Start reading config file.")
        conf = JsonConfigFileManager('./config/{}'.format(conf_file)).values
        print("Finished reading config file.")
        interlocker_logger.info("Finished reading config file.")
    except Exception as e:
        inter_error_logger.error("Failed to Read config file. Config File : {}".format(conf_file))
        inter_error_logger.error(e)
        return 0
    
    try:
        print("Start loading log from file.")
        total_log = extract_log_from_file('session','test.log',conf)
        print("Finished Loading log from file.")
        interlocker_logger.info("Finished Loading log from file.")
    except Exception as e:
        inter_error_logger.error("Failed to Load log from file. Log Name : {}".format('test.log'))
        inter_error_logger.error(e)
        return 0

    try:
        print("Start converting log to Stix")
        convert_form_log_to_file(conf,total_log)
        print("Finished converting log to Stix.")
        interlocker_logger.info("Finished converting log to Stix.")
    except Exception as e:
        inter_error_logger.error("Failed to convert log to Stix. Log Name : {}".format('test.log'))
        inter_error_logger.error(e)
        return 0  
    try:
        print("Start uploading STIX")
        upload(conf)
        print("Finished uploading STIX")
        interlocker_logger.info("Finished uploading STIX")
    except Exception as e:
        inter_error_logger.error("Failed to upload STIX. URL : {}".format(configure_url(conf)))
        inter_error_logger.error(e)
        return 0
if __name__ == '__main__':
    main()
