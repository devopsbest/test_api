import os
import shutil

import requests

my_path = os.path.split(os.path.realpath(__file__))[0]

my_folder = "build"

folder = my_path + "/" + my_folder

file_name = folder + "/" + "ec.apk"

print(folder)

url = "https://ec.ef.com.cn/services/oboe2/url?type=Engage2App&partner=Cool&ctr=cn"


def check_folder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)


def is_apk_exist(path):
    if os.path.isfile(path) and path.endswith('apk'):
        print("{file} exist".format(file=path))
        return True

    else:
        print("{file} does't exist".format(file=path))
        return False


def download_file(url, path):
    try:
        file = requests.get(url).content
        with open(path, 'wb') as f:
            f.write(file)
    except:
        print("Download file fail, please check")


def check_ssh(check_file):
    cmd = "openssl sha1 {}".format(check_file)
    os.system(cmd)


if __name__ == '__main__':
    check_folder(folder)
    download_file(url, file_name)
    if is_apk_exist(file_name):
        check_ssh(file_name)
    else:
        print("download fail, please check!")
