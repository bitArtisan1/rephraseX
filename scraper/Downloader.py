import requests
import os
import re
from alive_progress import alive_bar, config_handler

class Downloader:
    def __init__(self, urls):
        self.urls = urls

    def sanitize_filename(self, filename):
        # Remove or replace invalid characters
        return re.sub(r'[<>:"/\\|?*]', '', filename)

    def download(self, folder):
        if not os.path.exists("images"):
            os.mkdir("images")
        
        if not os.path.exists(f"images/{folder}"):
            os.mkdir(f"images/{folder}")

        for link in self.urls:
            print(f"Downloading {link}")
            r = requests.get(link, allow_redirects=True, stream=True)
            
            filename = link.split("/")[-1].split('?')[0]  # Get filename and remove URL parameters
            sanitized_filename = self.sanitize_filename(filename)
            file_path = f"images/{folder}/{sanitized_filename}.jpg"  # Append .jpg to filename

            total_size = int(r.headers.get('content-length', 0))
            block_size = 1024  # 1KB
            downloaded_size = 0

            # Customizing the progress bar
            config_handler.set_global(
                bar='classic',          # Custom bar style ('classic', 'smooth', 'blocks', etc.)
                spinner='waves',       # Custom spinner style ('dots', 'waves', 'arrows', etc.)
                title_length=30,       # Set title length (title will be cut to fit)
                theme='smooth',        # You can also apply a preset theme like 'smooth', 'retro', 'modern', etc.
            )

            with open(file_path, 'wb') as f, alive_bar(
                total_size, title=f"Downloading {sanitized_filename}"
            ) as bar:
                for data in r.iter_content(block_size):
                    f.write(data)
                    downloaded_size += len(data)
                    bar(len(data))  # Update the progress bar with the size of the block

        print("Download complete.")
