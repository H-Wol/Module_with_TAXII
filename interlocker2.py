from stix2 import CustomObservable
from stix2.properties import (IntegerProperty, StringProperty, BinaryProperty,
                              ObjectReferenceProperty,  TimestampProperty, BooleanProperty, TypeProperty)
import time
from datetime import datetime, timedelta, tzinfo
from utils import (JsonConfigFileManager, load_module_func,
                   configure_url, confirm_Connection, add_slash, del_slash)
import ipaddress

from stix2 import IPv4Address, Bundle, NetworkTraffic, MemoryStore, Filter


class simple_utc(tzinfo):
    def tzname(self, **kwargs):
        return "UTC"

    def utcoffset(self, dt):
        return timedelta(0)

# api request result example : 1,0,000000,...etc


class LogParser:
    log_count = 0

    def __init__(self, log):
        self.log = log
        self.parse_log()
        LogParser.log_count += 1

    def parse_log(self):
        log_type = ['session']
        module_type = ['packet', 'policy', 'system']
        protocols = ['TCP', 'UDP']
        logs = self.log.replace(' ', '').split(',')
        self.index = int(logs[0])
        self.log_type = log_type[int(logs[1])]
        self.module = module_type[int(logs[2], 2)]
        self.src_ip_type = int(logs[3], 2)
        self.src_ip_type, self.src_ip = self.convert_bin_to_ip(
            self.src_ip_type, logs[4])
        self.src_port = int(logs[5])
        self.dst_ip_type = int(logs[6], 2)
        self.dst_ip_type, self.dst_ip = self.convert_bin_to_ip(
            self.dst_ip_type, logs[7])
        self.dst_port = int(logs[8])
        self.protocol = protocols[int(logs[9], 2)]
        self.block_code = int(logs[10], 2)
        # binary to datetime logic require!!!!!
        # create_date = datetime.strptime(
        #     logs[11], "%Y-%m-%d %H:%M:%S") - timedelta(hours=9)  # UTC 시간의 경우 timedelta 제외
        # self.create_date = create_date.replace(
        #     tzinfo=simple_utc()).isoformat().replace('+00:00', 'Z')
        self.pkt_counts = int(logs[12])
        self.pkt_bypes = int(logs[13])

    def convert_bin_to_ip(self, ipv, ip_log):
        if ipv == 0:
            return 'IPv4', str(ipaddress.IPv4Address(int(ip_log, 2)))
        else:
            return 'IPv6', str(ipaddress.IPv6Address(int(ip_log, 2)))


@CustomObservable(
    'session-log',
    [
        ('index', IntegerProperty(required=True)),
        ('log_type', StringProperty(required=True)),
        ('module', StringProperty(required=True)),
        ('src_ip_type', StringProperty(required=True)),
        ('src_ip', StringProperty(required=True)),
        ('src_port', IntegerProperty(required=True)),
        ('dst_ip_type', StringProperty(required=True)),
        ('dst_ip', StringProperty(required=True)),
        ('dst_port', IntegerProperty(required=True)),
        ('protocol', StringProperty(required=True)),
        ('block_code', BooleanProperty(required=True)),
        # ('create_date', TimestampProperty(required=True)),
        ('pkt_counts', IntegerProperty(required=True)),
        ('pkt_bytes', IntegerProperty(required=True))
    ],
    ['index', 'src_ip', 'dst_ip', 'protocol']  # 'create_date'
)
class Stix():
    pass


# @CustomObservable(
#     'any_other_log',
#     [
#         ('index', IntegerProperty(required=True)),
#         ('log_type', StringProperty(required=True)),
#         ('module', StringProperty(required=True)),
#         ('src_ip_type', StringProperty(required=True)),
#         ('src_ip', StringProperty(required=True)),
#         ('src_port', IntegerProperty(required=True)),
#         ('dst_ip_type', StringProperty(required=True)),
#         ('dst_ip', StringProperty(required=True)),
#         ('dst_port', IntegerProperty(required=True)),
#         ('protocol', StringProperty(required=True)),
#         ('block_code', BooleanProperty(required=True)),
#         # ('create_date', TimestampProperty(required=True)),
#         ('pkt_counts', IntegerProperty(required=True)),
#         ('pkt_bytes', IntegerProperty(required=True))
#     ],
#     ['index', 'src_ip', 'dst_ip', 'protocol']  # 'create_date'
# )
# class Stix1():
#     pass


if __name__ == '__main__':

    # logs = "0,'00000000 0000000','00000000 00000000','11111111111111111111111111111111','80','00000000 00000000','11111111111111111111111111111111','80','00000000 00000000','00000000 00000001','','20','350'"
    logs = "1,0,00000000 0000000,00000000 00000000,11111111111111111111111111111111,80,00000000 00000001,1111111111111111111111111111111111111111111111111111111111111111,80,00000000 00000000,00000000 00000001,,0,350"
    log1 = LogParser(logs)
    new_observable = Stix(index=log1.index,
                          log_type=log1.log_type,
                          module=log1.module,
                          src_ip_type=log1.src_ip_type,
                          src_ip=log1.src_ip,
                          src_port=log1.src_port,
                          dst_ip_type=log1.dst_ip_type,
                          dst_ip=log1.dst_ip,
                          dst_port=log1.dst_port,
                          protocol=log1.protocol,
                          block_code=log1.block_code,
                          #   create_date=log1.create_date,
                          pkt_counts=log1.pkt_counts,
                          pkt_bytes=log1.pkt_bypes
                          )
    print(new_observable)
    mem = MemoryStore()
    mem.add(new_observable)
    print(mem.query([Filter("index", "=", 1)])[0])
