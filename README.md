# Aliyun OSS Archive
### Basic Operations:

>dir: show current dir's contents  

usage: >dir

>cd: change directory  

usage: >cd &lt;dir>  

>ul: upload directory or file to current remote dir  

usage: ul &lt;remote_path> &lt;local_path>  

>rm: remove directory or file 

usage: rm &lt;remote_path>


>dl: download directory or file from remote to local  

usage: dl &lt;remote_path> &lt;local_path>

>info: get infomation about current server  

usage: info

### Configuration File: config.json  

* 'access_key_id': <access_key_id>,  
* 'access_key_secret': <access_key_secret>,  
* 'endpoint': <endpoint>,  
* 'bucket_name': <bucket_name>,  
* 'default_path': <default_path> # used for local path not started with '/'
