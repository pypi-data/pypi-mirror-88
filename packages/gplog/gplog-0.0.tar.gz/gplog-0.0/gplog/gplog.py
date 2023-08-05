from datetime import datetime
from os import getenv as arg
from sys import exc_info
from traceback import extract_tb



class StdOut:
    def __init__(self):
        self.service_name = arg('SERVICE_NAME')
    def info(self,message):
        print({"service":self.service_name,"log_level":"INFO","date":str(datetime.now()),"message":message},flush=True)
    def warn(self,message):
        print({"service":self.service_name,"log_level":"WARNING","date":str(datetime.now()),"message":message},flush=True)
    def err(self,message):
        __message = {"text":message,"trace":[]}
        ext = extract_tb(exc_info()[2])
        for i in range(len(ext)):
            __message['trace'].append({"file":ext[i].filename,"line":ext[i].lineno})
        print({"service":self.service_name,"log_level":"ERROR","date":str(datetime.now()),"message":__message},flush=True)

stdout = StdOut()

def info(message):
    stdout.info(message)

def warning(message):
    stdout.warn(message)

def error(message):
    stdout.err(message)