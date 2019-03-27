import json
import os
import sys
import platform
import oss2
from termcolor import colored


os_name = platform.system()
slash = os.sep


def print_err(*args, **kwargs):
    if os_name != 'Windows':
        print(colored(*args, 'red'), file=sys.stderr, **kwargs)
    else:
        print(*args, **kwargs)


def print_folder(*args, **kwargs):
    if os_name != 'Windows':
        print(colored(*args, 'yellow'), **kwargs)
    else:
        print(*args, **kwargs)


def input_confirm(*args):
    tf = ''
    while tf != 't' and tf != 'f':
        if os_name != 'Windows':
            tf = input(colored(*args, 'green'))
        else:
            tf = input(*args)
    if tf == 't':
        return True
    else:
        return False


def print_info(*args, **kwargs):
    if os_name != 'Windows':
        print(colored(*args, 'cyan'), **kwargs)
    else:
        print(*args, **kwargs)


def percentage(consumed_bytes, total_bytes):
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        print_info('\r{0}% '.format(rate), end='')
        sys.stdout.flush()


def is_abs_add(address):
    if os_name == 'Darwin' or os_name == 'Linux':
        if address.startswith('/'):
            return True
        else:
            return False
    else:
        if address[1:3] == ':\\':
            return True
        else:
            return False


def get_config_path():
    if os_name == 'Darwin' or os_name == 'Linux':
        return '/etc/oss/config.json'
    elif os_name == 'Windows':
        return os.getcwd() + '//config.json'
    else:
        print_err('What the hell os you are using?')
        return


class OSS:

    def __init__(self, access_key_id, access_key_secret, endpoint, bucket_name, default_path):
        self.config_path = get_config_path()
        self.auth = oss2.Auth(access_key_id, access_key_secret)
        self.bucket = oss2.Bucket(self.auth, endpoint, bucket_name)
        if not default_path.endswith(slash):
            self.default_path = default_path + slash
        else:
            self.default_path = default_path
        self.path = []
        self.objects = dict()
        print_info('Downloading catalogs...')
        for obj in oss2.ObjectIterator(self.bucket):
            self.append_object(obj.key)
        print_info('Downloaded.\n')
        self.bucket_info = self.bucket.get_bucket_info()

    def append_object(self, object_name):
        dic = self.objects
        for _slice in object_name.split('/'):
            if _slice:
                if _slice in dic.keys():
                    dic = dic[_slice]
                else:
                    dic[_slice] = dict()
                    dic = dic[_slice]

    def upload_file(self, object_name, path):
        if object_name:
            object_name = object_name + '/' + os.path.basename(path)
        else:
            object_name = os.path.basename(path)
        print_info(path)
        self.bucket.put_object_from_file(object_name, path, progress_callback=percentage)
        print('')
        self.append_object(object_name)

    def upload_directory(self, object_name, path):
        if not path.endswith(slash):
            if object_name:
                object_name = object_name + slash + os.path.basename(path)
            else:
                object_name = os.path.basename(path)
            path += slash
        os.chdir(path)
        for elem in os.listdir():
            now_path = path + elem
            if os.path.isdir(now_path):
                self.upload_directory(object_name, now_path)
            else:
                self.upload_file(object_name, now_path)

    def upload(self, object_name, path):
        if not is_abs_add(path):
            path = self.default_path + path
        if not object_name.startswith('/') and self.now_path():
            object_name = self.now_path() + '/' + object_name
        if os.path.isfile(path):
            self.upload_file(object_name, path)
        else:
            try:
                os.chdir(path)
            except FileNotFoundError:
                print_err('No such file or directory.')
                return
            except OSError:
                print_err('Invalid grammar.')
                return
            self.upload_directory(object_name, path)

    def download_file(self, object_name, path):
        print_info(path)
        self.bucket.get_object_to_file(object_name, path, progress_callback=percentage)
        print('')

    def download_dir(self, dic, object_name, path):
        if not os.path.exists(path):
            os.mkdir(path)
        for _slice in dic.keys():
            if dic[_slice]:
                now_name = object_name.copy()
                now_name.append(_slice)
                self.download_dir(dic[_slice], now_name, path + slash + _slice)
            else:
                self.download_file('/'.join(object_name) + '/' + _slice, path + slash + _slice)

    def download(self, object_name, path):
        dic = self.objects
        now_name = []
        if not is_abs_add(path):
            path = self.default_path + path
        if os.path.isfile(path):
            print_err('Invalid local path.', file=sys.stderr)
            return
        if path.endswith(slash):
            path = path[0:len(path)-1]
        try:
            os.chdir(path)
        except FileNotFoundError:
            print_err('Invalid local path.')
            return
        if not object_name.startswith('/'):
            for _slice in self.path:
                dic = dic[_slice]
                now_name.append(_slice)
        for _slice in object_name.split('/'):
            if _slice:
                if _slice in dic.keys():
                    dic = dic[_slice]
                    now_name.append(_slice)
                else:
                    print_err('Invalid remote path.')
                    return
        if dic:
            self.download_dir(dic, now_name, path + slash + now_name[-1])
        else:
            self.download_file('/'.join(now_name), path + slash + now_name[-1])

    def print_bucket_info(self):
        print_info('name: ' + self.bucket_info.name)
        print_info('storage class: ' + self.bucket_info.storage_class)
        print_info('creation date: ' + self.bucket_info.creation_date)
        print_info('intranet_endpoint: ' + self.bucket_info.intranet_endpoint)
        print_info('extranet_endpoint ' + self.bucket_info.extranet_endpoint)
        print_info('owner: ' + self.bucket_info.owner.id)
        print_info('grant: ' + self.bucket_info.acl.grant)

    def print_dir(self):
        dic = self.objects
        for _slice in self.path:
            dic = dic[_slice]
        for elem in dic:
            if dic[elem]:
                print_folder(elem + '/')
            else:
                print(elem)

    def change_directory(self, directory):
        if self.path:
            if directory == '..':
                self.path.remove(self.path[len(self.path) - 1])
                return
        if directory == '~':
            self.path = []
            return
        dic = self.objects
        temp = []
        if directory.startswith('/'):
            for _slice in directory.split('/'):
                if _slice != '':
                    if _slice in dic.keys():
                        dic = dic[_slice]
                        temp.append(_slice)
                    else:
                        print_err("Invalid path.")
                        return
            if not dic:
                print_err("Not a directory.")
                return
        else:
            dic = self.objects
            for _slice in self.path:
                dic = dic[_slice]
                temp.append(_slice)
            for _slice in directory.split('/'):
                if _slice != '':
                    if _slice in dic.keys():
                        dic = dic[_slice]
                        temp.append(_slice)
                    else:
                        print_err("Invalid path.")
                        return
            if not dic:
                print_err("Not A Directory.")
                return
        self.path = temp

    def remove_directory_file(self, dic, object_name):
        for _slice in dic.keys():
            if dic[_slice]:
                self.remove_directory_file(dic[_slice], object_name + [_slice, ])
            else:
                self.bucket.delete_object('/'.join(object_name) + '/' + _slice)
        self.bucket.delete_object('/'.join(object_name))

    def remove(self, object_name):
        dic = self.objects
        remote_name = []
        if not object_name.startswith('/'):
            for _slice in self.path:
                dic = dic[_slice]
                remote_name.append(_slice)
        for _slice in object_name.split('/'):
            if _slice:
                if _slice in dic:
                    last_dic = dic
                    last_slice = _slice
                    dic = dic[_slice]
                    remote_name.append(_slice)
                else:
                    print_err('Invalid Path')
                    return
        self.remove_directory_file(dic, remote_name)
        last_dic.pop(last_slice)

    def now_path(self):
        return '/'.join(self.path)

    def sync(self, sync_file):
        with open(self.config_path, 'r') as f:
            load_dic = json.load(f)
        if not 'files' in load_dic.keys():
            return
        files = load_dic['files']
        if not sync_file:
            if not input_confirm('Are you sure to start sync?(t/f)'):
                return
            for file in files.keys():
                self.upload(files[file], file)
        else:
            if not is_abs_add(sync_file):
                sync_file = self.default_path + sync_file
            if not sync_file in files.keys():
                print_err('No such sync file. Check your spelling or use <set>.')
            else:
                if not input_confirm('Are you sure to start sync?(t/f)'):
                    return
                self.upload(files[sync_file], sync_file)

    def set_sync(self, path, remote_path):
        with open(self.config_path, 'r') as f:
            load_dic = json.load(f)
        if not 'files' in load_dic.keys():
            load_dic['files'] = {}
        files = load_dic['files']
        if not is_abs_add(path):
            path = self.default_path + path
        if not os.path.isfile(path):
            try:
                os.chdir(path)
            except FileNotFoundError:
                print_err('No such file or directory.')
                return
        if remote_path.startswith('/'):
            remote_path = remote_path[1:]
        else:
            remote_path = self.now_path() + '/' + remote_path
        if path in files.keys() and files[path] != remote_path:
            if input_confirm(path + ' is already exist. Are you sure to change its remote path(' + files[path] + ')?(t/f)'):
                files[path] = remote_path
        else:
            files[path] = remote_path
        with open(self.config_path, 'w') as f:
            json.dump(load_dic, f)
        if not remote_path:
            remote_path = '/'
        print_info('<local>' + path + ' <remote>' + remote_path)

    def disable_sync(self, path):
        with open(self.config_path, 'r') as f:
            load_dic = json.load(f)
        if not 'files' in load_dic:
            print_err('No sync file found. Try to use <set>.')
        else:
            if not is_abs_add(path):
                path = self.default_path + path
            if not path in load_dic['files']:
                print_err('No such sync file. Check your spelling or use <set>.')
            else:
                if input_confirm('You are trying to disable <local>:' + path + ' <remote>:' + load_dic['files'][path] + '. Are you sure?(t/f)'):
                    load_dic['files'].pop(path)
        with open(self.config_path, 'w') as f:
            json.dump(load_dic, f)

    def print_sync_info(self):
        with open(self.config_path, 'r') as f:
            load_dic = json.load(f)
        if 'files' in load_dic:
            for file in load_dic['files'].keys():
                print_info('<local>: ' + file + ' <remote>: ' + load_dic['files'][file])
        else:
            print_err('No sync file found. Try to use <set>.')

    def refresh(self):
        self.objects = {}
        print_info('refreshing catalogs...')
        for obj in oss2.ObjectIterator(self.bucket):
            self.append_object(obj.key)
        print_info('refreshed.')
