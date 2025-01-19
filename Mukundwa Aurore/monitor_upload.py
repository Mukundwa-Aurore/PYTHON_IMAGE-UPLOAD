import os
import time
import shutil
import subprocess

# Configuration
WATCH_FOLDER = "C:/Users/user/Documents/Mukundwa Aurore/camera"  # Use forward slashes or double backslashes
UPLOADED_FOLDER = "C:/Users/user/Documents/Mukundwa Aurore/Uploaded"  # Use forward slashes or double backslashes
UPLOAD_URL = "https://projects.benax.rw/f/o/r/e/a/c/h/p/r/o/j/e/c/t/s/4e8d42b606f70fa9d39741a93ed0356c/iot_testing_202501/upload.php"
CHECK_INTERVAL = 5  # Check for new files every 5 seconds
UPLOAD_DELAY = 30  # Wait 30 seconds before uploading new files

# Ensure the "uploaded" folder exists
os.makedirs(UPLOADED_FOLDER, exist_ok=True)

def upload_file(file_path):
    """Uploads a file using curl command."""
    try:
        result = subprocess.run(
            ["curl", "-X", "POST", "-F", f"imageFile=@{file_path}", UPLOAD_URL],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode == 0:
            print(f"Successfully uploaded: {file_path}")
            return True
        else:
            print(f"Failed to upload {file_path}: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error during upload: {e}")
        return False

def move_file_to_uploaded(file_path):
    """Moves a file to the 'uploaded' folder."""
    try:
        destination = os.path.join(UPLOADED_FOLDER, os.path.basename(file_path))
        shutil.move(file_path, destination)
        print(f"Moved {file_path} to {destination}")
    except Exception as e:
        print(f"Error moving file {file_path}: {e}")

def monitor_folder():
    """Monitors the folder for new files and uploads them."""
    uploaded_files = set()  # Track files that have already been processed

    while True:
        for filename in os.listdir(WATCH_FOLDER):
            file_path = os.path.join(WATCH_FOLDER, filename)

            # Skip if it's not a file or has already been uploaded
            if not os.path.isfile(file_path) or file_path in uploaded_files:
                continue

            # Wait for 30 seconds before uploading
            print(f"Waiting {UPLOAD_DELAY} seconds to upload: {file_path}")
            time.sleep(UPLOAD_DELAY)

            # Attempt to upload the file
            if upload_file(file_path):
                move_file_to_uploaded(file_path)
                uploaded_files.add(file_path)

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    print("Monitoring folder for new images...")
    monitor_folder()
