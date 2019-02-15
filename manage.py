from OSS_api import OSS
import json, sys


with open("config.json", "r") as f:
    load_dic = json.load(f)
oss = OSS(load_dic['access_key_id'], load_dic['access_key_secret'], load_dic['endpoint'], load_dic['bucket_name'])

if len(sys.argv) == 2:
    oss.upload(oss.now_path(), sys.argv[1])
