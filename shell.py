from OSS_api import print_info, os_name, OSS
import json


def input_std(input_str):
    if os_name != 'Windows':
        indict = input('\033[0;32m' + input_str + '\033[0m').split(' ')
    else:
        indict = input(input_str).split(' ')
    new_indict = []
    i = 0
    while i < len(indict):
        j = i + 1
        while indict[i].endswith('\\') and j < len(indict):
            indict[i] = indict[i][0:-1] + ' ' + indict[j]
            j += 1
        new_indict.append(indict[i])
        i = j
    return new_indict


def upload(oss, indict):
    if len(indict) == 2:
        oss.upload('/' + oss.now_path(), indict[1])
    elif len(indict) == 3:
        oss.upload(indict[1], indict[2])


def remove(oss, indict):
    if len(indict) == 2:
        oss.remove(indict[1])


def download(oss, indict):
    if len(indict) == 3:
        oss.download(indict[1], indict[2])
    elif len(indict) == 2:
        oss.download(indict[1], oss.default_path)


def set_sync(oss, indict):
    if len(indict) == 3:
        oss.set_sync(indict[1], indict[2])
    elif len(indict) == 2:
        oss.set_sync(indict[1], '/' + oss.now_path())


def push(oss, indict):
    if len(indict) == 1:
        oss.sync('', True)
    elif len(indict) == 2:
        oss.sync(indict[1], True)


def pull(oss, indict):
    if len(indict) == 1:
        oss.sync('', False)
    elif len(indict) == 2:
        oss.sync(indict[1], False)


def sync_info(oss, indict):
    if len(indict) == 1:
        oss.print_sync_info()


def disable(oss, indict):
    if len(indict) == 2:
        oss.disable_sync(indict[1])


def file_info(oss, indict):
    if len(indict) == 2:
        oss.print_file_info(indict[1])


def info(oss, indict):
    if len(indict) == 1:
        oss.print_bucket_info()


def help(manage):
    print_info('remove       : rm <remote_path>')
    print_info('upload       : ul <remote_path> <local_path> || ul <local_path>')
    print_info('download     : dl <remote_path> <local_path> || dl <remote_path>')
    print_info('set sync     : set <local_path> || set <local_path> <remote_path>')
    print_info('start push   : push <local_path> || push')
    print_info('start pull   : pull <local_path> || pull')
    print_info('disable sync : dis <local_path>')
    print_info('get info     : info || sync-info')
    print_info('file info    : finfo <remote_path>')
    if not manage:
        print_info('show content : dir')
        print_info('change dir   : cd <dir>')
        print_info('quit         : quit')
        print_info('refresh      : f5')


def shell(oss):
    oss.print_dir()
    while 1:
        print(oss.bucket_info.name, end=' ')
        indict = input_std('~/' + oss.now_path() + '>')

        if indict[0] == 'dir':
            oss.print_dir()
        elif indict[0] == 'cd':
            if len(indict) == 2:
                oss.change_directory(indict[1])
        elif indict[0] == 'ul':
            upload(oss, indict)
        elif indict[0] == 'rm':
            remove(oss, indict)
        elif indict[0] == 'dl':
            download(oss, indict)
        elif indict[0] == 'info':
            info(oss, indict)
        elif indict[0] == 'help':
            help(False)
        elif indict[0] == 'set':
            set_sync(oss, indict)
        elif indict[0] == 'push':
            push(oss, indict)
        elif indict[0] == 'pull':
            pull(oss, indict)
        elif indict[0] == 'sync-info':
            sync_info(oss, indict)
        elif indict[0] == 'dis':
            disable(oss, indict)
        elif indict[0] == 'f5':
            oss.refresh()
        elif indict[0] == 'finfo':
            file_info(oss, indict)
        elif indict[0] == 'quit':
            exit()
