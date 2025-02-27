from print import print_error, print_info
from playwright.sync_api import sync_playwright
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
            raise RuntimeError(f'{path} does not exist.')
        
        if not os.path.isfile(path):
            raise RuntimeError(f'{path} is not a file.')

        with open(path, 'r') as file:
            self.from_json(json.load(file))

    def to_json_file(self, path):
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(self.to_json(), file, ensure_ascii=False, indent=4)

    def input(self):
        while True:
            browser_path: str = input(f'Browser {self.browser_path}: ')
            browser_path_length: int = len(browser_path)

            if browser_path_length == 0 and len(self.browser_path) == 0:
                print_error('Browser should not be empty.')
                continue

            if browser_path_length != 0:
                print_info(f'Set browser to {browser_path}.')
                self.browser_path: str = browser_path
            else:
                self.browser_path: str = self.browser_path

            try:
                print_info('Browser verification...')
                with sync_playwright() as pw:
                    browser = pw.chromium.launch(executable_path=self.browser_path)
                    browser.close()
                print_info('Browser can be used.')
            except Exception:
                self.browser_path: str = ''
                print_error('Invalid browser. The browser path may be wrong or the browser may not be Chromium-based.')
                continue

            break

        while True:
            delay: str = input(f'Delay {self.delay}: ')

            if len(delay) != 0:
                self.delay: str = delay

                if not self.delay.isdigit():
                    self.delay = 50
                    print_error('Delay must be an integer.')
                    continue
                
                print_info(f'Set delay to {delay}.')
                self.delay: int = int(self.delay)

            if self.delay < 50:
                self.delay = 50
                print_error('Delay should not be under 50 milliseconds.')
                continue

            break

        while True:
            port: str = input(f'Port {self.port}: ')

            if len(port) != 0:
                self.port: str = port

                if not self.port.isdigit():
                    self.port = 8080
                    print_error('Port must be an integer.')
                    continue

                print_info(f'Set port to {port}.')
                self.port: int = int(self.port)

            break

        while True:
            link: str = input(f'Link {self.link}: ')

            if len(link) == 0 and len(self.link) == 0:
                self.link = ''
                print_error('Link should not be empty.')
                continue

            if len(link) != 0:
                print_info(f'Set link to {link}.')
                self.link: str = link

            self.link: urllib.parse.ParseResult = urllib.parse.urlparse(self.link)
            
            if self.link.hostname != 'www.youtube.com' or self.link.path != '/live_chat':
                self.link = ''
                print_error('Invalid YouTube live chat URL.')
                continue

            link_query_params = urllib.parse.parse_qs(self.link.query)
            if 'v' not in link_query_params or not link_query_params['v']:
                self.link = ''
                print_error('YouTube live chat URL does not a video ID.')
                continue

            self.link: str = urllib.parse.urlunparse(self.link)

            try:
                print_info('Link verification...')
                with sync_playwright() as pw:
                    browser = pw.chromium.launch(executable_path=self.browser_path)
                    browser_context = browser.new_context()
                    page = browser_context.new_page()
                    page.goto(self.link, wait_until='domcontentloaded')
                    page.wait_for_selector('yt-live-chat-text-message-renderer', state='attached')
                    browser.close()
                print_info('Link can be used.')
            except Exception:
                self.link: str = ''
                print_error('YouTube live chat URL is missing or the live stream is over.')
                continue

            break