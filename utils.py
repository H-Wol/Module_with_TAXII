from easydict import EasyDict
import json
import importlib


class JsonConfigFileManager:
    def __init__(self, file_path):
        self.values = EasyDict()
        if file_path:
            self.file_path = file_path
            self.reload()

    def reload(self):
        self.clear()
        if self.file_path:
            with open(self.file_path, 'r') as f:
                self.values.update(json.load(f))

    def clear(self):
        self.values.clear()

    def update(self, in_dict):
        for (k1, v1) in in_dict.items():
            if isinstance(v1, dict):
                for (k2, v2) in v1.items():
                    if isinstance(v2, dict):
                        for (k3, v3) in v2.items():
                            self.values[k1][k2][k3] = v3
                    else:
                        self.values[k1][k2] = v2
            else:
                self.values[k1] = v1

    def export(self, save_file_name):
        if save_file_name:
            with open(save_file_name, 'w') as f:
                json.dump(dict(self.values), f)


def load_module_func(module_name):
    mod = importlib.import_module(module_name)
    return mod

def configure_url(conf,*args):
    if 'dicovery_url' in conf:
        url = "{}://{}".format(conf.protocol,conf.dicovery_url)
    elif 'host' in conf:
        url = "{}://{}:{}".format(conf.protocol,conf.host,conf.port)
    
    url = add_slash(url)
    if args:
        
        if args[0] == 'discovery':
            if conf.version.TAXII == 'v20':
                taxii_ver = 'taxii/'
            elif conf.version.TAXII == 'v21':
                taxii_ver = 'taxii2/'
            if url.split('/')[-2] != taxii_ver:
                url += taxii_ver
        elif args[0] == 'api_root':
            info = args[1]
            url += '{}/'.format(info.api_root)
        elif args[0] == 'collection':
            info = args[1]
            url += '{}/collections/{}/'.format(info.api_root,info.collection)
        
    return url

def confirm_Connection(conf,taxii):
    retry = conf.retry
    count = 1
    url = configure_url(conf,'discovery')
    while 1:
        try:
            server = taxii.Server(url, user=conf.id, password=conf.pw).title
            return 0
        except Exception as e:
            count += 1
            if count == retry:
                return 1

def add_slash(string):
    if string[-1] == "/":
        string = string
    else:
        string = string + "/"
    return string
def del_slash(string):
    if string[-1] == "/":
        string = string[0:-1]
    else:
        string = string
    return string