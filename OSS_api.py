import oss2, sys, os


def print_err(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def percentage(consumed_bytes, total_bytes):
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        print('\r{0}% '.format(rate), end='')
        sys.stdout.flush()


class OSS:

    def __init__(self, access_key_id, access_key_secret, endpoint, bucket_name, default_path):
        print('connecting to server...')
        self.auth = oss2.Auth(access_key_id, access_key_secret)
        self.bucket = oss2.Bucket(self.auth, endpoint, bucket_name)
        print('connected.')
        if not default_path.endswith('/'):
            self.default_path = default_path + '/'
        else:
            self.default_path = default_path
        self.path = []
        self.objects = dict()
        print('Downloading catalogs...')
        for obj in oss2.ObjectIterator(self.bucket):
            self.append_object(obj.key)
        print('Downloaded.\n')
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
        print(path)
        self.bucket.put_object_from_file(object_name, path, progress_callback=percentage)
        print('')
        self.append_object(object_name)

    def upload_directory(self, object_name, path):
        if not path.endswith('/'):
            if object_name:
                object_name = object_name + '/' + os.path.basename(path)
            else:
                object_name = os.path.basename(path)
            path += '/'
        os.chdir(path)
        for elem in os.listdir():
            now_path = path + elem
            if os.path.isdir(now_path):
                self.upload_directory(object_name, now_path)
            else:
                self.upload_file(object_name, now_path)

    def upload(self, object_name, path):
        if not path.startswith('/'):
            path = self.default_path + path
        if os.path.isfile(path):
            self.upload_file(object_name, path)
        else:
            try:
                os.chdir(path)
            except FileNotFoundError:
                print_err('No such file or directory.')
                return
            self.upload_directory(object_name, path)

    def download_file(self, object_name, path):
        print(path)
        self.bucket.get_object_to_file(object_name, path, progress_callback=percentage)
        print('')

    def download_dir(self, dic, object_name, path):
        if not os.path.exists(path):
            os.mkdir(path)
        for _slice in dic.keys():
            if dic[_slice]:
                now_name = object_name.copy()
                now_name.append(_slice)
                self.download_dir(dic[_slice], now_name, path + '/' + _slice)
            else:
                self.download_file('/'.join(object_name) + '/' + _slice, path + '/' + _slice)

    def download(self, object_name, path):
        dic = self.objects
        now_name = []
        if not path.startswith('/'):
            path = self.default_path + path
        if os.path.isfile(path):
            print_err('Invalid local path.', file=sys.stderr)
            return
        if path.endswith('/'):
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
            self.download_dir(dic, now_name, path + '/' + now_name[-1])
        else:
            self.download_file('/'.join(now_name), path + '/' + now_name[-1])

    def print_bucket_info(self):
        print('name: ' + self.bucket_info.name)
        print('storage class: ' + self.bucket_info.storage_class)
        print('creation date: ' + self.bucket_info.creation_date)
        print('intranet_endpoint: ' + self.bucket_info.intranet_endpoint)
        print('extranet_endpoint ' + self.bucket_info.extranet_endpoint)
        print('owner: ' + self.bucket_info.owner.id)
        print('grant: ' + self.bucket_info.acl.grant)

    def print_dir(self):
        dic = self.objects
        for _slice in self.path:
            dic = dic[_slice]
        for elem in dic:
            if dic[elem]:
                print(elem + '/')
            else:
                print(elem)

    def change_directory(self, directory):
        if self.path:
            if directory == '..':
                self.path.remove(self.path[len(self.path) - 1])
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
        new_name = []
        for _slice in self.path:
            dic = dic[_slice]
            new_name.append(_slice)
        for _slice in object_name.split('/'):
            if _slice:
                if _slice in dic:
                    old = dic
                    old_slice = _slice
                    dic = dic[_slice]
                    new_name.append(_slice)
                else:
                    print('Invalid Path')
                    return
        self.remove_directory_file(dic, new_name)
        old.pop(old_slice)

    def now_path(self):
        return '/'.join(self.path)
