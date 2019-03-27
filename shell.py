from OSS_api import *
import json


config_path = get_config_path()
with open(config_path, "r") as f:
    load_dic = json.load(f)
oss = OSS(load_dic['access_key_id'], load_dic['access_key_secret'], load_dic['endpoint'], load_dic['bucket_name'], load_dic['default_path'])
oss.print_dir()

while 1:
    print(oss.bucket_info.name, end=' ')
    if os_name != 'Windows':
        indict = input('\033[0;32m~/' + oss.now_path() + '\033[0m>').split(' ')
    else:
        indict = input('~/' + oss.now_path() + '>').split(' ')

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
        elif len(indict) == 3:
            oss.upload(indict[1], indict[2])
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
    elif indict[0] == 'help':
        print_info('show content : dir')
        print_info('change dir   : cd <dir>')
        print_info('remove       : rm <remote_path>')
        print_info('upload       : ul <remote_path> <local_path> || ul <local_path>')
        print_info('download     : dl <remote_path> <local_path> || dl <remote_path>')
        print_info('set sync     : set <local_path> || set <local_path> <remote_path>')
        print_info('start sync   : sync <local_path> || sync')
        print_info('disable sync : dis <local_path>')
        print_info('get info     : info || sync-info')
        print_info('quit         : quit')
        print_info('refresh      : f5')
    elif indict[0] == 'set':
        if len(indict) == 3:
            oss.set_sync(indict[1], indict[2])
        elif len(indict) == 2:
            oss.set_sync(indict[1], '/' + oss.now_path())
    elif indict[0] == 'sync':
        if len(indict) == 1:
            oss.sync('')
        elif len(indict) == 2:
            oss.sync(indict[1])
    elif indict[0] == 'sync-info':
        oss.print_sync_info()
    elif indict[0] == 'dis':
        if len(indict) == 2:
            oss.disable_sync(indict[1])
    elif indict[0] == 'f5':
        oss.refresh()
    elif indict[0] == 'quit':
        exit()
