# YT Live Chat Service

YT Live Chat Service is a tool designed to extract real-time chat data from YouTube Live streams. It allows users to utilize live chat data for various purposes, such as creating custom live chat overlays for streaming software like OBS, and more. The service is currently designed for **Windows** platforms.

## Features

- Fetch real-time YouTube Live Chat data.
- Customizable delay intervals for chat updates.
- Cross-platform compatibility for paths (Windows-focused).
- Provides an easy-to-use interface for setting up and configuring the service.
- Emits live chat data via Socket.IO for flexible integration into other tools or custom applications.

## Prerequisites

Before you start, ensure you have the following installed on your system:

- [Node.js](https://nodejs.org/) (v16 or higher recommended)
- [npm](https://www.npmjs.com/) (comes with Node.js)
- [Playwright](https://playwright.dev/) (automatically installed as a dependency)

## Installation and Build

Follow these steps to set up the project:

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install the required dependencies:
   ```bash
   npm install
   ```

3. Build the project:
   ```bash
   npm run build
   ```

4. After building, you will find the output in the `dist` folder. Inside the `dist` folder, a `service.bat` file will be available for running the service.

## Usage

1. Run the service by executing the `service.bat` file located in the `dist` folder. This will:
   - Set up the required environment.
   - Prompt you to provide the necessary configurations such as:
     - Browser executable path.
     - Update delay (in milliseconds).
     - Port number for the service.
     - YouTube Live Chat link.
     - Whether to run the browser in headless mode.

2. Once the setup is complete, the service will start and display the port number on which it is running.

3. Connect to the service using Socket.IO or other tools to fetch live chat data.

## Configuration Details

During the setup process, the service will prompt you for the following inputs:

- **Browser Executable Path**: Path to your browser executable (e.g., Chrome or Edge).
- **Update Delay**: Time interval (in milliseconds) for fetching new chat messages. Must be at least 500ms.
- **Port**: Port number for the service. If "random" is selected, the system will assign an available port.
- **Headless Mode**: Whether the browser runs in headless mode (`true` or `false`).
- **YouTube Live Chat Link**: The URL of the YouTube Live Chat to fetch data from.

The configuration is saved and reused for subsequent runs.

## Example Output

The service emits live chat messages via Socket.IO in the following format:

```json
{
  "type": "default",
  "name": "User Name",
  "message": "Hello, world!"
}
```

## Limitations

- Currently supports **Windows** only.
- Requires manual setup for browser executable paths.
- The minimum update delay is 500 milliseconds.

## License

This project is licensed under Custom License. Please refer to the `LICENSE` file for more details.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request to help improve this project.

## Contact

For questions or support, please contact Fern Aerell at fernaerell2020@gmail.com.