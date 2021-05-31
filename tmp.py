# # # # # datetime.now().strftime("%Y%m%d-%H%M%S")


# # # # def del_slash(url):
# # # #     if url[-1] == "/":
# # # #         url = url[0:-1]
# # # #     else:
# # # #         url = url
# # # #     return url


# # # # print(del_slash('abc'))


# # # # import requests

# # # # url = "http://127.0.0.1:5000/taxii2"

# # # # payload={}
# # # # files={}
# # # # headers = {
# # # #   'Accept': 'application/taxii+json;version=2.1',
# # # #   'Content-Type': 'application/taxii+json;version=2.1',
# # # #   'Authorization': 'Basic YWRtaW46UGFzc3dvcmQw'
# # # # }

# # # # response = requests.request("GET", url, headers=headers, data=payload, files=files)

# # # # print(response.text)


# # # from urllib.parse import urlparse, urljoin

# # # a = urlparse('http://localhost:500/asd/asd/asff/as/asd/asd?Asda=3')

# # # print((a.path))
# # # print(urljoin(a.scheme,a.netloc))


# # # import datetime
# # # import dateutil

# # # def getDateTimeFromISO8601String(s):
# # #     d = dateutil.parser.parse(s)
# # #     return d
# # # print(getDateTimeFromISO8601String("2019-01-04T16:41:24+0900"))



with open('log/test.log', 'w' ) as f:
    for i in range(10):        
        for j in range(10):        
            for z in range(10):        
                for x in range(100):
                    f.write('session,ui,192.168.{}.1,191.168.0.{},TCP,1,2021-05-17 10:10:{}.{},2,2\n'.format(i,j,z,x))


# # import os

# # LOG_DIR = './log/'
# # target_log = LOG_DIR+'test.log'
# # log_total_index =  os.popen('wc -l {}'.format(target_log)).read().split(' ')[0]
# # print(log_total_index)


# # def open_log_file(start_index):
# #     with open('log/session.log','r') as f:
# #         f.seek(start_index)
# #         lines = f.read(2).splitlines()
# #     return lines

# # print(len(open_log_file(2)))
# # print(open_log_file(2))



# from interlocker import *

# def open_log_file(name):
#     with open('log/{}'.format(name),'r') as f:
#         lines = f.read()
#     return lines


# conf = JsonConfigFileManager('./config/Log_interlocker_config.json').values
# total_log = open_log_file('test.log')

# print(len(total_log.splitlines()))

# import re

# ip_candidates = list(set(re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", total_log)))
# print(ip_candidates)