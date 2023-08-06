import pandas as pd
import numpy as np
import pickle
import base64
import csv
import os





def csv_write(fname, obj):


    if os.path.isfile(fname):
        os.remove(fname)



    with open(fname, 'a', encoding='utf8') as csv_file:
        wr = csv.writer(csv_file, delimiter='|')
        pickle_bytes = pickle.dumps(obj)            # unsafe to write
        b64_bytes = base64.b64encode(pickle_bytes)  # safe to write but still bytes
        b64_str = b64_bytes.decode('utf8')          # safe and in utf8
        wr.writerow(['col1', 'col2', b64_str])
        



def csv_read(fname):

    with open(fname, 'r') as csv_file:
        count = 0
        obj = 0
        for line in csv_file:
            
            line = line.strip('\n')
            
            b64_str = line.split('|')[2]                    # take the pickled obj
            obj = pickle.loads(base64.b64decode(b64_str))

            break

    return obj




def comp_csv_write(fname, obj):


    if os.path.isfile(fname):
        os.remove(fname)



    with open(fname, 'a', encoding='utf8') as csv_file:
        wr = csv.writer(csv_file, delimiter='|')
        pickle_bytes = pickle.dumps(obj)            # unsafe to write
        b64_bytes = base64.b64encode(pickle_bytes)  # safe to write but still bytes
        b64_str = b64_bytes.decode('utf8')          # safe and in utf8

        length = len(b64_str)

        n = int(length/16)

        wr.writerow(['col1', 'col2', length])

        if length % 16 == 0:
            for m in range(n):
                wr.writerow(['col1', 'col2', b64_str[m*16:(m+1)*16]])
        else:
            for m in range(n):
                wr.writerow(['col1', 'col2', b64_str[m*16:(m+1)*16]])
            wr.writerow(['col1', 'col2', b64_str[n*16:]])
            






def comp_csv_read(fname):

    with open(fname, 'r') as csv_file:
        count = 0
        obj = 0
        length = 0
        stor = []

        for line in csv_file:
            
            line = line.strip('\n')
            b64_str = line.split('|')[2]                    # take the pickled obj

            length = int(b64_str)
            
            stor.append(b64_str)
                
            #obj = pickle.loads(base64.b64decode(b64_str))

            break

        count = 0
        stor = []
        p = 1 
        if length % 16 == 0:
            m = int(length/16)
        else:
            m = int(length/16) + 1
        
        for line in csv_file:
            if count == -1:
                count += 1
                p = 1 - p
                continue
            
            if p == 1:
                p = 1 - p
                continue
            
            if count >= m:
                break
            line = line.strip('\n')
            b64_str = line.split('|')[2]                    # take the pickled obj

            stor.append(b64_str)
                
            #obj = pickle.loads(base64.b64decode(b64_str))

            count += 1
            p = 1 - p
    s = ""
    for st in stor:
        s = s + st
    obj = pickle.loads(base64.b64decode(s))
    return obj

