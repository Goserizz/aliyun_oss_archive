import oss2, sys, os


def percentage(consumed_bytes, total_bytes):
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        print('\r{0}% '.format(rate), end='')
        sys.stdout.flush()


class OSS:

    def __init__(self, access_key_id, access_key_secret, endpoint, bucket_name):
        self.auth = oss2.Auth(access_key_id, access_key_secret)
        self.bucket = oss2.Bucket(self.auth, endpoint, bucket_name)
        self.path = []
        self.objects = dict()
        for obj in oss2.ObjectIterator(self.bucket):
            self.append_object(obj.key)

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
        try:
            os.chdir(path)
        except FileNotFoundError:
            print('No such file or directory.')
            return
        for elem in os.listdir():
            now_path = path + elem
            if os.path.isdir(now_path):
                self.upload_directory(object_name, now_path)
            else:
                self.upload_file(object_name, now_path)

    def upload(self, object_name, path):
        if os.path.isfile(path):
            self.upload_file(object_name, path)
        else:
            self.upload_directory(object_name, path)

    def print_bucket_info(self):
        bucket_info = self.bucket.get_bucket_info()
        print('name: ' + bucket_info.name)
        print('storage class: ' + bucket_info.storage_class)
        print('creation date: ' + bucket_info.creation_date)
        print('intranet_endpoint: ' + bucket_info.intranet_endpoint)
        print('extranet_endpoint ' + bucket_info.extranet_endpoint)
        print('owner: ' + bucket_info.owner.id)
        print('grant: ' + bucket_info.acl.grant)

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
                        print("Invalid path.")
                        return
            if not dic:
                print("Not a directory.")
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
                        print("Invalid path.")
                        return
            if not dic:
                print("Not A Directory.")
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
