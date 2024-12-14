import { validateYoutubeLiveChatLink, validateBrowserExecutablePath } from './validates';
import { getAvailablePort, isPortAvailable, MAX_PORT_NUMBER, MIN_PORT_NUMBER } from './port';
import { Server } from 'socket.io';
import { chromium } from 'playwright';
import input from '@inquirer/input';
import process from 'process';
import { loadJsonData, saveJsonData } from './jsondata';

interface SaveDataType {
    browserPath: string;
    delay: string;
    port: string;
    headless: string;
    link: string;
}

(async () => {
    console.info('Leva YT Live Chat Service\n');

    // Load saved configuration data if available
    const savedData = loadJsonData('savedata') as SaveDataType | null;

    // Get browser executable path from user
    let browserPath: string;

    try {
        browserPath = await input({
            message: 'Enter the browser executable path:',
            required: true,
            default: savedData?.browserPath,
            transformer: (value) => value.replace(/\\/g, '/'), // Normalize path for cross-platform compatibility
            validate: validateBrowserExecutablePath
        });
    } catch (error) {
        return;
    }

    // Get delay time from user and validate input
    let delay: number;

    try {
        delay = parseInt(await input({
            message: 'Enter update delay in milliseconds:',
            required: true,
            default: savedData?.delay || '500',
            validate: (value) => {
                const delayValue = parseInt(value);
                if (isNaN(delayValue)) return 'The update delay must be a number.';
                if (delayValue < 500) return 'The update delay must not be below 500 milliseconds.';
                return true;
            }
        }));
    } catch (error) {
        return;
    }

    // Get port from user and validate input
    let port: string | number

    try {
        port = await input({
            message: 'Enter the port:',
            required: true,
            default: savedData?.port || MIN_PORT_NUMBER.toString(),
            validate: async (value) => {
                if (value === 'random') return true;
                const portValue = parseInt(value);
                if (isNaN(portValue)) return 'The port must be a number.';
                if (portValue < MIN_PORT_NUMBER || portValue > MAX_PORT_NUMBER) {
                    return `The port number must be between ${MIN_PORT_NUMBER} and ${MAX_PORT_NUMBER}.`;
                }
                if (!(await isPortAvailable(portValue))) {
                    return 'The port is already in use.';
                }
                return true;
            }
        });
    } catch (error) {
        return;
    }

    // If "random" is selected, get an available port
    port = port === 'random' ? await getAvailablePort() : parseInt(port);

    // Get the Headless value
    let headless: string | boolean;

    try {
        /**
         * Prompt the user to input the headless value.
         * - The input must be either "true" or "false".
         * - If no input is provided, the default value is taken from `savedData.headless` or set to "true".
         * - Validation ensures the input is valid ("true" or "false").
         */
        headless = await input({
            message: 'Please enter a value for headless (true or false):', // Prompt message for the user
            required: true, // The input is mandatory
            default: savedData?.headless || 'true', // Use saved value or default to "true"
            validate: (value) => {
                /**
                 * Validation function:
                 * - Ensures the input is either "true" or "false".
                 * - Returns an error message if the input is invalid.
                 */
                if (value != 'true' && value != "false") {
                    return 'The headless value must be either "true" or "false".'; // Error message shown to the user
                }
                return true; // Input is valid
            }
        });
    } catch (error) {
        // Exit gracefully if an error occurs (e.g., user cancels the input).
        return;
    }

    // Convert the input string ("true" or "false") to a boolean value.
    headless = headless == 'true' ? true : false;

    // Get YouTube live chat link from user
    let link: string;

    try {
        link = await input({
            message: 'Enter the YouTube live chat link:',
            required: true,
            default: savedData?.link,
            validate: validateYoutubeLiveChatLink
        });
    } catch (error) {
        return;
    }

    // Save configuration data
    saveJsonData('savedata', { browserPath, delay: delay.toString(), port: port.toString(), link, headless: `${headless}` });

    // Initialize Socket.IO server
    const io = new Server(port, {
        cors: {
            origin: '*',
            methods: ["GET", "POST"],
        }
    });
    console.info(`\nService running on port: ${port}`);

    // Launch Playwright browser
    const browser = await chromium.launch({ headless: headless, executablePath: browserPath });
    const context = await browser.newContext();
    const page = await context.newPage();
    await page.goto(link, { waitUntil: 'domcontentloaded' });

    // Wait for YouTube live chat messages to load
    try {
        await page.waitForSelector('yt-live-chat-text-message-renderer', { state: 'visible' });
    } catch (error) {
        console.error('Error: Unable to load YouTube live chat. Please check the link.');
        await browser.close();
        io.close();
        return;
    }

    // Variable to store the previous chat message
    let oldChat: { type: string; name: string; message: string } | null = null;

    // Set interval to fetch the latest chat messages
    const interval = setInterval(async () => {
        const latestChat = await page.evaluate(() => {
            const chatItems = document.querySelectorAll('yt-live-chat-text-message-renderer');
            const latestItem = chatItems[chatItems.length - 1];

            if (!latestItem) return null;

            const name = latestItem.querySelector('#author-name')?.textContent?.trim();
            const messageElement = latestItem.querySelector<HTMLElement>('#message');
            let message = '';

            if (messageElement) {
                messageElement.childNodes.forEach((node) => {
                    if (node.nodeType === Node.TEXT_NODE) {
                        message += node.textContent?.trim() || '';
                    } else if (node.nodeType === Node.ELEMENT_NODE) {
                        const element = node as HTMLElement;
                        if (element.tagName === 'IMG' && element.classList.contains('emoji')) {
                            const emojiSrc = element.getAttribute('src');
                            if (emojiSrc) {
                                message += `<img src="${emojiSrc}" alt="emoji" class="emoji" style="width: 24px; height: 24px; vertical-align: middle;" />`;
                            }
                        }
                    }
                });
                message = message.trim();
            }

            return name && message ? { type: 'default', name, message } : null;
        });

        // Emit new chat messages to connected clients
        if (latestChat && (!oldChat || oldChat.message !== latestChat.message)) {
            io.emit('latest-chat', latestChat);
        }

        oldChat = latestChat;
    }, delay);

    // Graceful shutdown on process termination
    process.on('SIGINT', async () => {
        clearInterval(interval);
        await browser.close();
        io.close();
        process.exit(0);
    });

    console.info('\nPress Ctrl + C to terminate.');
})();
