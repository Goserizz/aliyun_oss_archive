from OSS_api import OSS
import json


with open("config.json", "r") as f:
    load_dic = json.load(f)
oss = OSS(load_dic['access_key_id'], load_dic['access_key_secret'], load_dic['endpoint'], load_dic['bucket_name'])
while 1:
    indict = input('>').split(' ')
    if indict[0] == 'dir':
        oss.print_dir()
    elif indict[0] == 'cd':
        if len(indict) == 2:
            oss.change_directory(indict[1])
    elif indict[0] == 'ul':
        if len(indict) == 2:
            oss.upload(oss.now_path(), indict[1])
    elif indict[0] == 'rm':
        if len(indict) == 2:
            if indict[1].startswith('/'):
                print('Can only remove file/dir in current dir.')
            else:
                oss.remove(indict[1])
