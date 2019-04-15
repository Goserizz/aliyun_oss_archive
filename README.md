# Aliyun OSS Archive
### Use Shell:
>python shell.py

### Basic Operations:

>dir: show current dir's contents  

usage: dir

>cd: change directory

usage: cd &lt;dir>  

>ul: upload directory or file to current remote dir  

usage: ul &lt;remote_path> &lt;local_path>  

usage: ul <local_path>  // upload to cwd

>rm: remove directory or file 

usage: rm &lt;remote_path>


>dl: download directory or file from remote to local  

usage: dl &lt;remote_path> &lt;local_path>

usage: dl <remote_path>  // download to 'defualt_path'(config.json)

>info: get infomation about current server  

usage: info

> set: set connection between local path and remote path

usage: set <local_path>  // connect <local_path> with cwd

usage: set <local_path> <remote_path>

> push/pull : synchronize connected files in 'files'(config.json)

usage: push/pull  // synchronize all

usage: push/pull <local_path>  // push/pull <local_path> to remote if it's in 'files'(config.json)

> sync-info: print all connections in 'files'(config.json)

usage: sync-info

> dis: disable connection in 'files'(config.json)

usage: dis <local_path>  // disable connections with <local_path> and its remote if it's in 'files'(config.json)

> help: get usage information

usage: help

> quit: quit

usage: quit

> refresh: sync contents with remote

usage: f5

> file info: get file info from remote

usage: finfo <remote_path>

### Configuration File: config.json  

* 'access_key_id': <access_key_id>,  
* 'access_key_secret': <access_key_secret>,  
* 'endpoint': <endpoint>,  
* 'bucket_name': <bucket_name>,  
* 'default_path': <default_path>  // used for local path not started with '/'
* 'files': {<local_path>: <remote_path>, …, <local_path>: <remote_path>}  // connections between local file and remote file, can be set/disabled in shell. Used in synchronizing.

### Files

- 'shell.py': Interactive bash-like program
- 'manage.py': Used for executing one command a time
- 'command.py': Aconnector between program and terminal, use 'oss' to start shell.py or 'oss &lt;command&gt;' to start manage.py
- 'OSS_api.py': More usable api generated from oss2 
- md5.py: Used to calculate md5 of local files