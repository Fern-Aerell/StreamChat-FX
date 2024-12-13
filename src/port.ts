import * as net from 'net';

export const MIN_PORT_NUMBER = 49152; // Minimum port number for dynamic/private ports.
export const MAX_PORT_NUMBER = 65535; // Maximum port number for dynamic/private ports.

/**
 * Generates a random port number within the specified range.
 * @param min - Minimum port number (default is MIN_PORT_NUMBER).
 * @param max - Maximum port number (default is MAX_PORT_NUMBER).
 * @returns A random port number between min and max.
 */
export function getRandomPort(min: number = MIN_PORT_NUMBER, max: number = MAX_PORT_NUMBER): number {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

/**
 * Checks if a given port is available for use.
 * @param port - The port number to check.
 * @returns A promise that resolves to true if the port is available, otherwise false.
 */
export function isPortAvailable(port: number): Promise<boolean> {
    return new Promise((resolve) => {
        const server = net.createServer();

        server.once('error', () => {
            // If an error occurs, the port is not available.
            resolve(false);
        });

        server.once('listening', () => {
            // If the server starts listening, the port is available.
            server.close(() => resolve(true));
        });

        server.listen(port);
    });
}

/**
 * Finds a random available port within the specified range.
 * @param min - Minimum port number (default is MIN_PORT_NUMBER).
 * @param max - Maximum port number (default is MAX_PORT_NUMBER).
 * @returns A promise that resolves to an available port number.
 */
export async function getAvailablePort(min: number = MIN_PORT_NUMBER, max: number = MAX_PORT_NUMBER): Promise<number> {
    let port: number;

    do {
        // Generate a random port and check if it is available.
        port = getRandomPort(min, max);
    } while (!(await isPortAvailable(port)));

    return port;
}