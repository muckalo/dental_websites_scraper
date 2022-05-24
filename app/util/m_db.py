import os
import csv
import chardet


def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        try:
            os.makedirs(folder_path)
        except:
            pass


def detect_encoding(file_path, binary=None):
    if binary:
        read_mode = 'rb'
    else:
        read_mode = 'r'
    with open(file_path, read_mode) as rawdata:
        return chardet.detect(rawdata.read(100000))


def open_data_from_csv(file_path, binary=None, md=True, encoding=None):
    if binary:
        read_mode = 'rb'
    else:
        read_mode = 'r'
    with open(file_path, read_mode, encoding=encoding) as cf:
        data = csv.reader(cf, delimiter=',', quotechar='"')
        if md:
            return [i for i in data]
        else:
            return [i[0] for i in data]


def save_data_to_csv(file_path, data, mode='w', newline="", encoding=None, md=True):
    with open(file_path, mode, newline=newline, encoding=encoding) as cf:
        rw = csv.writer(cf, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if md:
            [rw.writerow(i) for i in data]
        else:
            [rw.writerow([i]) for i in data]


def remove_file_if_exist(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
