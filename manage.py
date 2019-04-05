from OSS_api import OSS, get_config_path
import shell
import json, sys


def init_oss(catalog):
    config_path = get_config_path()
    with open(config_path, "r") as f:
        load_dic = json.load(f)
    if catalog:
        return OSS(load_dic['access_key_id'], load_dic['access_key_secret'], load_dic['endpoint'], load_dic['bucket_name'], load_dic['default_path'], True)
    else:
        return OSS(load_dic['access_key_id'], load_dic['access_key_secret'], load_dic['endpoint'], load_dic['bucket_name'], load_dic['default_path'], False)

if len(sys.argv) == 1:
    shell.shell(init_oss(True))
else:
    indict = sys.argv[1:]
    if indict[0] == 'ul':
        shell.upload(init_oss(True), indict)
    elif indict[0] == 'dl':
        shell.download(init_oss(True), indict)
    elif indict[0] == 'rm':
        shell.remove(init_oss(True), indict)
    elif indict[0] == 'set':
        shell.set_sync(init_oss(True), indict)
    elif indict[0] == 'sync':
        shell.sync(init_oss(True), indict)
    elif indict[0] == 'sync-info':
        shell.sync_info(init_oss(False), indict)
    elif indict[0] == 'dis':
        shell.disable(init_oss(False), indict)
    elif indict[0] == 'finfo':
        shell.file_info(init_oss(False), indict)
    elif indict[0] == 'help':
        shell.help(1)
    elif indict[0] == 'info':
        shell.info(init_oss(False), indict)
    