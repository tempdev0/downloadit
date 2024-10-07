import requests
import os
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

def download_js_file(url, output_dir, overwrite):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        filename = os.path.join(output_dir, url.split('/')[-1])
        
        # Check if file exists and handle overwrite logic
        if not overwrite and os.path.exists(filename):
            print(f"File already exists and overwrite is disabled: {filename}")
            return
        
        # Write the file to disk
        with open(filename, 'wb') as js_file:
            js_file.write(response.content)
        
        # Check if the URL contains '.js' and rename the file to ensure it has a .js extension
        if '.js' in url and not filename.endswith('.js'):
            new_filename = filename + '.js'
            os.rename(filename, new_filename)
            print(f"Renamed to: {new_filename}")
        else:
            print(f"Downloaded: {filename}")
    
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")
    except Exception as e:
        print(f"Error processing {url}: {e}")

def download_js_files(input_file, output_dir, overwrite):
    os.makedirs(output_dir, exist_ok=True)

    try:
        with open(input_file, 'r') as file:
            urls = file.readlines()
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        return

    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(download_js_file, url.strip(), output_dir, overwrite): url.strip() for url in urls if url.strip()}
        
        for future in as_completed(futures):
            _ = futures[future]  # Get the original URL from the future

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download JavaScript files from URLs listed in a text file.")
    parser.add_argument('input_file', type=str, help='Path to the input text file containing URLs.')
    parser.add_argument('-o', '--output-dir', type=str, default='downloaded_js', help='Directory to save downloaded files.')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing files.')
    
    args = parser.parse_args()
    download_js_files(args.input_file, args.output_dir, args.overwrite)
