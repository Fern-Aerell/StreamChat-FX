from eventlet import monkey_patch
monkey_patch()

from print import print_error, print_info
from service import Service
from config import Config
import os

cfgFilePath: str = 'config.json'
service: Service = Service(Config())

if __name__ == '__main__':
    try:
        print('YT Live Chat Service')
        print('Versi 2.0.0')
        print('Dibuat oleh Fern Aerell.\n')

        print('Cek apakah ada data yang tersimpan.')
        if os.path.exists(cfgFilePath):
            print('Memuat data yang tersimpan.\n')
            service.config.from_json_file(cfgFilePath)
        else:
            print('Tidak ada data yang tersimpan.\n')

        print_info('Info: Kosongkan input jika ingin menggunakan data yang tersimpan sebelumnya.\n')

        service.config.input()
        service.run()
    except BaseException as error:
        for arg in error.args:
            print_error(arg)
    finally:
        service.stop()
        service.config.to_json_file(cfgFilePath)