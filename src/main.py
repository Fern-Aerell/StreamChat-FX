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
        print('StreamChat FX')
        print('Version: 2.0.0')
        print('Create By: Fern Aerell.\n')

        print('Check whether saved data exists.')
        if os.path.exists(cfgFilePath):
            print('Load saved data.\n')
            service.config.from_json_file(cfgFilePath)
        else:
            print('Saved data does not exist.\n')

        print_info('Info: Empty the input if you want to use previously saved data.\n')

        service.config.input()
        service.run()
    except BaseException as error:
        for arg in error.args:
            print_error(arg)
    finally:
        service.stop()
        service.config.to_json_file(cfgFilePath)