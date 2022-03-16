import boto3
import os
import sys
import threading


# Variaveis
bucket = 'igti-eric-rais2020-mod1'

s3 = boto3.client('s3')


class ProgressPercentage(object):

    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()


def aws_upload_raw():
    lista_arquivos = os.listdir('raw_dados')
    for file in lista_arquivos:
        s3.upload_file(
            f'raw_dados/{file}', bucket, f'raw/{file}',
            Callback=ProgressPercentage(f'raw_dados/{file}')
        )
