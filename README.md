# aliyun_oss_archive
basic operations:
dir: show current dir's contents
cd: change directory
ul: upload directory or file to current remote dir
rm: remove directory or file in current remote dir
dl: download directory or file from remote to local
info: get infomation about current server

configuration file: config.json
{
  'access_key_id': <access_key_id>,
  'access_key_secret: <access_key_secret>,
  'endpoint': <endpoint>,
  'bucket_name': <bucket_name>
  'default_path': <default_path> # used for local path not started with '/'
}
