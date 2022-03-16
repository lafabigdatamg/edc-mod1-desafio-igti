from ftplib import FTP
from aws_python import aws_upload_raw
import py7zr
import os
import progressbar as pb


# Função de escrita do arquivo e atualização da progressbar
def file_write(data):
    file.write(data)
    global pbar
    pbar += len(data)


# Baixar os dados contidos no FTP para a pasta zip_dados
ftp = FTP(host="ftp.mtps.gov.br")
ftp.login()
ftp.cwd("/pdet/microdados/RAIS/2020")
lista_dados = ftp.nlst()
for i in lista_dados:
    if not "RAIS_ESTAB_PUB.7z" in i:
        file = open(f'zip_dados/{i}', 'wb')
        size = ftp.size(i)
        widgets = [f'Baixando {i}: ', pb.Percentage(), ' ',
                   pb.Bar(marker='#', left='[', right=']'),
                   ' ', pb.ETA(), ' ', pb.FileTransferSpeed()]
        pbar = pb.ProgressBar(widgets=widgets, maxval=size)
        pbar.start()
        ftp.retrbinary(f'RETR {i}', file_write)
ftp.quit()


# Descompactando arquivos
arquivos_descompactar = os.listdir('zip_dados')
for file in arquivos_descompactar:
    print(f"Descompactando {file}")
    archive = py7zr.SevenZipFile(f'zip_dados/{file}', mode='r')
    archive.extractall(path="raw_dados")
    archive.close()
    print(f"Processo concluído")


# Executa o uploading dos dados para o S3
aws_upload_raw()
