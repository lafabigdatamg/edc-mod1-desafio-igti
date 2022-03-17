# Importar biliotecas necessarias
import zipfile
import requests
from io import BytesIO
import os
import threading
import sys
import boto3

# Criar um diretorio para armazenar o conteudo do arquivo
os.makedirs('dados', exist_ok=True)

# Define a url
url = "https://storage.googleapis.com/basedosdados-public/one-click-download/br_me_rais/microdados_vinculos.zip"

# Download do conteudo
filebytes = BytesIO(
    requests.get(url).content
)

# Extrair o conteudo do zpfile
myzip = zipfile.ZipFile(filebytes)
myzip.extractall("dados")

print("Processo de download e extração finalizado!")


# criando thread para validação do processo de uplaoad
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


# Criar um cliente para interagir com o AWS S3
s3_client = boto3.client('s3')

s3_client.upload_file('raw_dados/microdados_vinculos.csv',
                      'igti-eric-rais2020-mod1',
                      'raw/microdados_vinculos.csv',
                      Callback=ProgressPercentage('raw_dados/microdados_vinculos.csv'))

print("Processo de upload para o S3 finalizado!")
