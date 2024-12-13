package main

import (
	"archive/zip"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"time"

	"github.com/briandowns/spinner"
)

// checkNodeFolder checks if the 'node' folder exists and contains 'node.exe' and 'npm.cmd'.
// It also checks if 'npm list' runs successfully.
func checkNodeFolder() (bool, error) {
	// Get the path to the 'node' folder
	exePath, err := os.Executable()
	if err != nil {
		return false, err
	}
	exeDir := filepath.Dir(exePath)
	nodeFolder := filepath.Join(exeDir, "node")
	nodeExe := filepath.Join(nodeFolder, "node.exe")
	npmCmd := filepath.Join(nodeFolder, "npm.cmd")

	// Check if the 'node' folder exists and contains both 'node.exe' and 'npm.cmd'
	if _, err := os.Stat(nodeFolder); os.IsNotExist(err) {
		return false, nil // Folder doesn't exist
	}
	if _, err := os.Stat(nodeExe); os.IsNotExist(err) {
		return false, nil // node.exe not found
	}
	if _, err := os.Stat(npmCmd); os.IsNotExist(err) {
		return false, nil // npm.cmd not found
	}

	// Run 'npm list' to check if it works
	cmd := exec.Command(npmCmd, "list")
	_, err = cmd.CombinedOutput()
	if err != nil {
		return false, nil // npm list failed
	}

	return true, nil // Everything is fine
}

// extractZipWithProgress extracts the contents of a ZIP file to the specified destination folder
func extractZipWithProgress(zipFile, destFolder string, sp *spinner.Spinner) error {
	// Open the ZIP file for reading
	zipReader, err := zip.OpenReader(zipFile)
	if err != nil {
		return err
	}
	defer zipReader.Close()

	// Create the destination folder if it doesn't exist
	err = os.MkdirAll(destFolder, 0755)
	if err != nil {
		return err
	}

	// Calculate the total size of the ZIP content for progress tracking
	var totalSize int64
	for _, file := range zipReader.File {
		totalSize += file.FileInfo().Size()
	}

	var extracted int64
	startTime := time.Now()

	// Extract each file in the ZIP archive
	for _, file := range zipReader.File {
		rc, err := file.Open()
		if err != nil {
			return err
		}
		defer rc.Close()

		// Determine the destination file path
		destPath := filepath.Join(destFolder, file.Name)
		if file.FileInfo().IsDir() {
			// Create directories for nested folders inside the ZIP
			err := os.MkdirAll(destPath, file.Mode())
			if err != nil {
				return err
			}
			continue
		}

		// Create the necessary directories for the destination file
		err = os.MkdirAll(filepath.Dir(destPath), 0755)
		if err != nil {
			return err
		}

		// Open the destination file for writing
		destFile, err := os.Create(destPath)
		if err != nil {
			return err
		}
		defer destFile.Close()

		// Copy data from the ZIP file to the destination file
		n, err := io.Copy(destFile, rc)
		if err != nil {
			return err
		}

		// Update the extracted file size
		extracted += n
		progress := float64(extracted) / float64(totalSize) * 100
		elapsed := time.Since(startTime)
		speed := float64(extracted) / elapsed.Seconds()
		remainingTime := time.Duration(float64(totalSize-extracted) / speed * float64(time.Second))

		// Update the spinner with progress information
		sp.Suffix = fmt.Sprintf(" %.2f%% | Speed: %.2f KB/s | Est. Time Left: %s", progress, speed/1024, remainingTime)
	}

	// Stop the spinner and print the completion message
	sp.Stop()
	fmt.Println("\nExtraction completed")
	return nil
}

// downloadFileWithProgress downloads a file from the given URL to the destination path
func downloadFileWithProgress(url, dest string, sp *spinner.Spinner) error {
	// Create the destination file for writing the downloaded content
	out, err := os.Create(dest)
	if err != nil {
		return err
	}
	defer out.Close()

	// Send a GET request to the URL
	resp, err := http.Get(url)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	// Get the total size of the file for progress calculation
	totalSize := resp.ContentLength
	var downloaded int64

	// Track the start time for speed and estimated time calculation
	startTime := time.Now()
	buf := make([]byte, 1024) // Buffer for reading the file in chunks

	// Read the file in chunks and write to the destination file
	for {
		n, err := resp.Body.Read(buf)
		if n > 0 {
			out.Write(buf[:n]) // Write chunk to the destination file
			downloaded += int64(n)

			// Calculate the progress, speed, and estimated time left
			progress := float64(downloaded) / float64(totalSize) * 100
			elapsed := time.Since(startTime)
			speed := float64(downloaded) / elapsed.Seconds()
			remainingTime := time.Duration(float64(totalSize-downloaded) / speed * float64(time.Second))

			// Update the spinner with progress information
			sp.Suffix = fmt.Sprintf(" %.2f%% | Speed: %.2f KB/s | Est. Time Left: %s", progress, speed/1024, remainingTime)
		}

		if err == io.EOF {
			break // End of file reached
		}
		if err != nil {
			return err
		}
	}

	// Stop the spinner and print the completion message
	sp.Stop()
	fmt.Println("\nDownload completed!")
	return nil
}

// setupEnvironment handles the setup process:
// 1. Checks if the required node folder exists and contains the necessary files.
// 2. Downloads and extracts Node.js if not found.
// 3. Renames the extracted folder to 'node'.
func setupEnvironment() error {
	// Get the path of the currently running executable
	exePath, err := os.Executable()
	if err != nil {
		return fmt.Errorf("error getting executable path: %w", err)
	}

	exeDir := filepath.Dir(exePath) // Extract directory from executable path

	// Check if the 'node' folder exists and contains the necessary files
	isValid, err := checkNodeFolder()
	if err != nil {
		return fmt.Errorf("error checking node folder: %w", err)
	}

	if isValid {
		// If everything is already set up correctly, do nothing and return
		return nil
	}

	// If the folder or files are missing, start the setup process

	// Path to the ZIP file for Node.js
	nodeZipPath := filepath.Join(exeDir, "node.zip")

	// If the ZIP file is not found, download it
	if _, err := os.Stat(nodeZipPath); os.IsNotExist(err) {
		nodeZipUrl := "https://nodejs.org/dist/v23.4.0/node-v23.4.0-win-x64.zip"

		// Set up a spinner to show download progress
		s := spinner.New(spinner.CharSets[9], 100*time.Millisecond)
		s.Start()

		// Download the ZIP file with progress
		if err := downloadFileWithProgress(nodeZipUrl, nodeZipPath, s); err != nil {
			return fmt.Errorf("download failed: %w", err)
		}
	}

	// Set up a spinner to show extraction progress
	s := spinner.New(spinner.CharSets[9], 100*time.Millisecond)
	s.Start()

	// Extract the downloaded ZIP file
	if err := extractZipWithProgress(nodeZipPath, exeDir, s); err != nil {
		return fmt.Errorf("extraction failed: %w", err)
	}

	// Rename the extracted folder
	oldFolderPath := filepath.Join(exeDir, "node-v23.4.0-win-x64")
	newFolderPath := filepath.Join(exeDir, "node")
	if err := os.Rename(oldFolderPath, newFolderPath); err != nil {
		return fmt.Errorf("renaming folder failed: %w", err)
	}

	// Delete the ZIP file after successful extraction and renaming
	if err := os.Remove(nodeZipPath); err != nil {
		return fmt.Errorf("failed to delete ZIP file: %w", err)
	}

	return nil
}

// main initializes the environment setup process and runs npm commands
func main() {

	// Call the setupEnvironment function
	if err := setupEnvironment(); err != nil {
		log.Fatalf("Error during setup: %v", err)
	}

	// Proceed with running npm commands
	exePath, err := os.Executable()
	if err != nil {
		log.Fatalf("Error getting executable path: %v", err)
	}

	folderPath := filepath.Join(filepath.Dir(exePath), "node")
	cmd := exec.Command(filepath.Join(folderPath, "npm.cmd"), "list")
	_, err = cmd.CombinedOutput()
	if err != nil {
		// If 'npm list' fails, run 'npm install'
		log.Printf("npm list failed, running npm install...")

		cmd := exec.Command(filepath.Join(folderPath, "npm.cmd"), "install")
		output, err := cmd.CombinedOutput()
		if err != nil {
			log.Fatalf("Error executing npm install: %v\n", err)
		}

		// Print the output of the npm command
		fmt.Printf("%s\n", output)
		log.Println("Setup complete!")
	}

}
