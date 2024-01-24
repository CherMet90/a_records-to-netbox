import csv
import os

from custom_modules.log import logger
from custom_modules.netbox_connector import NetboxDevice
from custom_modules.error_handling import print_errors
from custom_modules.errors import Error, NonCriticalError


class Record:
    def __init__(self, zone, name, ip_address):
        # Формирование FQDN
        self.zone = zone
        self.name = name
        if name == '@':
            self.fqdn = zone
        else:
            self.fqdn = f'{name}.{zone}'
        
        # Получение IP-адреса с указанием длины префикса
        self.ip_address = ip_address
        self.netbox_prefix = NetboxDevice.get_prefix_for_ip(ip_address)
        self.ip_with_prefix = f'{ip_address}/{self.netbox_prefix.prefix.split("/")[1]}'


NetboxDevice.create_connection()

# Чтение csv-файлов из папки input
csv_folder = "input"
csv_files = [file for file in os.listdir(csv_folder) if file.endswith(".csv")]
for file in csv_files:
    file_path = os.path.join(csv_folder, file)
    with open(file_path, "r", encoding='UTF-8') as csv_file:
        logger.info(f"Reading file: {file_path}")
        csv_content = csv.DictReader(csv_file, delimiter=',')
        logger.info('=' * 50)
        logger.info(f'Zone {file} parsing')
        for row in csv_content:
            try:
                # Парсим
                record = Record(
                    zone = file.split('.csv')[0],
                    name = row['HostName'],
                    ip_address = row['RecordData'],
                )
                # Вносим данные в Netbox
                NetboxDevice.create_ip_address(
                    record.ip_address,
                    record.ip_with_prefix,
                    dns_name=record.fqdn
                )
            except Error:
                continue
        logger.debug(f'Zone {file} was processed')
# Вывод ошибок, возникших в процессе работы
print_errors()