import { chromium } from 'playwright';

/**
 * Validate if the provided link is a valid YouTube Live Chat URL.
 *
 * @param link - The URL string to validate.
 * @returns `true` if the link is a valid YouTube Live Chat URL; otherwise, `false`.
 */
export async function validateYoutubeLiveChatLink(link: string): Promise<boolean> {
  try {
    // Step 1: Parse the URL string into a URL object
    const urlObj = new URL(link);

    // Step 2: Validate the domain (hostname) and the path
    if (
      urlObj.hostname !== 'www.youtube.com' || // The hostname must match YouTube
      urlObj.pathname !== '/live_chat' // The path must be '/live_chat'
    ) {
      return false;
    }

    // Step 3: Check if the 'v' parameter (video ID) exists
    const videoId = urlObj.searchParams.get('v');
    if (!videoId) {
      return false; // Return false if the video ID is missing
    }

    // If all validations pass, return true
    return true;
  } catch (error) {
    // Return false if the URL is invalid or any error occurs
    return false;
  }
}

/**
 * Validate if the provided Chromium executable path is valid.
 *
 * @param executablePath - The file path to the Chromium executable.
 * @returns `true` if the Chromium executable is valid; otherwise, `false`.
 */
export async function validateBrowserExecutablePath(executablePath: string): Promise<boolean> {
  try {
    // Attempt to launch a Chromium browser instance using the provided executable path
    const browser = await chromium.launch({ executablePath });

    // Close the browser to release resources
    await browser.close();

    // If the browser launched successfully, return true
    return true;
  } catch (error) {
    // If an error occurs, return false
    return false;
  }
}