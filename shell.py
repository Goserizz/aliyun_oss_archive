from OSS_api import OSS
import json


with open("/etc/oss/config.json", "r") as f:
    load_dic = json.load(f)
oss = OSS(load_dic['access_key_id'], load_dic['access_key_secret'], load_dic['endpoint'], load_dic['bucket_name'], load_dic['default_path'])
oss.print_dir()

while 1:
    print(oss.bucket_info.name, end=' ')
    indict = input('\033[0;32m~/' + oss.now_path() + '\033[0m>').split(' ')

    new_indict = []
    i = 0
    while i < len(indict):
        j = i + 1
        while indict[i].endswith('\\') and j < len(indict):
            indict[i] = indict[i][0:-1] + ' ' + indict[j]
            j += 1
        new_indict.append(indict[i])
        i = j
    indict = new_indict

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
            oss.remove(indict[1])
    elif indict[0] == 'dl':
        if len(indict) == 3:
            oss.download(indict[1], indict[2])
        elif len(indict) == 2:
            oss.download(indict[1], oss.default_path)
    elif indict[0] == 'info':
        oss.print_bucket_info()
