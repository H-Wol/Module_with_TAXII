import json 
import time
import requests
from datetime import datetime
from logger import error_logger
from urllib.parse import urlparse
from utils import JsonConfigFileManager, load_module_func, configure_url, confirm_Connection, add_slash, del_slash
from stix2 import MemoryStore

COLLECTION_SAVE_DIR = './collection'



def select_collection(url,taxii,conf):
    collection_list = taxii.ApiRoot(url,user=conf.id, password=conf.pw).collections
    if collection_list == []:  
        error_logger.error("There is no collection in that apiroot. URL : {}".format(url))
        return 0
    for num in range(len(collection_list)):
        print ("{}. {}".format(num+1,collection_list[num].title))
    selection = int(input())
    return collection_list[selection-1].url

def select_api_root(url,taxii,conf):
    headers = JsonConfigFileManager('./config/header.json').values[conf.version.TAXII]
    api_root_list = taxii.Server(url,user=conf.id, password=conf.pw).api_roots
    session = requests.Session()
    session.auth = (conf.id,conf.pw)
    r = session.get(url,headers=headers)
    for num in range(len(list(r.json()['api_roots']))):
        print ("{}. {}".format(num+1,r.json()['api_roots'][num]))
    selection = int(input())
    if 'host' in conf:
        url =del_slash(configure_url(conf)) + (urlparse(r.json()['api_roots'][selection-1]).path)
    else:
        url = r.json()['api_roots'][selection-1]
    return url

def main():
    config = JsonConfigFileManager('./config/IP_collect_config.json').values
    
    for server in config:
            error_logger.error("Server Connection Error {}".format(url))
            continue

        for num in conf.detail:
            info = conf.detail[num]
            api_root = info.api_root
            collection_id = info.collection

            if collection_id:
                url = configure_url(conf,'collection',info)
            elif api_root:
                url = configure_url(conf,'api_root',info)
                url = select_collection(url,taxii,conf)
            else:
                url = configure_url(conf,'discovery',info)
                url = select_api_root(url,taxii,conf)
                url = select_collection(url,taxii,conf)
            if not url:
                continue
            print(url)
            collection = taxii.Collection(url,user=conf.id, password=conf.pw)

            if not collection.can_read:
                error_logger.error("Selected collection cannot be read. URL : {}".format(url))
                continue

            # collection_objects = MemoryStore()
            collection_objects = list()
            objects = collection.get_objects()
            while 1:
                print('while?')
                if not objects:
                    break
                # collection_objects.add(objects['objects'])
                collection_objects += objects['objects']
                if not 'more' in objects:
                    break
                if not objects['more']:
                    break
                objects = collection.get_objects(next=objects['next'])
            
            # collection_objects.save_to_file('{}/{}.json'.format(COLLECTION_SAVE_DIR,collection.id))
            with open('{}/{}.json'.format(COLLECTION_SAVE_DIR,collection.id), 'w', encoding='utf-8') as f:
                json.dump(collection_objects,f, indent="\t")
            print('done')

if __name__ == '__main__':
    main()