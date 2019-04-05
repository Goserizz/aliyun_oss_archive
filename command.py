import os
import json
from OSS_api import get_config_path, os_name
from shell import input_std


config_path = get_config_path()
with open(config_path, 'r') as f:
    load_dic = json.load(f)
manage_path = load_dic['manage_path']
while True:
    indict = input_std('command~>')
    if indict[0] != 'oss':
        continue
    os.system('python ' + manage_path + ' ' + ' '.join(indict[1:]))
