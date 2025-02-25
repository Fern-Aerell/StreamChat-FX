from print import print_error, print_info
from config import Config
import asyncio
import os

cfgFilePath: str = 'config.json'
cfg: Config = Config()

if __name__ == '__main__':
    try:
        print('YT Live Chat Service')
        print('Versi 2.0.0')
        print('Dibuat oleh Fern Aerell.\n')

        print('Cek apakah ada data yang tersimpan.')
        if os.path.exists(cfgFilePath):
            print('Memuat data yang tersimpan.\n')
            cfg.from_json_file(cfgFilePath)
        else:
            print('Tidak ada data yang tersimpan.\n')

        print_info('Info: Kosongkan input jika ingin menggunakan data yang tersimpan sebelumnya.\n')

        asyncio.run(cfg.input())

        print('Program Selesai.')
    except Exception as error:
        for arg in error.args:
            print_error(arg)
    finally:
        cfg.to_json_file(cfgFilePath)