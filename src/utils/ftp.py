from ftplib import FTP
import datetime
from conf.settings import MEDIA_ROOT
import os
from django.core.files.storage import default_storage
import csv
from dynaconf import settings
from os import listdir
from os.path import isfile, join
import io
from parts.models import Part

csv_folder = os.path.join(MEDIA_ROOT, 'import-csv')

def connect_to_ftp():
    '''
        Берет параметры для подключения из settings:
        settings.FTP_HOST, settings.FTP_USER, settings.FTP_PASS
    '''
    try:
        ftp = FTP(settings.FTP_HOST, settings.FTP_USER, settings.FTP_PASS) # connect to the FTP server
        ftp.encoding = "utf-8" # force UTF-8 encoding
        print('Connection established')
        return ftp
    except:
        print('Connection faild')
        return False

def close_ftp(ftp):
    ftp.quit()

def set_filename():
    now = datetime.datetime.now()
    time_stamp = now.strftime("%d-%m-%Y_%H:%M") # %d-%m-%Y-%H:%M
    return f'parts-{time_stamp}.csv'

def get_csv_from_ftp(ftp): 
    local_filename = set_filename()

    if remote_file_is_exist(ftp):
        with open(os.path.join(csv_folder, local_filename), "wb") as file:
            ftp.retrbinary(f"RETR {settings.REMOTE_CSV_FILE}", file.write)
            # clean_remote_file(ftp, settings.REMOTE_CSV_FILE)
    else:
        return False

def clean_remote_file(ftp, filename):
    with open(filename, 'rb') as localfile:
        ftp.storbinary('STOR ' + filename, localfile)
    print('upload ' + filename)

def remote_file_is_exist(ftp):
    _remote_files_list = []
    ftp.retrlines('NLST', _remote_files_list.append)
    if settings.REMOTE_CSV_FILE in _remote_files_list:
        return True

# def show_file_data(file):
#     data = []

#     with open(os.path.join(csv_folder, file), "r", encoding='utf-8') as f:
#         reader = csv.reader(f, delimiter=';')
#         for row in reader:
#             print(row)
#             data.append(row)
#     return data

def get_data_from_csv(filename, delimiter=';'):
    data = []
    f = default_storage.open(os.path.join(csv_folder, filename), 'r')
    reader = csv.reader(f, delimiter=delimiter)
    #next(reader)
    for row in reader:
        data.append(row)
    f.close()
    
    return data

# ftp_connection = connect_to_ftp()
# get_csv_from_ftp(ftp_connection)
# close_ftp(ftp_connection)

def handle_uploaded_csv_file(f):
    # with open(f"{os.path.join(MEDIA_ROOT, 'upload-csv')}/file.csv", 'wb+') as destination:
    local_filename = set_filename()
    with open(os.path.join(csv_folder, local_filename), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return local_filename

def take_files_form_csv_folder():
    myfiles = [f for f in listdir(csv_folder) if isfile(join(csv_folder, f))]
    return myfiles

def import_parts(filename):
    '''
    Create parts from local csv file
    '''
    data = get_data_from_csv(filename)
    for row in data:
        if row[0] and row[1] and row[2]:
            _, created = Part.objects.get_or_create(
                vin = row[0],
                code = row[1],
                name = row[2],
                #unit = row[3],
                #count = row[4],
                )
