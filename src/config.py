from print import print_error, print_info
from playwright.async_api import async_playwright
from dataclasses import dataclass, asdict
import urllib
import json
import os

@dataclass
class Config:
    browser_path: str = ''
    delay: int = 50
    port: int = 8080
    link: str = ''

    def from_json(self, data: dict):
        for key, default, type in [
            ('browser_path', '', str),
            ('delay', 50, int),
            ('port', 8080, int),
            ('link', '', str),
        ]:
            setattr(self, key, data.get(key, default) if isinstance(data.get(key), type) else default)

    def to_json(self) -> dict:
        return asdict(self)
    
    def from_json_file(self, path):
        if not os.path.exists(path):
            raise RuntimeError(f'{path} tidak ada.')
        
        if not os.path.isfile(path):
            raise RuntimeError(f'{path} bukan file.')

        with open(path, 'r') as file:
            self.from_json(json.load(file))

    def to_json_file(self, path):
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(self.to_json(), file, ensure_ascii=False, indent=4)

    async def input(self):
        while True:
            browser_path: str = input(f'Browser {self.browser_path}: ')
            browser_path_length: int = len(browser_path)

            if browser_path_length == 0 and len(self.browser_path) == 0:
                self.browser_path: str = ''
                print_error('Lokasi file executable browser tidak boleh kosong.')
                continue

            if browser_path_length != 0:
                print_info(f'Mengatur lokasi file executable browser menjadi {browser_path}.')
                self.browser_path: str = browser_path
            else:
                self.browser_path: str = self.browser_path

            try:
                async with async_playwright() as pw:
                    browser = await pw.chromium.launch(executable_path=self.browser_path)
                    await browser.close()
            except Exception:
                self.browser_path: str = ''
                print_error('File executable browser tidak valid.')
                continue

            break

        while True:
            delay: str = input(f'Delay {self.delay}: ')

            if len(delay) != 0:
                self.delay: str = delay

                if not self.delay.isdigit():
                    self.delay = 50
                    print_error('Delay harus sebuah bilangan.')
                    continue
                
                print_info(f'Mengatur delay menjadi {delay}.')
                self.delay: int = int(self.delay)

            if self.delay < 50:
                self.delay = 50
                print_error('Delay tidak boleh dibawah 50 milidetik.')
                continue

            break

        while True:
            port: str = input(f'Port {self.port}: ')

            if len(port) != 0:
                self.port: str = port

                if not self.port.isdigit():
                    self.port = 8080
                    print_error('Port harus sebuah bilangan.')
                    continue

                print_info(f'Mengatur port menjadi {port}.')
                self.port: int = int(self.port)

            break

        while True:
            link: str = input(f'Link {self.link}: ')

            if len(link) == 0 and len(self.link) == 0:
                self.link = ''
                print_error('Link tidak boleh kosong.')
                continue

            if len(link) != 0:
                print_info(f'Mengatur link menjadi {link}.')
                self.link: str = link

            self.link: urllib.parse.ParseResult = urllib.parse.urlparse(self.link)
            
            if self.link.hostname != 'www.youtube.com' or self.link.path != '/live_chat':
                self.link = ''
                print_error('Link bukan url youtube live chat yang valid.')
                continue

            link_query_params = urllib.parse.parse_qs(self.link.query)
            if 'v' not in link_query_params or not link_query_params['v']:
                self.link = ''
                print_error('Link youtube live char tidak memiliki video id.')
                continue

            self.link: str = urllib.parse.urlunparse(self.link)

            break