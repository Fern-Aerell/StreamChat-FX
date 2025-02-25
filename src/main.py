import dataclasses
import json
import os
import urllib
import asyncio
import urllib.parse
import playwright

@dataclasses.dataclass
class Data:
    browserPath: str = ''
    delay: int = 500
    port: int = 8080
    link: str = ''

    def fromJson(self, data: dict):
        for key, default, type in [
            ('browserPath', '', str),
            ('delay', 500, int),
            ('port', 8080, int),
            ('link', '', str),
        ]:
            setattr(self, key, data.get(key, default) if isinstance(data.get(key), type) else default)

    def toJson(self) -> dict:
        return dataclasses.asdict(self)
    
    def fromJsonFile(self, path):
        if os.path.isfile(path):
            with open(path, 'r') as file:
                self.fromJson(json.load(file))

    def toJsonFile(self, path):
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(self.toJson(), file, ensure_ascii=False, indent=4)

    async def input(self):
        while True:
            print(f'Masukkan lokasi file executable browser: {self.browserPath}')
            browserPath: str = input('> ')
            browserPathLength: int = len(browserPath)

            if browserPathLength == 0 and len(self.browserPath) == 0:
                self.browserPath: str = ''
                print('\033[31mFile executable tidak boleh kosong.\033[0m')
                continue

            if browserPathLength != 0:
                print(f'Mengatur lokasi file executable browser menjadi {browserPath}.')
                self.browserPath: str = browserPath
            else:
                self.browserPath: str = self.browserPath

            try:
                async with playwright.async_api.async_playwright() as p:
                    browser = await p.chromium.launch(executable_path=self.browserPath)
                    await browser.close()
            except Exception:
                self.browserPath: str = ''
                print('\033[31mFile executable browser tidak valid.\033[0m')
                continue

            break

        while True:
            print(f'Masukkan delay: {self.delay}')
            delay: str = input('> ')

            if len(delay) != 0:
                self.delay: str = delay

                if not self.delay.isdigit():
                    self.delay = 500
                    print('\033[31mDelay harus sebuah bilangan.\033[0m')
                    continue
                
                print(f'Mengatur delay menjadi {delay}.')
                self.delay: int = int(self.delay)

            if self.delay < 500:
                self.delay = 500
                print('\033[31mDelay tidak boleh dibawah 500 milidetik.\033[0m')
                continue

            break

        while True:
            print(f'Masukkan port: {self.port}')
            port: str = input('> ')

            if len(port) != 0:
                self.port: str = port

                if not self.port.isdigit():
                    self.port = 8080
                    print('\033[31mPort harus sebuah bilangan.\033[0m')
                    continue

                print(f'Mengatur port menjadi {port}.')
                self.port: int = int(self.port)

            break

        while True:
            print(f'Masukkan link: {self.link}')
            link: str = input('> ')

            if len(link) == 0 and len(self.link) == 0:
                self.link = ''
                print('\033[31mLink tidak boleh kosong.\033[0m')
                continue

            if len(link) != 0:
                print(f'Mengatur link menjadi {link}.')
                self.link: str = link

            self.link: urllib.parse.ParseResult = urllib.parse.urlparse(self.link)
            
            if self.link.hostname != 'www.youtube.com' or self.link.path != '/live_chat':
                self.link = ''
                print('\033[31mLink bukan url youtube live chat yang valid.\033[0m')
                continue

            link_query_params = urllib.parse.parse_qs(self.link.query)
            if 'v' not in link_query_params or not link_query_params['v']:
                self.link = ''
                print('\033[31mLink youtube live char tidak memiliki video id.\033[0m')
                continue

            self.link: str = urllib.parse.urlunparse(self.link)

            break

dataFilePath: str = 'data.json'
data: Data = Data()

if __name__ == '__main__':
    try:
        print('YT Live Chat Service')
        print('Versi 2.0.0')
        print('Dibuat oleh Fern Aerell.\n')

        print('Cek apakah ada data yang tersimpan.')
        if os.path.exists(dataFilePath):
            print('Memuat data yang tersimpan.\n')
            data.fromJsonFile(dataFilePath)
        else:
            print('Tidak ada data yang tersimpan.\n')

        print('Info: Kosongkan input jika ingin menggunakan data yang tersimpan sebelum nya.\n')

        asyncio.run(data.input())
    except Exception as error:
        for arg in error.args:
            print(f'\033[31m{arg}\033[0m')
    finally:
        data.toJsonFile(dataFilePath)