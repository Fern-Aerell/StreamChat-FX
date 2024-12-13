import * as fs from 'fs';
import * as path from 'path';

/**
 * Save JSON data to a file.
 * 
 * @param fileName - The name of the file (without extension).
 * @param data - The data object to be saved.
 */
export function saveJsonData(fileName: string, data: object): void {
  try {
    // Resolve the file path with the .json extension
    const filePath = path.resolve(__dirname, `${fileName}.json`);

    // Convert the data object to a formatted JSON string
    const jsonData = JSON.stringify(data, null, 2);

    // Write the JSON data to the file synchronously
    fs.writeFileSync(filePath, jsonData, 'utf8');
  } catch (error) {
    // console.error(`Failed to save JSON data: ${(error as Error).message}`);
    throw error; // Rethrow error for better debugging
  }
}

/**
 * Load JSON data from a file.
 * 
 * @param fileName - The name of the file (without extension).
 * @returns The parsed JSON object if the file exists and is valid; otherwise, null.
 */
export function loadJsonData<T>(fileName: string): T | null {
  try {
    // Resolve the file path with the .json extension
    const filePath = path.resolve(__dirname, `${fileName}.json`);

    // Check if the file exists
    if (!fs.existsSync(filePath)) {
      return null; // Return null if file does not exist
    }

    // Read the file content synchronously
    const jsonData = fs.readFileSync(filePath, 'utf8');

    // Parse and return the JSON data
    return JSON.parse(jsonData) as T;
  } catch (error) {
    // console.error(`Failed to load JSON data: ${(error as Error).message}`);
    return null; // Return null in case of any error
  }
}