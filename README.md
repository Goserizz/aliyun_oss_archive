# Aliyun OSS Archive
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

> sync: synchronize connected files in 'files'(config.json)

usage: sync  // synchronize all

usage: sync <local_path>  // sync <local_path> to remote if it's in 'files'(config.json)

> sync-info: print all connections in 'files'(config.json)

usage: sync-info

> dis: disable connection in 'files'(config.json)

usage: dis <local_path>  // disable connections with <local_path> and its remote if it's in 'files'(config.json)

> help: get usage information

usage: help

> quit: quit

usage: quit

### Configuration File: config.json  

* 'access_key_id': <access_key_id>,  
* 'access_key_secret': <access_key_secret>,  
* 'endpoint': <endpoint>,  
* 'bucket_name': <bucket_name>,  
* 'default_path': <default_path>  // used for local path not started with '/'
* 'files': {<local_path>: <remote_path>, …, <local_path>: <remote_path>}  // connections between local file and remote file, can be set/disabled in shell. Used in synchronizing.
