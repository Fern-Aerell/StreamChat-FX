from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from flask_socketio import SocketIO
from dataclasses import dataclass
from print import print_info, print_error
from config import Config
from flask import Flask, request
from time import sleep
from threading import Thread

@dataclass
class Service:
    __config: Config

    __browser: Browser
    __browser_context: BrowserContext
    __page: Page

    __app: Flask
    __socket_io: SocketIO

    __host: str = '127.0.0.1'

    __isRunning: bool = False

    def __init__(self, config: Config):
        self.__config = config

        self.__app = Flask('YT Chat Stream')
        self.__app.config['SECRET_KEY'] = 'gZmPpFY0eMIWuU38LYmbXTx9LX0vzhoV/rwKlir8fdg='

        self.__socket_io = SocketIO(self.__app, cors_allowed_origins='*', async_mode='eventlet')

        self.__socket_io.on_event('connect', self.__handle_connect)
        self.__socket_io.on_event('disconnect', self.__handle_disconnect)

    def __handle_connect(self):
        print_info(f'Client {request.sid} connected.')

    def __handle_disconnect(self):
        print_info(f'Client {request.sid} disconnected.')

    @property
    def config(self) -> Config:
        return self.__config

    def __run_browser(self, callback):
        try:
            with sync_playwright() as pw:
                self.__browser = pw.chromium.launch(executable_path=self.__config.browser_path, headless=False)
                self.__browser_context = self.__browser.new_context()
                self.__page = self.__browser_context.new_page()
                self.__page.goto(self.__config.link, wait_until='domcontentloaded')

                self.__page.wait_for_selector('yt-live-chat-text-message-renderer', state='attached')

                callback()

                old_chat = None

                while not self.__page.is_closed():
                    latest_chat = self.__page.evaluate_handle(
                    """
                        () => {
                            const chatItems = document.querySelectorAll('yt-live-chat-text-message-renderer');
                            if (!chatItems.length) return null;

                            const latestItem = chatItems[chatItems.length - 1];
                            if (!latestItem) return null;

                            const name = latestItem.querySelector('#author-name')?.textContent?.trim() || "";
                            const messageElement = latestItem.querySelector('#message');

                            if (!name || !messageElement) return null;

                            let message = "";
                            messageElement.childNodes.forEach(node => {
                                if (node.nodeType === Node.TEXT_NODE) {
                                    message += node.textContent.trim();
                                } else if (node.tagName === 'IMG' && node.classList.contains('emoji')) {
                                    const emojiSrc = node.getAttribute('src');
                                    if (emojiSrc) {
                                        message += `<img src="${emojiSrc}" alt="emoji" class="emoji" style="width:24px; height:24px; vertical-align:middle;" />`;
                                    }
                                }
                            });

                            return message.trim() ? { type: 'default', name, message } : null;
                        }
                    """
                    ).json_value()

                    if latest_chat and (not old_chat or old_chat.get('message') != latest_chat.get('message')):
                        self.__socket_io.emit('latest-chat', latest_chat)
                        old_chat = latest_chat

                    sleep(self.__config.delay / 1000)

        except BaseException as error:
            self.stop()
            for arg in error.args:
                print_error(arg)

    def __run_socket_io(self):
        try:
            self.__socket_io.run(self.__app, host=self.__host, port=self.__config.port)
        except BaseException as error:
            self.stop()
            for arg in error.args:
                print_error(arg)

    def run(self):
        if self.__isRunning:
            return
        
        self.__isRunning = True

        def info():
            print_info(f'Service berjalan pada {self.__host}:{self.__config.port}.')
            print_info('Ctrl + C untuk mengentikan service.')
        
        socket_io_thread = Thread(target=self.__run_socket_io, daemon=True)
        socket_io_thread.start()

        self.__run_browser(callback=info)

    def stop(self):
        if not self.__isRunning:
            return
        
        self.__isRunning = False

        try:
            self.__browser.close()
        except:
            pass

        try:
            self.__socket_io.stop()
        except:
            pass

        print_info('Service berhenti.')