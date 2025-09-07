import requests
import os
from urllib.parse import urlparse
import hashlib

def get_filename_from_url(url):
    """Extracts filename from URL or generates one using a hash."""
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    if not filename:
        # Generate a filename from the hash of the URL
        filename = hashlib.md5(url.encode()).hexdigest() + ".jpg"
    return filename

def download_image(url, directory="Fetched_Images"):
    """Downloads an image from a URL and saves it to the directory."""
    try:
        # Create directory if it doesn't exist
        os.makedirs(directory, exist_ok=True)

        # Set headers to mimic a browser request
        headers = {
            "User-Agent": "UbuntuImageFetcher/1.0 (+https://example.com)"
        }

        # Fetch the image with timeout
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors

        # Extract filename
        filename = get_filename_from_url(url)
        filepath = os.path.join(directory, filename)

        # Prevent downloading duplicates
        if os.path.exists(filepath):
            print(f"⚠ Image already exists: {filename}")
            return

        # Save image in binary mode
        with open(filepath, 'wb') as f:
            f.write(response.content)

        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error for {url}: {e}")
    except Exception as e:
        print(f"✗ An error occurred for {url}: {e}")

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    # Get multiple URLs from user separated by commas
    urls_input = input("Please enter image URL(s), separated by commas: ")
    urls = [url.strip() for url in urls_input.split(",") if url.strip()]

    for url in urls:
        download_image(url)

    print("\nConnection strengthened. Community enriched.")

if __name__ == "__main__":
    main()